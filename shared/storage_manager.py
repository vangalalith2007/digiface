"""
Storage Manager Module
Handles saving and loading user data with face embeddings
"""

import json
import os
import uuid
from datetime import datetime
from typing import Dict, List, Optional
import numpy as np

import config


class StorageManager:
    """Manages user data storage with face embeddings"""
    
    def __init__(self, database_path: Optional[str] = None):
        self.database_path = database_path or os.environ.get('DATABASE_PATH', config.DATABASE_PATH)
        self.users = []
        
        # Check if using SQL database (future-proofing)
        self.db_url = os.environ.get('DATABASE_URL')
        if self.db_url:
            print(f"SQL Database detected: {self.db_url.split('@')[-1]}")
            # In a real implementation, we would initialize SQLAlchemy here
            # For now, we'll stick to JSON but keep the structure ready
        
        self._ensure_data_directory()
        self.load_database()
    
    def _ensure_data_directory(self):
        """Create data directory if it doesn't exist"""
        data_dir = os.path.dirname(self.database_path)
        if data_dir and not os.path.exists(data_dir):
            os.makedirs(data_dir)
            print(f"Created data directory: {data_dir}")
    
    def load_database(self):
        """Load existing user database from JSON file"""
        if os.path.exists(self.database_path):
            try:
                with open(self.database_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.users = data.get('users', [])
                
                print(f"Loaded {len(self.users)} users from database")
                
                # Check for model compatibility
                if self.users:
                    first_user = self.users[0]
                    stored_model = first_user.get('model_name', 'Unknown')
                    stored_dim = first_user.get('embedding_dim', len(first_user.get('face_embedding', [])))
                    
                    if stored_model != 'Unknown' and stored_model != config.FACE_RECOGNITION_MODEL:
                        print("\n" + "="*60)
                        print("⚠️  MODEL COMPATIBILITY WARNING")
                        print("="*60)
                        print(f"Database was created with: {stored_model} (embedding dim: {stored_dim})")
                        print(f"Current config uses: {config.FACE_RECOGNITION_MODEL}")
                        print("\nExisting users will NOT be recognized with the new model.")
                        print("Options:")
                        print("  1. Delete data/users_database.json to start fresh")
                        print("  2. Change FACE_RECOGNITION_MODEL back to '{}'".format(stored_model))
                        print("="*60 + "\n")
                        
            except Exception as e:
                print(f"Error loading database: {e}")
                self.users = []
        else:
            print("No existing database found. Starting fresh.")
            self.users = []
    
    def save_database(self):
        """Save user database to JSON file"""
        try:
            data = {
                'users': self.users,
                'last_updated': datetime.now().isoformat()
            }
            with open(self.database_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Database saved successfully with {len(self.users)} users")
        except Exception as e:
            print(f"Error saving database: {e}")
    
    def add_user(self, user_data: Dict, face_embedding: np.ndarray) -> str:
        """
        Add a new user to the database
        
        Args:
            user_data: Dictionary containing user information from template
            face_embedding: Face embedding vector (numpy array)
        
        Returns:
            user_id: Unique identifier for the user
        """
        user_id = str(uuid.uuid4())
        
        user_record = {
            'user_id': user_id,
            'timestamp': datetime.now().isoformat(),
            'face_embedding': face_embedding.tolist(),  # Convert numpy array to list
            'embedding_dim': len(face_embedding),  # Store embedding dimension
            'model_name': config.FACE_RECOGNITION_MODEL,  # Store model used
            'data': user_data
        }
        
        self.users.append(user_record)
        self.save_database()
        
        print(f"Added new user: {user_data.get('name', 'Unknown')} (ID: {user_id})")
        return user_id
    
    def find_matching_user(self, face_embedding: np.ndarray, threshold: float = config.FACE_MATCH_THRESHOLD) -> Optional[Dict]:
        """
        Find a user with matching face embedding
        
        Args:
            face_embedding: Face embedding to match
            threshold: Maximum distance for a match (lower = stricter)
        
        Returns:
            User record if match found, None otherwise
        """
        if not self.users:
            return None
        
        best_match = None
        best_distance = float('inf')
        
        for user in self.users:
            stored_embedding = np.array(user['face_embedding'])
            distance = self._calculate_distance(face_embedding, stored_embedding)
            
            if distance < best_distance:
                best_distance = distance
                best_match = user
        
        # Return match only if distance is below threshold
        if best_distance < threshold:
            print(f"Match found: {best_match['data'].get('name', 'Unknown')} (distance: {best_distance:.4f})")
            return best_match
        
        return None
    
    def _calculate_distance(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """
        Calculate Euclidean distance between two embeddings
        
        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector
        
        Returns:
            Distance value (returns infinity if dimensions don't match)
        """
        # Check if embeddings have the same dimension
        if embedding1.shape != embedding2.shape:
            print(f"Warning: Embedding dimension mismatch - {embedding1.shape} vs {embedding2.shape}")
            print(f"This usually happens when switching between different face recognition models.")
            print(f"Current model embedding size: {embedding1.shape[0]}, Stored embedding size: {embedding2.shape[0]}")
            return float('inf')  # Return infinite distance (no match)
        
        return np.linalg.norm(embedding1 - embedding2)
    
    def get_user_count(self) -> int:
        """Get total number of users in database"""
        return len(self.users)
    
    def get_all_users(self) -> List[Dict]:
        """Get all user records"""
        return self.users
