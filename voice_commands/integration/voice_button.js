/**
 * Voice Button Integration for ManVue
 * 
 * Adds a floating voice button to the ManVue interface
 */

class VoiceButton {
    constructor() {
        this.button = null;
        this.isListening = false;
        this.init();
    }
    
    init() {
        // Only create button if no other voice button exists
        if (!document.querySelector('.voice-btn')) {
            this.createButton();
            this.attachEventListeners();
            console.log('Voice button initialized');
        } else {
            console.log('Voice button already exists, skipping creation');
        }
    }
    
    createButton() {
        // Create voice button HTML
        const buttonHTML = `
            <div id="voice-button-container" class="voice-button-container">
                <button id="voice-button" class="voice-button" title="Click to use voice commands">
                    <svg class="voice-icon" viewBox="0 0 24 24" width="24" height="24">
                        <path fill="currentColor" d="M12 1c-1.6 0-3 1.4-3 3v8c0 1.6 1.4 3 3 3s3-1.4 3-3V4c0-1.6-1.4-3-3-3z"/>
                        <path fill="currentColor" d="M19 10v2c0 3.9-3.1 7-7 7s-7-3.1-7-7v-2"/>
                        <path fill="currentColor" d="M12 19v4"/>
                        <path fill="currentColor" d="M8 23h8"/>
                    </svg>
                    <div class="pulse-ring"></div>
                </button>
                <div id="voice-status" class="voice-status hidden">Ready</div>
            </div>
        `;
        
        // Add CSS styles
        const styles = `
            <style>
                .voice-button-container {
                    position: fixed;
                    bottom: 20px;
                    right: 20px;
                    z-index: 10000;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                }
                
                .voice-button {
                    width: 60px;
                    height: 60px;
                    border-radius: 50%;
                    border: none;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
                    transition: all 0.3s ease;
                    position: relative;
                    outline: none;
                }
                
                .voice-button:hover {
                    transform: scale(1.05);
                    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
                }
                
                .voice-button:active {
                    transform: scale(0.95);
                }
                
                .voice-button.listening {
                    background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
                    animation: pulse 1.5s infinite;
                }
                
                .voice-button.listening .pulse-ring {
                    animation: pulse-ring 1.5s cubic-bezier(0.215, 0.61, 0.355, 1) infinite;
                }
                
                .voice-icon {
                    width: 24px;
                    height: 24px;
                }
                
                .pulse-ring {
                    position: absolute;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    width: 60px;
                    height: 60px;
                    border: 2px solid currentColor;
                    border-radius: 50%;
                    opacity: 0;
                }
                
                .voice-status {
                    margin-top: 8px;
                    background: rgba(0, 0, 0, 0.8);
                    color: white;
                    padding: 4px 8px;
                    border-radius: 12px;
                    font-size: 12px;
                    white-space: nowrap;
                    transition: opacity 0.3s ease;
                }
                
                .voice-status.hidden {
                    opacity: 0;
                    pointer-events: none;
                }
                
                @keyframes pulse {
                    0% { transform: scale(1); }
                    50% { transform: scale(1.05); }
                    100% { transform: scale(1); }
                }
                
                @keyframes pulse-ring {
                    0% {
                        transform: translate(-50%, -50%) scale(0.8);
                        opacity: 1;
                    }
                    100% {
                        transform: translate(-50%, -50%) scale(2);
                        opacity: 0;
                    }
                }
                
                @media (max-width: 768px) {
                    .voice-button-container {
                        bottom: 80px;
                        right: 15px;
                    }
                    
                    .voice-button {
                        width: 50px;
                        height: 50px;
                    }
                    
                    .voice-icon {
                        width: 20px;
                        height: 20px;
                    }
                }
            </style>
        `;
        
        // Add styles to head
        document.head.insertAdjacentHTML('beforeend', styles);
        
        // Add button to body
        document.body.insertAdjacentHTML('beforeend', buttonHTML);
        
        this.button = document.getElementById('voice-button');
        this.statusElement = document.getElementById('voice-status');
    }
    
    attachEventListeners() {
        if (!this.button) return;
        
        // Button click handler
        this.button.addEventListener('click', () => {
            this.toggleVoiceRecognition();
        });
        
        // Keyboard shortcut (Ctrl+Shift+V)
        document.addEventListener('keydown', (event) => {
            if (event.ctrlKey && event.shiftKey && event.code === 'KeyV') {
                event.preventDefault();
                this.toggleVoiceRecognition();
            }
        });
        
        // Listen for voice integration events
        document.addEventListener('voiceStarted', () => {
            this.setListeningState(true);
        });
        
        document.addEventListener('voiceStopped', () => {
            this.setListeningState(false);
        });
    }
    
    toggleVoiceRecognition() {
        if (!window.manvueVoiceIntegration) {
            this.showStatus('Voice not available', 'error');
            return;
        }
        
        if (this.isListening) {
            this.stopListening();
        } else {
            this.startListening();
        }
    }
    
    startListening() {
        if (window.manvueVoiceIntegration && window.manvueVoiceIntegration.startListening()) {
            this.setListeningState(true);
            this.showStatus('Listening...', 'listening');
        } else {
            this.showStatus('Voice not available', 'error');
        }
    }
    
    stopListening() {
        if (window.manvueVoiceIntegration && window.manvueVoiceIntegration.stopListening()) {
            this.setListeningState(false);
            this.showStatus('Voice stopped', 'stopped');
        }
    }
    
    setListeningState(listening) {
        this.isListening = listening;
        
        if (this.button) {
            if (listening) {
                this.button.classList.add('listening');
                this.button.title = 'Click to stop voice commands';
            } else {
                this.button.classList.remove('listening');
                this.button.title = 'Click to use voice commands';
            }
        }
    }
    
    showStatus(message, type = 'info') {
        if (!this.statusElement) return;
        
        this.statusElement.textContent = message;
        this.statusElement.classList.remove('hidden');
        
        // Auto-hide after 3 seconds
        setTimeout(() => {
            if (this.statusElement && this.statusElement.textContent === message) {
                this.statusElement.classList.add('hidden');
            }
        }, 3000);
    }
    
    hide() {
        const container = document.getElementById('voice-button-container');
        if (container) {
            container.style.display = 'none';
        }
    }
    
    show() {
        const container = document.getElementById('voice-button-container');
        if (container) {
            container.style.display = 'flex';
        }
    }
    
    destroy() {
        const container = document.getElementById('voice-button-container');
        if (container) {
            container.remove();
        }
    }
}

// Initialize voice button when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Wait for other scripts to load
    setTimeout(() => {
        if (!document.getElementById('voice-button-container')) {
            window.manvueVoiceButton = new VoiceButton();
        }
    }, 1500);
});

// Export for use in other modules
window.VoiceButton = VoiceButton;
