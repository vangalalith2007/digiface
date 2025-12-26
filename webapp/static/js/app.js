/**
 * Main Application Logic
 */

// Initialize modules
const camera = new Camera();
const faceDetection = new FaceDetection();
const voiceInput = new VoiceInput();

// State
let currentFaces = [];
let currentImageData = null;
let dataTemplate = null;

// DOM Elements
const startCameraBtn = document.getElementById('start-camera');
const captureBtn = document.getElementById('capture');
const statusEl = document.getElementById('status');
const userCountEl = document.getElementById('user-count');
const modelInfoEl = document.getElementById('model-info');
const detectionResultEl = document.getElementById('detection-result');
const detectionInfoEl = document.getElementById('detection-info');
const recognitionResultEl = document.getElementById('recognition-result');
const recognitionInfoEl = document.getElementById('recognition-info');
const dataFormEl = document.getElementById('data-form');
const userFormEl = document.getElementById('user-form');
const formFieldsEl = document.getElementById('form-fields');
const cancelFormBtn = document.getElementById('cancel-form');
const voiceCollectBtn = document.getElementById('voice-collect');

// Initialize app
async function init() {
    updateStatus('Connecting to server...', false);

    try {
        // Check server status
        const response = await fetch('/api/status');
        const status = await response.json();

        updateStatus('Online', true);
        userCountEl.textContent = `Users: ${status.users_count}`;
        modelInfoEl.textContent = `Model: ${status.model}`;

        // Load data template
        const templateResponse = await fetch('/api/template');
        dataTemplate = await templateResponse.json();

        console.log('App initialized successfully');
    } catch (error) {
        console.error('Error initializing app:', error);
        updateStatus('Offline', false);
    }
}

// Update status indicator
function updateStatus(message, isOnline) {
    statusEl.textContent = `● ${message}`;
    statusEl.className = isOnline ? 'status online' : 'status';
}

// Start camera
startCameraBtn.addEventListener('click', async () => {
    const started = await camera.start();
    if (started) {
        startCameraBtn.disabled = true;
        captureBtn.disabled = false;
        updateStatus('Camera active', true);
    }
});

// Capture and process frame
captureBtn.addEventListener('click', async () => {
    try {
        captureBtn.disabled = true;
        captureBtn.textContent = '⏳ Processing...';
        captureBtn.classList.add('processing');

        // Capture frame
        currentImageData = camera.captureFrame();

        // Detect faces
        const result = await faceDetection.detectFaces(currentImageData);

        if (result.success && result.faces.length > 0) {
            currentFaces = result.faces;

            // Draw face boxes
            faceDetection.drawFaceBoxes(result.faces, camera.getVideoDimensions());

            // Show detection result
            showDetectionResult(result.faces[0]);

            // Try to recognize face
            await recognizeFace(result.faces[0]);
        } else {
            alert('No face detected. Please try again.');
            faceDetection.clearOverlay();
        }

    } catch (error) {
        console.error('Error processing frame:', error);
        alert('Error processing image. Please try again.');
    } finally {
        captureBtn.disabled = false;
        captureBtn.textContent = '✓ Capture';
        captureBtn.classList.remove('processing');
    }
});

// Show detection result
function showDetectionResult(face) {
    detectionInfoEl.innerHTML = `
        <div class="info-row">
            <span class="info-label">Gender:</span>
            <span class="info-value">${face.gender}</span>
        </div>
        <div class="info-row">
            <span class="info-label">Confidence:</span>
            <span class="info-value">${Math.round(face.confidence * 100)}%</span>
        </div>
        <div class="info-row">
            <span class="info-label">Position:</span>
            <span class="info-value">x:${face.x}, y:${face.y}</span>
        </div>
    `;
    detectionResultEl.style.display = 'block';
}

// Recognize face
async function recognizeFace(face) {
    try {
        const result = await faceDetection.recognizeFace(currentImageData, face);

        if (result.recognized) {
            // Known user
            showRecognitionResult(result.user, true);
            dataFormEl.style.display = 'none';
        } else {
            // New user - show registration form
            showRecognitionResult(null, false);
            showRegistrationForm(face);
        }
    } catch (error) {
        console.error('Error recognizing face:', error);
    }
}

