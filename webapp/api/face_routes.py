"""
Face Detection and Recognition API Routes
"""

from flask import Blueprint, request, jsonify
import base64
import numpy as np
import cv2
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from face_recognition_module import FaceRecognitionModule
from storage_manager import StorageManager
import config

bp = Blueprint('face', __name__, url_prefix='/api/face')

# Modules will be initialized when app starts
face_module = None
storage = None

def init_modules(face_mod, stor):
    """Initialize modules from main app"""
    global face_module, storage
    face_module = face_mod
    storage = stor

def decode_image(image_data):
    """Decode base64 image to numpy array"""
    try:
        # Remove data URL prefix if present
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        
        # Decode base64
        img_bytes = base64.b64decode(image_data)
        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return img
    except Exception as e:
        print(f"Error decoding image: {e}")
        return None

@bp.route('/detect', methods=['POST'])
def detect_face():
    """
    Detect faces in the provided image
    
    Request: {image: "base64_encoded_image"}
    Response: {faces: [{x, y, w, h, confidence, gender}]}
    """
    try:
        data = request.get_json()
        if not data or 'image' not in data:
            return jsonify({'error': 'No image provided'}), 400
        
        # Decode image
        img = decode_image(data['image'])
        if img is None:
            return jsonify({'error': 'Invalid image data'}), 400
        
        # Detect faces
        faces = face_module.detect_faces(img)
        
        result_faces = []
        for face in faces:
            facial_area = face.get('facial_area', {})
            confidence = face.get('confidence', 0)
            
            # Analyze for gender
            analysis = face_module.analyze_face(img, face)
            gender = face_module.get_gender_from_analysis(analysis)
            
            result_faces.append({
                'x': facial_area.get('x', 0),
                'y': facial_area.get('y', 0),
                'w': facial_area.get('w', 0),
                'h': facial_area.get('h', 0),
                'confidence': confidence,
                'gender': gender
            })
        
        return jsonify({
            'success': True,
            'faces': result_faces,
            'count': len(result_faces)
        })
    
    except Exception as e:
        print(f"Error in detect_face: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@bp.route('/recognize', methods=['POST'])
def recognize_face():
    """
    Recognize a face and check if it matches existing users
    
    Request: {image: "base64_encoded_image", face: {x, y, w, h}}
    Response: {recognized: true/false, user: {...} or null}
    """
    try:
        data = request.get_json()
        if not data or 'image' not in data:
            return jsonify({'error': 'No image provided'}), 400
        
        # Decode image
        img = decode_image(data['image'])
        if img is None:
            return jsonify({'error': 'Invalid image data'}), 400
        
        # Get face region
        face_data = data.get('face', {})
        face_region = {
            'facial_area': {
                'x': face_data.get('x', 0),
                'y': face_data.get('y', 0),
                'w': face_data.get('w', 100),
                'h': face_data.get('h', 100)
            }
        }
        
        # Generate face embedding
        face_embedding = face_module.get_face_embedding(img, face_region)
        
        if face_embedding is None:
            return jsonify({'error': 'Could not generate face embedding'}), 400
        
        # Check against database
        matching_user = storage.find_matching_user(face_embedding)
        
        if matching_user:
            return jsonify({
                'success': True,
                'recognized': True,
                'user': {
                    'id': matching_user['user_id'],
                    'data': matching_user['data'],
                    'timestamp': matching_user['timestamp']
                }
            })
        else:
            return jsonify({
                'success': True,
                'recognized': False,
                'user': None
            })
    
    except Exception as e:
        print(f"Error in recognize_face: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@bp.route('/register', methods=['POST'])
def register_user():
    """
    Register a new user with face embedding
    
    Request: {image: "base64_encoded_image", face: {x, y, w, h}, userData: {...}}
    Response: {success: true, user_id: "..."}
    """
    try:
        data = request.get_json()
        if not data or 'image' not in data or 'userData' not in data:
            return jsonify({'error': 'Missing required data'}), 400
        
        # Decode image
        img = decode_image(data['image'])
        if img is None:
            return jsonify({'error': 'Invalid image data'}), 400
        
        # Get face region
        face_data = data.get('face', {})
        face_region = {
            'facial_area': {
                'x': face_data.get('x', 0),
                'y': face_data.get('y', 0),
                'w': face_data.get('w', 100),
                'h': face_data.get('h', 100)
            }
        }
        
        # Generate face embedding
        face_embedding = face_module.get_face_embedding(img, face_region)
        
        if face_embedding is None:
            return jsonify({'error': 'Could not generate face embedding'}), 400
        
        # Get user data
        user_data = data['userData']
        
        # Add gender if provided
        if 'gender' in face_data:
            user_data['gender'] = face_data['gender']
        
        # Save to database
        user_id = storage.add_user(user_data, face_embedding)
        
        return jsonify({
            'success': True,
            'user_id': user_id,
            'message': 'User registered successfully'
        })
    
    except Exception as e:
        print(f"Error in register_user: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
