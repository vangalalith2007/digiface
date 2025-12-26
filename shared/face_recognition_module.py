"""
Face Recognition Module
Handles face detection, gender classification, and face recognition using DeepFace
"""

import cv2
import numpy as np
from typing import List, Dict, Optional, Tuple
from deepface import DeepFace

import config


class FaceRecognitionModule:
    """Handles all face detection and recognition operations"""
    
    def __init__(self):
        self.detector_backend = config.FACE_DETECTOR_BACKEND
        self.model_name = config.FACE_RECOGNITION_MODEL
        print(f"Initialized Face Recognition Module")
        print(f"Detector: {self.detector_backend}, Model: {self.model_name}")
    
    def detect_faces(self, frame: np.ndarray) -> List[Dict]:
        """
        Detect faces in the given frame
        
        Args:
            frame: Input image frame (BGR format from OpenCV)
        
        Returns:
            List of detected face dictionaries with coordinates and info
        """
        try:
            # DeepFace.extract_faces returns list of face dictionaries
            faces = DeepFace.extract_faces(
                img_path=frame,
                detector_backend=self.detector_backend,
                enforce_detection=False,
                align=True
            )
            
            return faces
        
        except Exception as e:
            print(f"Error detecting faces: {e}")
            return []
    
    def analyze_face(self, frame: np.ndarray, face_region: Dict) -> Optional[Dict]:
        """
        Analyze a detected face for gender and other attributes
        
        Args:
            frame: Input image frame
            face_region: Face region dictionary from detect_faces
        
        Returns:
            Analysis results including gender
        """
        try:
            # Extract face coordinates
            facial_area = face_region.get('facial_area', {})
            x = facial_area.get('x', 0)
            y = facial_area.get('y', 0)
            w = facial_area.get('w', 0)
            h = facial_area.get('h', 0)
            
            # Crop face region
            face_img = frame[y:y+h, x:x+w]
            
            # Analyze face attributes
            analysis = DeepFace.analyze(
                img_path=face_img,
                actions=['gender'],
                detector_backend=self.detector_backend,
                enforce_detection=False,
                silent=True
            )
            
            # DeepFace.analyze returns a list, get first result
            if isinstance(analysis, list) and len(analysis) > 0:
                return analysis[0]
            return analysis
        
        except Exception as e:
            print(f"Error analyzing face: {e}")
            return None
    
    def get_face_embedding(self, frame: np.ndarray, face_region: Dict) -> Optional[np.ndarray]:
        """
        Generate face embedding for recognition
        
        Args:
            frame: Input image frame
            face_region: Face region dictionary from detect_faces
        
        Returns:
            Face embedding as numpy array
        """
        try:
            # Extract face coordinates
            facial_area = face_region.get('facial_area', {})
            x = facial_area.get('x', 0)
            y = facial_area.get('y', 0)
            w = facial_area.get('w', 0)
            h = facial_area.get('h', 0)
            
            # Crop face region
            face_img = frame[y:y+h, x:x+w]
            
            # Generate embedding
            embedding_objs = DeepFace.represent(
                img_path=face_img,
                model_name=self.model_name,
                detector_backend=self.detector_backend,
                enforce_detection=False
            )
            
            # DeepFace.represent returns a list of dictionaries
            if isinstance(embedding_objs, list) and len(embedding_objs) > 0:
                embedding = embedding_objs[0].get('embedding')
                return np.array(embedding)
            
            return None
        
        except Exception as e:
            print(f"Error generating face embedding: {e}")
            return None
    
    def draw_face_box(self, frame: np.ndarray, face_region: Dict, 
                      label: str, color: Tuple[int, int, int]) -> np.ndarray:
        """
        Draw bounding box and label on face
        
        Args:
            frame: Input image frame
            face_region: Face region dictionary
            label: Text label to display
            color: Box color (BGR)
        
        Returns:
            Frame with drawn box and label
        """
        facial_area = face_region.get('facial_area', {})
        x = facial_area.get('x', 0)
        y = facial_area.get('y', 0)
        w = facial_area.get('w', 0)
        h = facial_area.get('h', 0)
        
        # Draw rectangle
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        
        # Draw label background
        label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 
                                        config.FONT_SCALE, config.FONT_THICKNESS)
        cv2.rectangle(frame, (x, y - label_size[1] - 10), 
                     (x + label_size[0], y), color, -1)
        
        # Draw label text
        cv2.putText(frame, label, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,
                   config.FONT_SCALE, config.TEXT_COLOR, config.FONT_THICKNESS)
        
        return frame
    
    def get_gender_from_analysis(self, analysis: Dict) -> str:
        """
        Extract gender from analysis results
        
        Args:
            analysis: Analysis dictionary from analyze_face
        
        Returns:
            Gender string (Male/Female)
        """
        if not analysis:
            return "Unknown"
        
        gender_data = analysis.get('gender', {})
        if isinstance(gender_data, dict):
            # Get the gender with highest confidence
            male_conf = gender_data.get('Man', 0)
            female_conf = gender_data.get('Woman', 0)
            return "Male" if male_conf > female_conf else "Female"
        
        return "Unknown"
