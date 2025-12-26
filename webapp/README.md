# Face Recognition Web App

## Quick Start

### 1. Install Dependencies

```bash
cd webapp
pip install -r requirements_web.txt
```

### 2. Run the Web Server

```bash
python app.py
```

### 3. Open in Browser

Navigate to: **http://localhost:5000**

## Features

- ✅ Real-time face detection via webcam
- ✅ Face recognition (matches against database)
- ✅ Gender classification
- ✅ Template-based user registration
- ✅ Responsive design (works on mobile)
- ✅ REST API for integration

## API Endpoints

### Face Detection
```
POST /api/face/detect
Body: {image: "base64_encoded_image"}
Response: {faces: [{x, y, w, h, gender, confidence}]}
```

### Face Recognition
```
POST /api/face/recognize
Body: {image: "base64_encoded_image", face: {x, y, w, h}}
Response: {recognized: true/false, user: {...}}
```

### User Registration
```
POST /api/face/register
Body: {image: "base64_encoded_image", face: {...}, userData: {...}}
Response: {success: true, user_id: "..."}
```

### Get Template
```
GET /api/template
Response: {fields: [...]}
```

### User Count
```
GET /api/user/count
Response: {count: 5}
```

## Project Structure

```
webapp/
├── app.py                  # Main Flask application
├── api/
│   ├── face_routes.py      # Face detection/recognition endpoints
│   └── user_routes.py      # User management endpoints
├── static/
│   ├── css/
│   │   └── style.css       # Styles
│   └── js/
│       ├── camera.js       # Camera handling
│       ├── face_detection.js  # API communication
│       └── app.js          # Main app logic
├── templates/
│   └── index.html          # Main web interface
└── requirements_web.txt    # Dependencies
```

## Usage

1. **Start Camera**: Click "Start Camera" button
2. **Capture Face**: Click "Capture" to detect faces
3. **Recognition**: 
   - If face is recognized → Shows user info
   - If new face → Shows registration form
4. **Register**: Fill form and click "Save"

## For Android WebView

The web app is designed to work seamlessly in Android WebView:

```kotlin
webView.loadUrl("http://localhost:5000")
// OR for production
webView.loadUrl("https://your-server.com")
```

## Configuration

Edit `../config.py` to change:
- Face recognition model
- Detection confidence threshold
- Camera resolution
- Data template path

## Troubleshooting

**Camera not working:**
- Check browser permissions
- Use HTTPS (required for camera on non-localhost)

**Face detection slow:**
- Reduce camera resolution in `camera.js`
- Use lighter model in `config.py`

**CORS errors:**
- CORS is enabled by default
- Check firewall settings

## Next Steps

- Deploy to cloud (Heroku, Railway, Render)
- Add HTTPS for production
- Wrap in Android WebView for mobile app
