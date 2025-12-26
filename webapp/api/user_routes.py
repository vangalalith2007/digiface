"""
User Management API Routes
"""

from flask import Blueprint, request, jsonify
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from storage_manager import StorageManager

bp = Blueprint('user', __name__, url_prefix='/api/user')

# Storage will be initialized when app starts
storage = None

def init_storage(stor):
    """Initialize storage from main app"""
    global storage
    storage = stor

@bp.route('/list', methods=['GET'])
def list_users():
    """Get list of all registered users"""
    try:
        users = storage.get_all_users()
        
        # Return user data without embeddings (too large)
        user_list = []
        for user in users:
            user_list.append({
                'id': user['user_id'],
                'data': user['data'],
                'timestamp': user['timestamp'],
                'model': user.get('model_name', 'Unknown')
            })
        
        return jsonify({
            'success': True,
            'users': user_list,
            'count': len(user_list)
        })
    
    except Exception as e:
        print(f"Error in list_users: {e}")
        return jsonify({'error': str(e)}), 500

@bp.route('/count', methods=['GET'])
def get_user_count():
    """Get total number of registered users"""
    try:
        count = storage.get_user_count()
        return jsonify({
            'success': True,
            'count': count
        })
    except Exception as e:
        print(f"Error in get_user_count: {e}")
        return jsonify({'error': str(e)}), 500
