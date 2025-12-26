/**
 * Face Detection Module
 * Handles communication with face detection API
 */

class FaceDetection {
    constructor(apiBaseUrl = '') {
        this.apiBaseUrl = apiBaseUrl;
        this.overlay = document.getElementById('face-overlay');
    }

    async detectFaces(imageData) {
        try {
            const response = await fetch(`${this.apiBaseUrl}/api/face/detect`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ image: imageData })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            return result;
        } catch (error) {
            console.error('Error detecting faces:', error);
            throw error;
        }
    }

    async recognizeFace(imageData, face) {
        try {
            const response = await fetch(`${this.apiBaseUrl}/api/face/recognize`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    image: imageData,
                    face: face
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            return result;
        } catch (error) {
            console.error('Error recognizing face:', error);
            throw error;
        }
    }

    async registerUser(imageData, face, userData) {
        try {
            const response = await fetch(`${this.apiBaseUrl}/api/face/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    image: imageData,
                    face: face,
                    userData: userData
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            return result;
        } catch (error) {
            console.error('Error registering user:', error);
            throw error;
        }
    }

    drawFaceBoxes(faces, videoDimensions) {
        // Clear previous boxes
        this.overlay.innerHTML = '';

        if (!faces || faces.length === 0) {
            return;
        }

        // Calculate scale factors
        const scaleX = this.overlay.clientWidth / videoDimensions.width;
        const scaleY = this.overlay.clientHeight / videoDimensions.height;

        faces.forEach((face, index) => {
            // Create face box
            const box = document.createElement('div');
            box.className = 'face-box';
            box.style.left = `${face.x * scaleX}px`;
            box.style.top = `${face.y * scaleY}px`;
            box.style.width = `${face.w * scaleX}px`;
            box.style.height = `${face.h * scaleY}px`;

            // Create label
            const label = document.createElement('div');
            label.className = 'face-label';
            label.textContent = `${face.gender || 'Unknown'} (${Math.round(face.confidence * 100)}%)`;
            box.appendChild(label);

            this.overlay.appendChild(box);
        });
    }

    clearOverlay() {
        this.overlay.innerHTML = '';
    }
}

// Export for use in other modules
window.FaceDetection = FaceDetection;
