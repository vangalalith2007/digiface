# Quick Start Guide - Face Recognition Application

## Steps to Run

### 1. Activate Virtual Environment (if not already activated)

```bash
cd c:\TGDemo
.venv\Scripts\activate
```

### 2. Run the Application

```bash
python main.py
```

### 3. What to Expect

**First Time Run:**
- DeepFace will download model weights (~100-200MB) - this happens only once
- May take 1-2 minutes to download and initialize

**Application Window:**
- A window titled "Face Recognition Application" will open
- Shows live camera feed

**Console Output:**
- Displays application status and logs
- Shows face detection results
- Displays user information

### 4. Using the Application

#### For New Users:
1. **Position your face** in front of the camera
2. System detects it's a **new face** (green box)
3. **Listen for voice prompts** and answer clearly:
   - "What is your name?" → Say your name
   - "What is your age?" → Say your age  
   - "What is your birth date?" → Say the date
   - "Which city are you from?" → Say your city
   - "Which state are you from?" → Say your state
4. Data is saved automatically

**💡 Tip:** Say **"stop"** or **"quit"** at any time during data collection to cancel the process.

#### For Returning Users:
1. **Position your face** in front of the camera
2. System **recognizes you** (blue box)
3. Displays "Welcome back, [Your Name]!"
4. Shows your stored information
5. No questions asked

### 5. Controls

- **Press 'q'** - Quit the application
- **Press 'r'** - Reload template (if you modified data_template.json)

### 6. Troubleshooting

**If camera doesn't open:**
- Check if another application is using the camera
- Try changing `CAMERA_INDEX` in `config.py` (try 0, 1, or 2)

**If microphone doesn't work:**
- Ensure microphone permissions are enabled in Windows
- Check that microphone is set as default input device
- Make sure you have internet connection (required for Google Speech Recognition)

**If face detection is slow:**
- This is normal on first run while models load
- Subsequent runs will be faster

**If speech recognition fails:**
- Speak clearly and at moderate pace
- Reduce background noise
- Ensure stable internet connection

### 7. Data Storage

Your data is stored in:
```
c:\TGDemo\data\users_database.json
```

You can view this file to see all captured user records with face embeddings.

### 8. Customizing Data Fields

To change what information is collected:

1. Edit `data_template.json`
2. Add/remove/modify fields
3. Press 'r' while app is running OR restart the app

Example - Adding email field:
```json
{
  "fields": [
    {"name": "name", "prompt": "What is your name?", "type": "string"},
    {"name": "email", "prompt": "What is your email?", "type": "string"}
  ]
}
```

## Quick Command Reference

```bash
# Activate virtual environment
.venv\Scripts\activate

# Run application
python main.py

# Install/update dependencies
pip install -r requirements.txt

# View stored data
type data\users_database.json
```

## Need Help?

Check the full documentation in `README.md` for detailed information and troubleshooting.
