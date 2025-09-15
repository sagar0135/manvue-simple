/**
 * Enhanced ManVue Chatbot Integration
 * Integrates chatbot with product display and cart functionality
 */

class EnhancedManVueChatbot {
    constructor() {
        this.isOpen = false;
        this.isMinimized = false;
        this.websocket = null;
        this.recognition = null;
        this.isListening = false;
        this.messageQueue = [];
        this.isProcessing = false;
        this.sessionId = this.generateSessionId();
        this.products = [];
        this.currentSearchResults = [];
        
        this.init();
        this.setupEventListeners();
        this.setupVoiceRecognition();
        this.connectWebSocket();
        this.loadProducts();
    }

    init() {
        // Get DOM elements
        this.elements = {
            toggle: document.getElementById('chatbot-toggle'),
            container: document.getElementById('chatbot-container'),
            messagesContainer: document.getElementById('chatbot-messages'),
            messageInput: document.getElementById('chatbot-input'),
            sendBtn: document.getElementById('chatbot-send'),
            voiceBtn: document.getElementById('chatbot-voice'),
            voiceFeedback: document.getElementById('voice-feedback'),
            quickActions: document.getElementById('quick-actions'),
            charCounter: document.getElementById('char-counter')
        };

        // Initialize character counter
        this.updateCharCounter();
        
        // Hide notification badge initially
        this.hideNotificationBadge();
    }

    setupEventListeners() {
        // Toggle chatbot
        this.elements.toggle.addEventListener('click', () => this.toggleChatbot());
        
        // Send message
        this.elements.sendBtn.addEventListener('click', () => this.sendMessage());
        this.elements.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Voice recognition
        this.elements.voiceBtn.addEventListener('click', () => this.toggleVoiceRecognition());
        
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
            // Connect to chatbot server via WebSocket
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
            if (this.isMinimized) {
                this.openChatbot();
            } else {
                this.minimizeChatbot();
            }
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
        
        // Show welcome message if first time
        if (this.elements.messagesContainer.children.length <= 1) {
            this.showMessage('👋 Welcome! I can help you find products, answer questions, and assist with your shopping. Try saying "Search for blue shirts" or ask me anything!', 'bot');
        }
    }

    closeChatbot() {
        this.isOpen = false;
        this.isMinimized = false;
        this.elements.container.classList.remove('open', 'minimized');
        this.elements.toggle.style.display = 'block';
    }

    minimizeChatbot() {
        this.isMinimized = true;
        this.elements.container.classList.add('minimized');
        this.elements.toggle.style.display = 'block';
    }

