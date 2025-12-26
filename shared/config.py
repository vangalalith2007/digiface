"""
OPTIMIZED Configuration for Snapdragon Chipsets
This configuration is optimized for better performance on Qualcomm Snapdragon processors
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Camera settings - Reduced resolution for faster processing
CAMERA_INDEX = 0
CAMERA_WIDTH = 320  # Reduced from 640 (2x faster processing)
CAMERA_HEIGHT = 240  # Reduced from 480

# File paths
DATA_TEMPLATE_PATH = "data_template.json"
DATABASE_PATH = "data/users_database.json"

# Face recognition settings
FACE_MATCH_THRESHOLD = 0.7  # Slightly higher for faster matching
FACE_DETECTION_CONFIDENCE = 0.5

# DeepFace model settings - Optimized for mobile/edge devices
FACE_DETECTOR_BACKEND = "ssd"  # Faster than opencv, good accuracy
# Alternative options for detector:
# - "mtcnn": More accurate but slower
# - "retinaface": Best accuracy but slowest
# - "opencv": Fastest but less accurate (default)

FACE_RECOGNITION_MODEL = os.environ.get('FACE_RECOGNITION_MODEL', "Facenet")
# Model comparison:
# - "Facenet": 90MB, Fast, 99.6% accuracy (RECOMMENDED for Snapdragon)
# - "VGG-Face": 500MB, Slow, 98.9% accuracy (Original)
# - "ArcFace": 166MB, Medium, 99.4% accuracy
# - "OpenFace": 30MB, Very Fast, 93% accuracy (Use if speed critical)

# Localization Settings for India
SUPPORTED_LANGUAGES = {
    "en-US": "English",
    "hi-IN": "Hindi",
    "ta-IN": "Tamil",
    "te-IN": "Telugu",
    "kn-IN": "Kannada",
    "ml-IN": "Malayalam",
    "mr-IN": "Marathi",
    "gu-IN": "Gujarati",
    "bn-IN": "Bengali"
}
DEFAULT_LANGUAGE = "en-US"

# Voice recognition settings
SPEECH_RECOGNITION_LANGUAGE = os.environ.get('SPEECH_LANG', DEFAULT_LANGUAGE)
SPEECH_TIMEOUT = 5  # seconds to wait for speech
SPEECH_PHRASE_TIME_LIMIT = 10  # max seconds for a single phrase

# Text-to-speech settings
TTS_RATE = 150  # Speaking rate (words per minute)
TTS_VOLUME = 0.9  # Volume level (0.0 to 1.0)

# Display settings
FONT_SCALE = 0.6
FONT_THICKNESS = 2
BOX_COLOR_NEW = (0, 255, 0)  # Green for new faces
BOX_COLOR_KNOWN = (255, 0, 0)  # Blue for known faces
TEXT_COLOR = (255, 255, 255)  # White text

# Performance optimization settings
FRAME_SKIP_INTERVAL = 60  # Process every 60 frames instead of 30 (reduces CPU load)
ENABLE_GPU_ACCELERATION = True  # Enable if TensorFlow GPU support available
