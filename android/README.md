# Android WebView Wrapper for Face Recognition App

## Overview

This Android application wraps the Flask web app in a WebView, providing a native Android experience while maintaining the flexibility of web development.

## Features

- ✅ Native Android app (installable from APK)
- ✅ Full camera and microphone access
- ✅ WebView with JavaScript enabled
- ✅ Permission handling
- ✅ JavaScript bridge for native features
- ✅ Back button navigation
- ✅ Error handling

## Project Structure

```
android/
├── build.gradle                    # App-level build configuration
├── src/main/
│   ├── AndroidManifest.xml         # App manifest with permissions
│   ├── java/com/facerecognition/app/
│   │   └── MainActivity.kt         # Main activity with WebView
│   └── res/
│       └── values/
│           └── strings.xml         # String resources
└── README.md                       # This file
```

## Prerequisites

- Android Studio (Arctic Fox or later)
- JDK 8 or higher
- Android SDK (API 24+)

## Setup Instructions

### 1. Open in Android Studio

1. Open Android Studio
2. Select "Open an Existing Project"
3. Navigate to `c:\TGDemo\android`
4. Click "OK"

### 2. Configure Server URL

Edit `MainActivity.kt` line 18:

```kotlin
// For Android Emulator (connects to host machine)
private val SERVER_URL = "http://10.0.2.2:5000"

// For Real Device (same WiFi network)
private val SERVER_URL = "http://YOUR_PC_IP:5000"  // Replace with your PC's IP

// For Production
private val SERVER_URL = "https://your-domain.com"
```

**To find your PC's IP:**
```bash
# Windows
ipconfig

# Look for "IPv4 Address" under your active network adapter
# Example: 192.168.1.100
```

### 3. Build the App

#### Option A: Using Android Studio
1. Click "Build" → "Build Bundle(s) / APK(s)" → "Build APK(s)"
2. Wait for build to complete
3. APK will be in `app/build/outputs/apk/debug/`

#### Option B: Using Command Line
```bash
cd c:\TGDemo\android
gradlew assembleDebug
```

### 4. Install on Device

#### Via Android Studio:
1. Connect Android device via USB (enable USB debugging)
2. Click "Run" button (green triangle)
3. Select your device

#### Via APK:
1. Transfer APK to device
2. Enable "Install from Unknown Sources"
3. Open APK file to install

## Running the App

### Development Mode

1. **Start Flask Server** on your PC:
   ```bash
   cd c:\TGDemo\webapp
   python app.py
   ```

2. **Ensure device can reach server:**
   - Emulator: Use `http://10.0.2.2:5000`
   - Real device: Use `http://YOUR_PC_IP:5000` (same WiFi)

3. **Launch Android app**

### Production Mode

1. Deploy Flask server to cloud (Heroku, Railway, etc.)
2. Update `SERVER_URL` to production URL
3. Build release APK
4. Distribute via Play Store or direct download

## Permissions

The app requests the following permissions:

- **INTERNET**: Required to connect to Flask server
- **CAMERA**: Required for face detection
- **RECORD_AUDIO**: Required for voice input
- **ACCESS_NETWORK_STATE**: To check connectivity

All permissions are requested at runtime on first launch.

## JavaScript Bridge

The app includes a JavaScript bridge for native features:

```javascript
// From your web app JavaScript:

// Show native toast
Android.showToast("Hello from web!");

// Get device info
const deviceInfo = JSON.parse(Android.getDeviceInfo());
console.log(deviceInfo.model);  // e.g., "Pixel 6"
```

## Troubleshooting

### App shows "Error loading page"

**Solution:**
- Check Flask server is running
- Verify SERVER_URL is correct
- Check firewall settings
- Ensure device can ping server IP

### Camera not working

**Solution:**
- Grant camera permission when prompted
- Check AndroidManifest.xml has camera permission
- Verify WebView settings allow camera access

### Blank screen

**Solution:**
- Check browser console in WebView (use Android Studio Logcat)
- Verify JavaScript is enabled
- Check for CORS errors in Flask server

### "net::ERR_CLEARTEXT_HTTP_NOT_PERMITTED"

**Solution:**
- Add `android:usesCleartextTraffic="true"` to AndroidManifest.xml (already included)
- Or use HTTPS in production

## Building for Production

### 1. Generate Signing Key

```bash
keytool -genkey -v -keystore face-recognition.keystore -alias face-recognition -keyalg RSA -keysize 2048 -validity 10000
```

### 2. Configure Signing in build.gradle

```gradle
android {
    signingConfigs {
        release {
            storeFile file("face-recognition.keystore")
            storePassword "your-password"
            keyAlias "face-recognition"
            keyPassword "your-password"
        }
    }
    buildTypes {
        release {
            signingConfig signingConfigs.release
            minifyEnabled true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt')
        }
    }
}
```

### 3. Build Release APK

```bash
gradlew assembleRelease
```

## Customization

### Change App Name

Edit `res/values/strings.xml`:
```xml
<string name="app_name">Your App Name</string>
```

### Change App Icon

Replace files in `res/mipmap-*/` directories with your icons.

### Add Splash Screen

Create `SplashActivity.kt` and set as launcher activity.

### Enable Offline Mode

1. Implement Service Worker in web app
2. Cache assets locally
3. Use WebView cache settings

## Next Steps

- [ ] Test on multiple devices
- [ ] Add splash screen
- [ ] Implement offline mode
- [ ] Add app icon
- [ ] Prepare for Play Store submission
- [ ] Add analytics
- [ ] Implement push notifications

## Support

For issues or questions:
1. Check Logcat in Android Studio
2. Verify Flask server logs
3. Test web app in mobile browser first
4. Check WebView console messages

## License

This project is for educational and demonstration purposes.