    async sendMessage() {
        const message = this.elements.messageInput.value.trim();
        if (!message || this.isProcessing) return;

        this.isProcessing = true;
        this.elements.messageInput.value = '';
        this.updateCharCounter();
        this.autoResizeTextarea();

        // Add user message to chat
        this.showMessage(message, 'user');
        this.scrollToBottom();

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
                // Fallback to HTTP
                await this.sendMessageHTTP(message);
            }
        } catch (error) {
            console.error('Error sending message:', error);
            this.hideTypingIndicator();
            this.showMessage('Sorry, I encountered an error. Please try again.', 'bot');
        }

        this.isProcessing = false;
    }

    async sendMessageHTTP(message) {
        try {
            const response = await fetch('http://localhost:5055/chat', {
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
                this.handleBotResponse(data.responses);
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
            responses.forEach(response => {
                if (response.text) {
                    this.showMessage(response.text, 'bot');
                } else if (response.custom) {
                    this.handleCustomResponse(response.custom);
                }
            });
        } else if (responses.text) {
            this.showMessage(responses.text, 'bot');
        } else if (responses.custom) {
            this.handleCustomResponse(responses.custom);
        }
        
        this.scrollToBottom();
    }

    handleCustomResponse(custom) {
        if (custom.type === 'product_search') {
            this.handleProductSearch(custom);
        } else if (custom.type === 'product_recommendation') {
            this.handleProductRecommendation(custom);
        } else if (custom.type === 'cart_action') {
            this.handleCartAction(custom);
        } else if (custom.type === 'quick_reply') {
            this.handleQuickReply(custom);
        }
    }

    handleProductSearch(custom) {
        const { query, products, filters } = custom;
        
        if (products && products.length > 0) {
            this.currentSearchResults = products;
            
            let message = `Found ${products.length} products for "${query}":\n\n`;
            
            // Show first few products
            const displayProducts = products.slice(0, 3);
            displayProducts.forEach((product, index) => {
                message += `${index + 1}. **${product.name}** - £${product.price}\n`;
                message += `   ${product.description}\n\n`;
            });
            
            if (products.length > 3) {
                message += `... and ${products.length - 3} more products.\n\n`;
            }
            
            message += "Would you like to see more details or add any of these to your cart?";
            
            this.showMessage(message, 'bot');
            
            // Show product cards
            this.showProductCards(displayProducts);
            
            // Show quick actions
            this.showProductQuickActions(products);
        } else {
            this.showMessage(`Sorry, I couldn't find any products matching "${query}". Try different keywords or browse our categories.`, 'bot');
        }
    }

    handleProductRecommendation(custom) {
        const { products, reason } = custom;
        
        let message = `Based on your preferences, here are some recommendations:\n\n`;
        message += `*${reason}*\n\n`;
        
        products.forEach((product, index) => {
            message += `${index + 1}. **${product.name}** - £${product.price}\n`;
            message += `   ${product.description}\n\n`;
        });
        
        this.showMessage(message, 'bot');
        this.showProductCards(products);
    }

    handleCartAction(custom) {
        const { action, product, message } = custom;
        
        if (action === 'add_to_cart') {
            // Add to cart using the global cart system
            if (window.cartSystem) {
                window.cartSystem.addToCart(product);
            }
        } else if (action === 'remove_from_cart') {
            if (window.cartSystem) {
                window.cartSystem.removeFromCart(product.id, product.size, product.color);
            }
        }
        
        this.showMessage(message, 'bot');
    }

    handleQuickReply(custom) {
        const { options } = custom;
        
        let message = "Here are some quick options:\n\n";
        options.forEach((option, index) => {
            message += `${index + 1}. ${option.text}\n`;
        });
        
        this.showMessage(message, 'bot');
        this.showQuickReplyButtons(options);
    }

    showProductCards(products) {
        const cardsContainer = document.createElement('div');
        cardsContainer.className = 'product-cards-container';
        
        products.forEach(product => {
            const card = document.createElement('div');
            card.className = 'product-card';
            card.innerHTML = `
                <img src="${product.image}" alt="${product.name}" class="product-card-image">
                <div class="product-card-info">
                    <h4>${product.name}</h4>
                    <p class="product-card-price">£${product.price}</p>
                    <p class="product-card-description">${product.description}</p>
                    <div class="product-card-actions">
                        <button onclick="enhancedChatbot.addToCartFromCard('${product.id}')" class="btn-primary">Add to Cart</button>
                        <button onclick="enhancedChatbot.viewProductDetails('${product.id}')" class="btn-secondary">View Details</button>
                    </div>
                </div>
            `;
            cardsContainer.appendChild(card);
        });
        
        this.elements.messagesContainer.appendChild(cardsContainer);
        this.scrollToBottom();
    }

    showProductQuickActions(products) {
        const actionsContainer = document.createElement('div');
        actionsContainer.className = 'quick-actions-container';
        
        const actions = [
            { text: 'Show All Results', action: () => this.showAllSearchResults() },
            { text: 'Filter by Price', action: () => this.showPriceFilter() },
            { text: 'Filter by Category', action: () => this.showCategoryFilter() },
            { text: 'Sort by Price', action: () => this.sortProductsByPrice() }
        ];
        
        actions.forEach(action => {
            const button = document.createElement('button');
            button.className = 'quick-action-btn';
            button.textContent = action.text;
            button.onclick = action.action;
            actionsContainer.appendChild(button);
        });
        
        this.elements.messagesContainer.appendChild(actionsContainer);
        this.scrollToBottom();
    }

    showQuickReplyButtons(options) {
        const buttonsContainer = document.createElement('div');
        buttonsContainer.className = 'quick-reply-buttons';
        
        options.forEach(option => {
            const button = document.createElement('button');
            button.className = 'quick-reply-btn';
            button.textContent = option.text;
            button.onclick = () => {
                this.elements.messageInput.value = option.text;
                this.sendMessage();
            };
            buttonsContainer.appendChild(button);
        });
        
        this.elements.messagesContainer.appendChild(buttonsContainer);
        this.scrollToBottom();
    }

    addToCartFromCard(productId) {
        const product = this.products.find(p => p.id === productId);
        if (product && window.cartSystem) {
            const cartItem = {
                id: product.id,
                name: product.name,
                price: product.price,
                image: product.image,
                size: 'M', // Default size
                color: 'Black', // Default color
                quantity: 1
            };
            
            window.cartSystem.addToCart(cartItem);
            this.showMessage(`Added ${product.name} to your cart!`, 'bot');
        }
    }

    viewProductDetails(productId) {
        // Open product page
        window.open(`products/${productId}.html`, '_blank');
    }

    showAllSearchResults() {
        if (this.currentSearchResults.length > 0) {
            // Open products page with search results
            const searchQuery = encodeURIComponent(this.currentSearchQuery || '');
            window.open(`products/index.html?search=${searchQuery}`, '_blank');
        }
    }

    showPriceFilter() {
        this.showMessage('What price range are you looking for? (e.g., "under £50", "£50-100", "over £100")', 'bot');
    }

    showCategoryFilter() {
        this.showMessage('Which category interests you? (shirts, jackets, bottoms, accessories)', 'bot');
    }

    sortProductsByPrice() {
        if (this.currentSearchResults.length > 0) {
            const sorted = [...this.currentSearchResults].sort((a, b) => a.price - b.price);
            this.currentSearchResults = sorted;
            this.showMessage('Products sorted by price (low to high):', 'bot');
            this.showProductCards(sorted.slice(0, 3));
        }
    }

    async loadProducts() {
        try {
            // Load products from the products.js file
            if (window.products) {
                this.products = window.products;
            } else {
                // Fallback: load from API
                const response = await fetch('/api/products');
                if (response.ok) {
                    const data = await response.json();
                    this.products = data.products || [];
                }
            }
        } catch (error) {
            console.error('Error loading products:', error);
            this.products = [];
        }
    }

    // Voice recognition methods
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

    toggleVoiceRecognition() {
        if (this.isListening) {
            this.stopVoiceRecognition();
        } else {
            this.startVoiceRecognition();
        }
    }

    showVoiceFeedback() {
        this.elements.voiceFeedback.classList.add('show');
        document.getElementById('voice-text').textContent = 'Listening...';
    }

    hideVoiceFeedback() {
        this.elements.voiceFeedback.classList.remove('show');
    }

    // UI methods
    showMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        
        if (sender === 'bot') {
            messageDiv.innerHTML = `
                <div class="message-avatar">🤖</div>
                <div class="message-content">
                    <div class="message-text">${this.formatMessage(text)}</div>
                    <div class="message-time">${new Date().toLocaleTimeString()}</div>
                </div>
            `;
        } else {
            messageDiv.innerHTML = `
                <div class="message-content">
                    <div class="message-text">${this.formatMessage(text)}</div>
                    <div class="message-time">${new Date().toLocaleTimeString()}</div>
                </div>
                <div class="message-avatar">👤</div>
            `;
        }
        
        this.elements.messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();
    }

    formatMessage(text) {
        // Convert markdown-like formatting to HTML
        return text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/\n/g, '<br>');
    }

    showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot typing-indicator';
        typingDiv.innerHTML = `
            <div class="message-avatar">🤖</div>
            <div class="message-content">
                <div class="typing-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        `;
        
        this.elements.messagesContainer.appendChild(typingDiv);
        this.scrollToBottom();
    }

    hideTypingIndicator() {
        const typingIndicator = this.elements.messagesContainer.querySelector('.typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    handleQuickAction(e) {
        const action = e.target.dataset.action;
        if (action) {
            this.elements.messageInput.value = action;
            this.sendMessage();
        }
    }

    handleOutsideClick(e) {
        if (this.isOpen && !this.elements.container.contains(e.target) && !this.elements.toggle.contains(e.target)) {
            this.closeChatbot();
        }
    }

    autoResizeTextarea() {
        this.elements.messageInput.style.height = 'auto';
        this.elements.messageInput.style.height = Math.min(this.elements.messageInput.scrollHeight, 100) + 'px';
    }

    updateCharCounter() {
        const length = this.elements.messageInput.value.length;
        this.elements.charCounter.textContent = `${length}/500`;
        
        if (length > 450) {
            this.elements.charCounter.style.color = '#e74c3c';
        } else {
            this.elements.charCounter.style.color = '#666';
        }
    }

    scrollToBottom() {
        this.elements.messagesContainer.scrollTop = this.elements.messagesContainer.scrollHeight;
    }

    showNotificationBadge() {
        this.elements.toggle.classList.add('has-notification');
    }

    hideNotificationBadge() {
        this.elements.toggle.classList.remove('has-notification');
    }

    generateSessionId() {
        return 'session_' + Math.random().toString(36).substr(2, 9);
    }
}

// Initialize enhanced chatbot
const enhancedChatbot = new EnhancedManVueChatbot();

// Make it globally available
window.enhancedChatbot = enhancedChatbot;
