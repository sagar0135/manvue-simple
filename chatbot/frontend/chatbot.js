// ManVue Chatbot JavaScript

class ManVueChatbot {
    constructor() {
        this.isOpen = false;
        this.isMinimized = false;
        this.websocket = null;
        this.recognition = null;
        this.isListening = false;
        this.messageQueue = [];
        this.isProcessing = false;
        this.sessionId = this.generateSessionId();
        
        this.init();
        this.setupEventListeners();
        this.setupVoiceRecognition();
        this.connectWebSocket();
    }

    init() {
        // Get DOM elements
        this.elements = {
            toggle: document.getElementById('chatbot-toggle'),
            container: document.getElementById('chatbot-container'),
            minimizeBtn: document.getElementById('minimize-btn'),
            closeBtn: document.getElementById('close-btn'),
            messagesContainer: document.getElementById('chat-messages'),
            messageInput: document.getElementById('message-input'),
            sendBtn: document.getElementById('send-btn'),
            voiceBtn: document.getElementById('voice-btn'),
            typingIndicator: document.getElementById('typing-indicator'),
            quickActions: document.getElementById('quick-actions'),
            notificationBadge: document.getElementById('notification-badge'),
            voiceFeedback: document.getElementById('voice-feedback'),
            voiceStop: document.getElementById('voice-stop'),
            charCount: document.getElementById('char-count')
        };

        // Initialize character counter
        this.updateCharCounter();
        
        // Hide notification badge initially
        this.hideNotificationBadge();
    }

    setupEventListeners() {
        // Toggle chatbot
        this.elements.toggle.addEventListener('click', () => this.toggleChatbot());
        
        // Header actions
        this.elements.minimizeBtn.addEventListener('click', () => this.minimizeChatbot());
        this.elements.closeBtn.addEventListener('click', () => this.closeChatbot());
        
        // Message input
        this.elements.messageInput.addEventListener('keydown', (e) => this.handleKeyDown(e));
        this.elements.messageInput.addEventListener('input', () => this.handleInputChange());
        this.elements.sendBtn.addEventListener('click', () => this.sendMessage());
        
        // Voice recognition
        this.elements.voiceBtn.addEventListener('click', () => this.toggleVoiceRecognition());
        this.elements.voiceStop.addEventListener('click', () => this.stopVoiceRecognition());
        
        // Quick actions
        this.elements.quickActions.addEventListener('click', (e) => this.handleQuickAction(e));
        
        // Auto-resize textarea
        this.elements.messageInput.addEventListener('input', () => this.autoResizeTextarea());
        
        // Click outside to close (mobile)
        document.addEventListener('click', (e) => this.handleOutsideClick(e));
    }

