/**
 * Camera Module
 * Handles webcam access and frame capture
 */

class Camera {
    constructor() {
        this.video = document.getElementById('video');
        this.canvas = document.getElementById('canvas');
        this.ctx = this.canvas.getContext('2d');
        this.stream = null;
        this.isActive = false;
    }

    async start() {
        try {
            this.stream = await navigator.mediaDevices.getUserMedia({
                video: {
                    facingMode: 'user',
                    width: { ideal: 640 },
                    height: { ideal: 480 }
                }
            });

            this.video.srcObject = this.stream;
            this.isActive = true;

            // Wait for video to be ready
            await new Promise((resolve) => {
                this.video.onloadedmetadata = () => {
                    this.canvas.width = this.video.videoWidth;
                    this.canvas.height = this.video.videoHeight;
                    resolve();
                };
            });

            console.log('Camera started successfully');
            return true;
        } catch (error) {
            console.error('Error accessing camera:', error);
            alert('Could not access camera. Please check permissions.');
            return false;
        }
    }

    stop() {
        if (this.stream) {
            this.stream.getTracks().forEach(track => track.stop());
            this.video.srcObject = null;
            this.isActive = false;
            console.log('Camera stopped');
        }
    }

    captureFrame() {
        if (!this.isActive) {
            console.error('Camera is not active');
            return null;
        }

        // Draw current video frame to canvas
        this.ctx.drawImage(this.video, 0, 0, this.canvas.width, this.canvas.height);

        // Get image as base64
        const imageData = this.canvas.toDataURL('image/jpeg', 0.8);
        return imageData;
    }

    getVideoDimensions() {
        return {
            width: this.video.videoWidth,
            height: this.video.videoHeight
        };
    }
}

// Export for use in other modules
window.Camera = Camera;