// Show recognition result
function showRecognitionResult(user, recognized) {
    if (recognized && user) {
        recognitionInfoEl.innerHTML = `
            <div class="info-row">
                <span class="info-label">Status:</span>
                <span class="info-value text-success">✓ Recognized</span>
            </div>
            <div class="info-row">
                <span class="info-label">Name:</span>
                <span class="info-value">${user.data.name || 'N/A'}</span>
            </div>
            <div class="info-row">
                <span class="info-label">Age:</span>
                <span class="info-value">${user.data.age || 'N/A'}</span>
            </div>
            <div class="info-row">
                <span class="info-label">City:</span>
                <span class="info-value">${user.data.city || 'N/A'}</span>
            </div>
            <div class="info-row">
                <span class="info-label">Registered:</span>
                <span class="info-value text-muted">${new Date(user.timestamp).toLocaleString()}</span>
            </div>
        `;
    } else {
        recognitionInfoEl.innerHTML = `
            <div class="info-row">
                <span class="info-label">Status:</span>
                <span class="info-value text-danger">✗ New Face</span>
            </div>
            <p class="text-muted" style="margin-top: 10px;">Please fill in the registration form below or use voice collection.</p>
        `;
    }
    recognitionResultEl.style.display = 'block';
}

// Show registration form
function showRegistrationForm(face) {
    // Generate form fields from template
    formFieldsEl.innerHTML = '';

    if (dataTemplate && dataTemplate.fields) {
        dataTemplate.fields.forEach(field => {
            const formGroup = document.createElement('div');
            formGroup.className = 'form-group';

            const label = document.createElement('label');
            label.textContent = field.prompt || field.name;
            label.setAttribute('for', field.name);

            const input = document.createElement('input');
            input.type = field.type === 'integer' ? 'number' : 'text';
            input.id = field.name;
            input.name = field.name;
            input.required = true;
            input.placeholder = `Enter ${field.name}`;

            formGroup.appendChild(label);
            formGroup.appendChild(input);
            formFieldsEl.appendChild(formGroup);
        });
    }

    // Store face data for registration
    userFormEl.dataset.face = JSON.stringify(face);

    dataFormEl.style.display = 'block';
}

// Voice collection handler
voiceCollectBtn.addEventListener('click', async () => {
    try {
        voiceCollectBtn.disabled = true;
        voiceCollectBtn.textContent = '🎤 Listening...';
        voiceCollectBtn.classList.add('processing');

        // Collect data via voice
        const voiceData = await voiceInput.collectAllData(dataTemplate.fields);

        if (voiceData) {
            // Fill form with voice data
            for (const [key, value] of Object.entries(voiceData)) {
                const input = document.getElementById(key);
                if (input) {
                    input.value = value;
                }
            }

            // Show success message
            await voiceInput.speak('Data collected successfully. Please review and save.');
        } else {
            // User cancelled
            await voiceInput.speak('Data collection cancelled.');
        }

    } catch (error) {
        console.error('Error during voice collection:', error);
        alert('Voice collection error. Please use manual input or try again.');
    } finally {
        voiceCollectBtn.disabled = false;
        voiceCollectBtn.textContent = '🎤 Collect via Voice';
        voiceCollectBtn.classList.remove('processing');
    }
});

// Handle form submission
userFormEl.addEventListener('submit', async (e) => {
    e.preventDefault();

    try {
        // Collect form data
        const formData = new FormData(userFormEl);
        const userData = {};

        for (let [key, value] of formData.entries()) {
            userData[key] = value;
        }

        // Get face data
        const face = JSON.parse(userFormEl.dataset.face);
        face.gender = currentFaces[0].gender;

        // Register user
        const result = await faceDetection.registerUser(currentImageData, face, userData);

        if (result.success) {
            alert(`User registered successfully! ID: ${result.user_id}`);

            // Update user count
            const statusResponse = await fetch('/api/status');
            const status = await statusResponse.json();
            userCountEl.textContent = `Users: ${status.users_count}`;

            // Reset form
            userFormEl.reset();
            dataFormEl.style.display = 'none';
            faceDetection.clearOverlay();
        }
    } catch (error) {
        console.error('Error registering user:', error);
        alert('Error registering user. Please try again.');
    }
});

// Cancel form
cancelFormBtn.addEventListener('click', () => {
    userFormEl.reset();
    dataFormEl.style.display = 'none';
    faceDetection.clearOverlay();
});

// Initialize on page load
document.addEventListener('DOMContentLoaded', init);
