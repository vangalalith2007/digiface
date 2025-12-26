"""
Flask Web Application for Face Recognition
Main application entry point
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import sys
import os

# Add parent and shared directories to path to import existing modules
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)
sys.path.append(os.path.join(root_dir, 'shared'))

from face_recognition_module import FaceRecognitionModule
from storage_manager import StorageManager
import config

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
CORS(app, resources={r"/api/*": {"origins": os.environ.get('ALLOWED_ORIGINS', '*')}})
socketio = SocketIO(app, cors_allowed_origins=os.environ.get('ALLOWED_ORIGINS', '*'))

# Initialize modules
face_module = FaceRecognitionModule()
storage = StorageManager()

print("="*60)
print("Face Recognition Web Application")
print(f"Database contains {storage.get_user_count()} users")
print("="*60)

@app.route('/')
def index():
    """Serve the main web interface"""
    return render_template('index.html')

@app.route('/api/status', methods=['GET'])
def status():
    """API health check"""
    return jsonify({
        'status': 'online',
        'users_count': storage.get_user_count(),
        'model': config.FACE_RECOGNITION_MODEL
    })

@app.route('/api/template', methods=['GET'])
def get_template():
    """Get data collection template"""
    import json
    try:
        with open(config.DATA_TEMPLATE_PATH, 'r', encoding='utf-8') as f:
            template = json.load(f)
        return jsonify(template)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Import API routes
from api import face_routes, user_routes

# Register blueprints
app.register_blueprint(face_routes.bp)
app.register_blueprint(user_routes.bp)

# Initialize modules in routes
face_routes.init_modules(face_module, storage)
user_routes.init_storage(storage)

# WebSocket events
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print('Client connected')
    emit('status', {'message': 'Connected to server'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print('Client disconnected')

if __name__ == '__main__':
    print("\nStarting Flask server...")
    print("Access the web app at: http://localhost:5000")
    print("Press Ctrl+C to stop\n")
    
    # Get port from environment variable (for production) or use 5000
    port = int(os.environ.get('PORT', 5000))
    
    # Run with SocketIO
    socketio.run(app, host='0.0.0.0', port=port, debug=True, allow_unsafe_werkzeug=True)
