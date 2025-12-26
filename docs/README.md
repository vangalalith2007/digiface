# Face Recognition Application with Voice Data Collection

A Python application that uses computer vision and voice recognition to detect faces, identify individuals, and collect user information through voice interaction.

## Features

- **Real-time Face Detection**: Detects human faces using webcam
- **Face Recognition**: Identifies previously captured individuals using face embeddings
- **Gender Classification**: Automatically classifies gender
- **Voice-Based Data Collection**: Collects user information via speech-to-text
- **Voice Abort Commands**: Say "stop" or "quit" to cancel data collection at any time
- **Template-Driven**: Configurable data fields via JSON template
- **Persistent Storage**: Stores user data with face embeddings in JSON format

## Requirements

- Python 3.8 or higher
- Webcam
- Microphone
- Internet connection (for Google Speech Recognition API)

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

**Note**: On Windows, you may need to install PyAudio separately:
```bash
pip install pipwin
pipwin install pyaudio
```

## Configuration

### Data Template (`data_template.json`)

Customize what information to collect by editing the template file:

```json
{
  "fields": [
    {"name": "name", "prompt": "What is your name?", "type": "string"},
    {"name": "age", "prompt": "What is your age?", "type": "integer"},
    {"name": "birth_date", "prompt": "What is your birth date?", "type": "date"},
    {"name": "city", "prompt": "Which city are you from?", "type": "string"},
    {"name": "state", "prompt": "Which state are you from?", "type": "string"}
  ]
}
```

### Application Settings (`config.py`)

Adjust camera, face recognition, and voice settings in `config.py`.

## Usage

1. Run the application:
```bash
python main.py
```

2. Position your face in front of the camera

3. **For new faces**:
   - The system detects it's a new face
   - Voice prompts will ask questions based on the template
   - Speak your answers clearly
   - Data is automatically saved

4. **For known faces**:
   - The system recognizes you
   - Displays your stored information
   - No data collection needed

## Controls

- **q**: Quit application
- **r**: Reload template (if you modified `data_template.json`)

## How It Works

1. **Face Detection**: Uses DeepFace with OpenCV backend to detect faces
2. **Face Embedding**: Generates 128-dimensional embedding vectors for each face
3. **Face Matching**: Compares embeddings using Euclidean distance
4. **Gender Classification**: Analyzes facial features to determine gender
5. **Voice Collection**: Uses Google Speech Recognition for voice-to-text
6. **Data Storage**: Saves user data with embeddings in `data/users_database.json`

## Project Structure

```
TGDemo/
├── main.py                      # Main application
├── face_recognition_module.py   # Face detection and recognition
├── voice_collector.py           # Voice-based data collection
├── storage_manager.py           # Data persistence
├── config.py                    # Configuration settings
├── data_template.json           # Data field template
├── requirements.txt             # Dependencies
└── data/
    └── users_database.json      # User database (created automatically)
```

## Troubleshooting

### PyAudio Installation Issues
- Windows: Use `pipwin install pyaudio`
- Linux: `sudo apt-get install portaudio19-dev python3-pyaudio`
- macOS: `brew install portaudio && pip install pyaudio`

### Microphone Not Working
- Check system microphone permissions
- Ensure microphone is set as default input device

### Face Detection Issues
- Ensure good lighting
- Position face clearly in front of camera
- Adjust `FACE_DETECTION_CONFIDENCE` in `config.py`

### Speech Recognition Errors
- Requires internet connection for Google Speech API
- Speak clearly and at moderate pace
- Reduce background noise

## Privacy Notice

This application captures and stores:
- Face embeddings (mathematical representations, not images)
- Personal information provided via voice
- Gender classification results

Ensure compliance with local privacy laws and regulations before deployment.

## License

This project is for educational and demonstration purposes.
