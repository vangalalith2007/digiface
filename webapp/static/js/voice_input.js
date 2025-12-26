/**
 * Voice Input Module
 * Handles speech recognition and text-to-speech for data collection
 */

class VoiceInput {
    constructor() {
        this.recognition = null;
        this.synthesis = window.speechSynthesis;
        this.isListening = false;
        this.initRecognition();
    }

    initRecognition() {
        // Check for browser support
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

        if (!SpeechRecognition) {
            console.error('Speech recognition not supported in this browser');
            return;
        }

        this.recognition = new SpeechRecognition();
        this.recognition.continuous = false;
        this.recognition.interimResults = false;
        this.recognition.lang = 'en-US';
        this.recognition.maxAlternatives = 1;
    }

    speak(text) {
        return new Promise((resolve) => {
            if (!this.synthesis) {
                console.error('Speech synthesis not supported');
                resolve();
                return;
            }

            // Cancel any ongoing speech
            this.synthesis.cancel();

            const utterance = new SpeechSynthesisUtterance(text);
            utterance.rate = 0.9;
            utterance.pitch = 1.0;
            utterance.volume = 1.0;

            utterance.onend = () => resolve();
            utterance.onerror = () => resolve();

            this.synthesis.speak(utterance);
        });
    }

    listen() {
        return new Promise((resolve, reject) => {
            if (!this.recognition) {
                reject(new Error('Speech recognition not available'));
                return;
            }

            this.isListening = true;

            this.recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                console.log('Recognized:', transcript);
                this.isListening = false;
                resolve(transcript);
            };

            this.recognition.onerror = (event) => {
                console.error('Speech recognition error:', event.error);
                this.isListening = false;
                reject(new Error(event.error));
            };

            this.recognition.onend = () => {
                this.isListening = false;
            };

            try {
                this.recognition.start();
            } catch (error) {
                this.isListening = false;
                reject(error);
            }
        });
    }

    async collectFieldData(field, maxRetries = 3) {
        const fieldName = field.name || 'unknown';
        const prompt = field.prompt || `Please provide ${fieldName}`;
        const fieldType = field.type || 'string';

        for (let attempt = 0; attempt < maxRetries; attempt++) {
            try {
                // Speak the prompt
                await this.speak(prompt);

                // Wait a bit before listening
                await new Promise(resolve => setTimeout(resolve, 500));

                // Listen for response
                const response = await this.listen();

                // Check for abort commands
                if (this.isAbortCommand(response)) {
                    await this.speak('Data collection cancelled');
                    return 'ABORT';
                }

                // Validate response
                if (this.validateResponse(response, fieldType)) {
                    return response;
                } else {
                    if (attempt < maxRetries - 1) {
                        await this.speak(`Invalid ${fieldType}. Please try again.`);
                    }
                }
            } catch (error) {
                console.error(`Error collecting ${fieldName}:`, error);
                if (attempt < maxRetries - 1) {
                    await this.speak("I didn't catch that. Please repeat.");
                }
            }
        }

        console.log(`Failed to collect data for field: ${fieldName}`);
        return null;
    }

    isAbortCommand(text) {
        if (!text) return false;
        const textLower = text.toLowerCase().trim();
        const abortKeywords = ['stop', 'quit', 'exit', 'cancel', 'abort'];
        return abortKeywords.some(keyword => textLower.includes(keyword));
    }

    validateResponse(response, fieldType) {
        if (!response || response.trim() === '') {
            return false;
        }

        switch (fieldType) {
            case 'integer':
                return /\d+/.test(response);
            case 'string':
                return response.length > 0;
            default:
                return true;
        }
    }

    async collectAllData(fields) {
        await this.speak('Please answer the following questions. You can say stop or quit at any time to cancel.');

        const collectedData = {};

        for (const field of fields) {
            const fieldName = field.name;
            const fieldType = field.type || 'string';

            const response = await this.collectFieldData(field);

            // Check if user aborted
            if (response === 'ABORT') {
                await this.speak('Data collection cancelled');
                return null;
            }

            if (response) {
                // Process response based on type
                if (fieldType === 'integer') {
                    // Extract digits
                    const digits = response.match(/\d+/);
                    collectedData[fieldName] = digits ? digits[0] : response;
                } else {
                    collectedData[fieldName] = response;
                }
            } else {
                // Mark as not provided
                collectedData[fieldName] = 'Not provided';
            }
        }

        await this.speak('Thank you. Data collection complete.');
        return collectedData;
    }

    stopListening() {
        if (this.recognition && this.isListening) {
            this.recognition.stop();
        }
    }

    stopSpeaking() {
        if (this.synthesis) {
            this.synthesis.cancel();
        }
    }
}

// Export for use in other modules
window.VoiceInput = VoiceInput;