    setupVoiceRecognition() {
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            this.recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            this.recognition.continuous = false;
            this.recognition.interimResults = true;
            this.recognition.lang = 'en-US';

            this.recognition.onstart = () => {
                this.isListening = true;
                this.showVoiceFeedback();
                this.elements.voiceBtn.innerHTML = '<i class="fas fa-stop"></i>';
            };

            this.recognition.onresult = (event) => {
                const transcript = Array.from(event.results)
                    .map(result => result[0].transcript)
                    .join('');
                
                document.getElementById('voice-text').textContent = transcript;
                
                if (event.results[event.results.length - 1].isFinal) {
                    this.elements.messageInput.value = transcript;
                    this.updateCharCounter();
                    this.stopVoiceRecognition();
                    
                    // Auto-send if transcript is complete
                    if (transcript.trim()) {
                        setTimeout(() => this.sendMessage(), 500);
                    }
                }
            };

            this.recognition.onerror = (event) => {
                console.error('Speech recognition error:', event.error);
                this.stopVoiceRecognition();
                this.showMessage('Sorry, I couldn\'t understand that. Please try typing instead.', 'bot');
            };

            this.recognition.onend = () => {
                this.stopVoiceRecognition();
            };
        } else {
            // Hide voice button if not supported
            this.elements.voiceBtn.style.display = 'none';
        }
    }


    connectWebSocket() {
        try {
            // Connect to Rasa action server via WebSocket
            this.websocket = new WebSocket('ws://localhost:5055/ws');
            
            this.websocket.onopen = () => {
                console.log('Connected to ManVue chatbot server');
            };
            
            this.websocket.onmessage = (event) => {
                const data = JSON.parse(event.data);
                this.handleBotResponse(data);
            };
            
            this.websocket.onerror = (error) => {
                console.error('WebSocket error:', error);
                this.handleOfflineMode();
            };
            
            this.websocket.onclose = () => {
                console.log('Disconnected from chatbot server');
                // Try to reconnect after 3 seconds
                setTimeout(() => this.connectWebSocket(), 3000);
            };
        } catch (error) {
            console.error('Failed to connect to chatbot server:', error);
            this.handleOfflineMode();
        }
    }

    handleOfflineMode() {
        // Fallback to HTTP API when WebSocket is unavailable
        console.log('Switching to HTTP API mode');
    }

    toggleChatbot() {
        if (this.isOpen) {
            this.closeChatbot();
        } else {
            this.openChatbot();
        }
    }

    openChatbot() {
        this.isOpen = true;
        this.isMinimized = false;
        this.elements.container.classList.add('open');
        this.elements.container.classList.remove('minimized');
        this.elements.toggle.style.display = 'none';
        this.hideNotificationBadge();
        this.elements.messageInput.focus();
        this.scrollToBottom();
    }

    closeChatbot() {
        this.isOpen = false;
        this.isMinimized = false;
        this.elements.container.classList.remove('open', 'minimized');
        this.elements.toggle.style.display = 'flex';
        this.stopVoiceRecognition();
    }

    minimizeChatbot() {
        this.isMinimized = !this.isMinimized;
        this.elements.container.classList.toggle('minimized');
        
        if (!this.isMinimized) {
            this.elements.messageInput.focus();
        }
    }

    handleKeyDown(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            this.sendMessage();
        }
    }

    handleInputChange() {
        this.updateCharCounter();
        this.updateSendButton();
    }

    updateCharCounter() {
        const length = this.elements.messageInput.value.length;
        this.elements.charCount.textContent = `${length}/500`;
        
        if (length > 450) {
            this.elements.charCount.style.color = '#e74c3c';
        } else {
            this.elements.charCount.style.color = '#7f8c8d';
        }
    }

    updateSendButton() {
        const hasText = this.elements.messageInput.value.trim().length > 0;
        this.elements.sendBtn.classList.toggle('active', hasText);
        this.elements.sendBtn.disabled = !hasText || this.isProcessing;
    }

    autoResizeTextarea() {
        const textarea = this.elements.messageInput;
        textarea.style.height = 'auto';
        textarea.style.height = Math.min(textarea.scrollHeight, 80) + 'px';
    }

    handleQuickAction(e) {
        const button = e.target.closest('.quick-action-btn');
        if (button) {
            const message = button.dataset.message;
            if (message) {
                this.elements.messageInput.value = message;
                this.updateCharCounter();
                this.sendMessage();
            }
        }
    }

    handleOutsideClick(e) {
        if (window.innerWidth <= 768 && this.isOpen && 
            !this.elements.container.contains(e.target) && 
            !this.elements.toggle.contains(e.target)) {
            this.closeChatbot();
        }
    }

    async sendMessage() {
        const message = this.elements.messageInput.value.trim();
        if (!message || this.isProcessing) return;

        this.isProcessing = true;
        this.elements.messageInput.value = '';
        this.updateCharCounter();
        this.updateSendButton();
        this.autoResizeTextarea();

        // Show user message
        this.showMessage(message, 'user');
        
        // Show typing indicator
        this.showTypingIndicator();

        try {
            if (this.websocket && this.websocket.readyState === WebSocket.OPEN) {
                // Send via WebSocket
                this.websocket.send(JSON.stringify({
                    message: message,
                    sender: this.sessionId
                }));
            } else {
                // Fallback to HTTP API
                await this.sendMessageHTTP(message);
            }
        } catch (error) {
            console.error('Error sending message:', error);
            this.hideTypingIndicator();
            this.showMessage('Sorry, I\'m having trouble connecting. Please try again.', 'bot');
        }

        this.isProcessing = false;
    }

    async sendMessageHTTP(message) {
        try {
            const response = await fetch('http://localhost:5005/webhooks/rest/webhook', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    sender: this.sessionId
                })
            });

            if (response.ok) {
                const data = await response.json();
                this.handleBotResponse(data);
            } else {
                throw new Error('Failed to get response');
            }
        } catch (error) {
            this.hideTypingIndicator();
            this.showMessage('I\'m currently offline. Please try again later or browse our website directly.', 'bot');
        }
    }

    handleBotResponse(responses) {
        this.hideTypingIndicator();
        
        if (Array.isArray(responses)) {
            responses.forEach((response, index) => {
                setTimeout(() => {
                    if (response.text) {
                        this.showMessage(response.text, 'bot');
                    }
                    if (response.image) {
                        this.showImage(response.image, 'bot');
                    }
                    if (response.buttons) {
                        this.showButtons(response.buttons);
                    }
                }, index * 800); // Stagger multiple responses
            });
        } else if (responses.text) {
            this.showMessage(responses.text, 'bot');
        }
    }

    showMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.innerHTML = sender === 'bot' ? '<i class="fas fa-robot"></i>' : '<i class="fas fa-user"></i>';
        
        const content = document.createElement('div');
        content.className = 'message-content';
        
        const bubble = document.createElement('div');
        bubble.className = 'message-bubble';
        bubble.innerHTML = this.formatMessage(text);
        
        const time = document.createElement('div');
        time.className = 'message-time';
        time.textContent = this.getCurrentTime();
        
        content.appendChild(bubble);
        content.appendChild(time);
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(content);
        
        this.elements.messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();
        
        // Show notification if chatbot is closed
        if (!this.isOpen) {
            this.showNotificationBadge();
        }
    }

    showImage(imageUrl, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.innerHTML = '<i class="fas fa-robot"></i>';
        
        const content = document.createElement('div');
        content.className = 'message-content';
        
        const bubble = document.createElement('div');
        bubble.className = 'message-bubble';
        
        const img = document.createElement('img');
        img.src = imageUrl;
        img.style.maxWidth = '100%';
        img.style.borderRadius = '8px';
        
        bubble.appendChild(img);
        
        const time = document.createElement('div');
        time.className = 'message-time';
        time.textContent = this.getCurrentTime();
        
        content.appendChild(bubble);
        content.appendChild(time);
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(content);
        
        this.elements.messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();
    }

    showButtons(buttons) {
        const buttonsDiv = document.createElement('div');
        buttonsDiv.className = 'message-buttons';
        buttonsDiv.style.cssText = 'margin: 10px 0; display: flex; flex-wrap: wrap; gap: 8px;';
        
        buttons.forEach(button => {
            const btn = document.createElement('button');
            btn.textContent = button.title;
            btn.style.cssText = 'background: #3498db; color: white; border: none; padding: 8px 16px; border-radius: 20px; cursor: pointer; font-size: 12px;';
            btn.onclick = () => {
                this.elements.messageInput.value = button.payload || button.title;
                this.sendMessage();
            };
            buttonsDiv.appendChild(btn);
        });
        
        this.elements.messagesContainer.appendChild(buttonsDiv);
        this.scrollToBottom();
    }

    formatMessage(text) {
        // Convert markdown-style formatting to HTML
        return text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/\n/g, '<br>')
            .replace(/•/g, '•');
    }

    showTypingIndicator() {
        this.elements.typingIndicator.classList.add('show');
        this.scrollToBottom();
    }

    hideTypingIndicator() {
        this.elements.typingIndicator.classList.remove('show');
    }

    toggleVoiceRecognition() {
        if (this.isListening) {
            this.stopVoiceRecognition();
        } else {
            this.startVoiceRecognition();
        }
    }

    startVoiceRecognition() {
        if (this.recognition) {
            this.recognition.start();
        }
    }

    stopVoiceRecognition() {
        if (this.recognition) {
            this.recognition.stop();
        }
        this.isListening = false;
        this.hideVoiceFeedback();
        this.elements.voiceBtn.innerHTML = '<i class="fas fa-microphone"></i>';
    }

    showVoiceFeedback() {
        this.elements.voiceFeedback.classList.add('show');
        document.getElementById('voice-text').textContent = 'Listening...';
    }

    hideVoiceFeedback() {
        this.elements.voiceFeedback.classList.remove('show');
    }

    showNotificationBadge() {
        this.elements.notificationBadge.style.display = 'flex';
    }

    hideNotificationBadge() {
        this.elements.notificationBadge.style.display = 'none';
    }

    scrollToBottom() {
        setTimeout(() => {
            this.elements.messagesContainer.scrollTop = this.elements.messagesContainer.scrollHeight;
        }, 100);
    }

    getCurrentTime() {
        return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }

    generateSessionId() {
        return 'session_' + Math.random().toString(36).substr(2, 9) + '_' + Date.now();
    }
}

// Initialize chatbot when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.manvueChatbot = new ManVueChatbot();
});

// Export for external access
window.ManVueChatbot = ManVueChatbot;

