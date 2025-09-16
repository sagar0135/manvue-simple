/**
 * Enhanced MANVUE AI Chatbot
 * Features realistic search simulation and intelligent responses
 */

class EnhancedChatbot {
    constructor() {
        this.isOpen = false;
        this.isTyping = false;
        this.products = window.products || [];
        this.searchProgress = null;
        this.isResizing = false;
        this.resizeMode = false;
        this.init();
    }

    init() {
        this.createChatbotHTML();
        this.setupEventListeners();
        this.showWelcomeMessage();
    }

    createChatbotHTML() {
        // Remove existing chatbot if it exists
        const existingChatbot = document.getElementById('enhanced-chatbot');
        if (existingChatbot) {
            existingChatbot.remove();
        }

        // Remove existing chat toggle
        const existingToggle = document.querySelector('.chat-toggle');
        if (existingToggle) {
            existingToggle.remove();
        }

        // Create enhanced chatbot HTML
        const chatbotHTML = `
            <!-- Enhanced Chatbot -->
            <div id="enhanced-chatbot" class="chatbot">
                <div class="chat-header">
                    <div class="assistant-info">
                        <div class="assistant-avatar">🤖</div>
                        <div class="assistant-details">
                            <h3>MANVUE AI Assistant</h3>
                            <span class="assistant-status">Online • Ready to help</span>
                        </div>
                    </div>
                    <div class="chat-controls">
                        <button class="chat-control-btn" onclick="enhancedChatbot.toggleResize()" title="Resize Chat">📏</button>
                        <button class="chat-control-btn" onclick="enhancedChatbot.clearChat()" title="Clear Chat">🗑️</button>
                        <button class="chat-control-btn" onclick="enhancedChatbot.toggleChat()" title="Close">✕</button>
                    </div>
                </div>
                
                <div class="chat-messages" id="chat-messages-enhanced">
                    <!-- Messages will be added here -->
                </div>
                
                <div class="typing-indicator" id="typing-indicator-enhanced">
                    <div class="message-avatar">🤖</div>
                    <div class="typing-dots">
                        <span></span>
                        <span></span>
                        <span></span>
                    </div>
                    <span style="font-size: 12px; color: #64748b; margin-left: 8px;">AI is thinking...</span>
                </div>
                
                <div class="chat-input">
                    <div class="input-container">
                        <button class="input-action-btn" onclick="enhancedChatbot.startVoiceInput()" title="Voice Input">🎤</button>
                        <input type="text" id="chat-input-enhanced" placeholder="Ask about products, styles, or anything..." onkeypress="enhancedChatbot.handleKeyPress(event)">
                        <button class="input-action-btn" onclick="enhancedChatbot.attachFile()" title="Attach Image">📎</button>
                        <button class="send-btn" onclick="enhancedChatbot.sendMessage()">
                            <span>📤</span>
                        </button>
                    </div>
                </div>
                
                <!-- Resize Handle -->
                <div class="resize-handle" id="resize-handle"></div>
            </div>
            
            <!-- Enhanced Chat Toggle Button -->
            <div class="chat-toggle" onclick="enhancedChatbot.toggleChat()">💬</div>
        `;

        document.body.insertAdjacentHTML('beforeend', chatbotHTML);
        this.setupResizeFunctionality();
    }

    setupEventListeners() {
        // Setup any additional event listeners
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isOpen) {
                this.toggleChat();
            }
        });
    }

    toggleChat() {
        const chatbot = document.getElementById('enhanced-chatbot');
        const toggle = document.querySelector('.chat-toggle');
        
        if (this.isOpen) {
            chatbot.classList.remove('active');
            toggle.classList.remove('hidden');
            this.isOpen = false;
        } else {
            chatbot.classList.add('active');
            toggle.classList.add('hidden');
            this.isOpen = true;
            
            // Focus on input
            setTimeout(() => {
                document.getElementById('chat-input-enhanced').focus();
            }, 400);
        }
    }

    handleKeyPress(event) {
        if (event.key === 'Enter') {
            this.sendMessage();
        }
    }

    sendMessage() {
        const input = document.getElementById('chat-input-enhanced');
        const message = input.value.trim();
        
        if (!message || this.isTyping) return;
        
        // Add user message
        this.addMessage(message, 'user');
        input.value = '';
        
        // Process the message and respond
        this.processMessage(message);
    }

    addMessage(text, sender = 'bot', isHTML = false) {
        const messagesContainer = document.getElementById('chat-messages-enhanced');
        const messageDiv = document.createElement('div');
        messageDiv.className = `chat-message ${sender}`;
        
        const now = new Date();
        const timeString = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        const avatarEmoji = sender === 'user' ? '👤' : '🤖';
        
        messageDiv.innerHTML = `
            <div class="message-avatar">${avatarEmoji}</div>
            <div class="message-content">
                <div class="message-bubble">
                    ${isHTML ? text : this.escapeHtml(text)}
                </div>
                <div class="message-time">${timeString}</div>
            </div>
        `;
        
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        
        return messageDiv;
    }

    showTypingIndicator() {
        const indicator = document.getElementById('typing-indicator-enhanced');
        indicator.classList.add('show');
        this.isTyping = true;
        
        const messagesContainer = document.getElementById('chat-messages-enhanced');
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    hideTypingIndicator() {
        const indicator = document.getElementById('typing-indicator-enhanced');
        indicator.classList.remove('show');
        this.isTyping = false;
    }

    async processMessage(message) {
        const lowerMessage = message.toLowerCase();
        
        // Check for blue shirt query
        if (lowerMessage.includes('blue shirt') || (lowerMessage.includes('blue') && lowerMessage.includes('shirt'))) {
            await this.simulateProductSearch('blue shirts');
            return;
        }
        
        // Check for other product queries
        if (lowerMessage.includes('shirt') && !lowerMessage.includes('blue')) {
            await this.simulateProductSearch('shirts');
            return;
        }
        
        if (lowerMessage.includes('jacket')) {
            await this.simulateProductSearch('jackets');
            return;
        }
        
        if (lowerMessage.includes('t-shirt') || lowerMessage.includes('tshirt')) {
            await this.simulateProductSearch('t-shirts');
            return;
        }
        
        // Default AI responses
        this.showTypingIndicator();
        await this.delay(1500 + Math.random() * 1500);
        this.hideTypingIndicator();
        
        const response = this.generateAIResponse(message);
        this.addMessage(response, 'bot', true);
    }

    async simulateProductSearch(searchTerm) {
        this.showTypingIndicator();
        await this.delay(800);
        this.hideTypingIndicator();
        
        // Initial response
        this.addMessage(`🔍 I'll help you find ${searchTerm}! Let me search our inventory for you.`, 'bot');
        
        // Start search simulation
        await this.delay(1000);
        
        // Step 1: Searching all products
        const progressMsg = this.addProgressMessage();
        await this.updateSearchProgress(progressMsg, '🔄 Searching through 40,000 products...', 0);
        await this.delay(1500);
        await this.updateSearchProgress(progressMsg, '🔍 Analyzing product categories...', 25);
        await this.delay(1000);
        
        // Step 2: Narrowing down to shirts
        if (searchTerm.includes('shirt')) {
            await this.updateSearchProgress(progressMsg, '👔 Found 10,000 shirts in catalog...', 50);
            await this.delay(1200);
            await this.updateSearchProgress(progressMsg, '🎨 Filtering by color and style...', 75);
            await this.delay(1000);
        }
        
        // Step 3: Final results
        let resultCount, filteredProducts;
        if (searchTerm === 'blue shirts') {
            await this.updateSearchProgress(progressMsg, '✅ Found 247 blue shirts!', 100);
            filteredProducts = this.getBlueShirts();
            resultCount = 247;
        } else if (searchTerm === 'shirts') {
            await this.updateSearchProgress(progressMsg, '✅ Found 1,856 shirts!', 100);
            filteredProducts = this.getAllShirts();
            resultCount = 1856;
        } else {
            await this.updateSearchProgress(progressMsg, '✅ Search complete!', 100);
            filteredProducts = this.getProductsByCategory(searchTerm);
            resultCount = Math.floor(Math.random() * 500) + 50;
        }
        
        await this.delay(800);
        this.removeProgressMessage(progressMsg);
        
        // Show results
        this.showSearchResults(searchTerm, resultCount, filteredProducts);
    }

    addProgressMessage() {
        const messagesContainer = document.getElementById('chat-messages-enhanced');
        const progressDiv = document.createElement('div');
        progressDiv.className = 'chat-message bot';
        progressDiv.innerHTML = `
            <div class="message-avatar">🤖</div>
            <div class="message-content">
                <div class="search-progress">
                    <div class="progress-header">
                        <span class="progress-icon">⏳</span>
                        <span class="progress-text">Initializing search...</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: 0%"></div>
                    </div>
                    <div class="progress-text" style="font-size: 11px; margin-top: 4px;">Processing your request...</div>
                </div>
            </div>
        `;
        
        messagesContainer.appendChild(progressDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        return progressDiv;
    }

    async updateSearchProgress(progressDiv, text, percentage) {
        const progressFill = progressDiv.querySelector('.progress-fill');
        const progressText = progressDiv.querySelector('.progress-header .progress-text');
        const progressIcon = progressDiv.querySelector('.progress-icon');
        
        progressText.textContent = text;
        progressFill.style.width = percentage + '%';
        
        if (percentage === 100) {
            progressIcon.textContent = '✅';
        } else {
            progressIcon.textContent = '🔄';
        }
    }

    removeProgressMessage(progressDiv) {
        setTimeout(() => {
            progressDiv.remove();
        }, 500);
    }

    showSearchResults(searchTerm, count, products) {
        // First show the search summary
        let summaryHTML = `
            <div class="ai-status">
                <div class="status-icon"></div>
                <div class="status-text">Search completed successfully! Found ${count} ${searchTerm}</div>
            </div>
        `;
        this.addMessage(summaryHTML, 'bot', true);
        
        // Then show visual product results
        setTimeout(() => {
            const productHTML = this.createVisualProductResults(searchTerm);
            this.addMessage(productHTML, 'bot', true);
            
            // Add quick reply buttons
            setTimeout(() => {
                this.addQuickReplies(searchTerm);
            }, 500);
        }, 800);
    }
    
    createVisualProductResults(searchTerm) {
        const productImages = this.getProductImages(searchTerm);
        
        let productHTML = `
            <div class="product-card">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
                    <span style="font-size: 18px;">🛍️</span>
                    <span style="font-weight: 600; color: #1e293b;">Top Results</span>
                </div>
                <div class="product-grid">
        `;
        
        productImages.forEach((product, index) => {
            productHTML += `
                <div class="product-item" onclick="enhancedChatbot.viewProduct('${product.id}')" style="animation-delay: ${index * 0.1}s">
                    <img src="${product.image}" alt="${product.name}" class="product-image" />
                    <div class="product-name">${product.name}</div>
                    <div class="product-price">£${product.price}</div>
                    <div class="product-rating">${'⭐'.repeat(Math.floor(product.rating))} ${product.rating}</div>
                </div>
            `;
        });
        
        productHTML += `
                </div>
                <div style="text-align: center; margin-top: 12px;">
                    <a href="#" class="product-link" onclick="enhancedChatbot.viewProducts('${searchTerm}')" style="display: inline-block;">
                        <span>🔍</span>
                        <span>View All Results</span>
                    </a>
                </div>
            </div>
        `;
        
        return productHTML;
    }
    
    getProductImages(searchTerm) {
        // Return realistic product data with actual images
        if (searchTerm === 'blue shirts') {
            return [
                {
                    id: 'shirt-001',
                    name: 'Oxford Blue Shirt',
                    price: '59.99',
                    rating: 4.6,
                    image: 'https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=200&h=200&fit=crop&auto=format'
                },
                {
                    id: 'shirt-002',
                    name: 'Denim Chambray',
                    price: '52.99',
                    rating: 4.5,
                    image: 'https://images.unsplash.com/photo-1598300042247-d088f8ab3a91?w=200&h=200&fit=crop&auto=format'
                },
                {
                    id: 'shirt-003',
                    name: 'Navy Dress Shirt',
                    price: '69.99',
                    rating: 4.7,
                    image: 'https://images.unsplash.com/photo-1620012253295-c15cc3e65df4?w=200&h=200&fit=crop&auto=format'
                },
                {
                    id: 'shirt-004',
                    name: 'Light Blue Linen',
                    price: '48.99',
                    rating: 4.4,
                    image: 'https://images.unsplash.com/photo-1621072156002-e2fccdc0b176?w=200&h=200&fit=crop&auto=format'
                }
            ];
        } else if (searchTerm === 'shirts') {
            return [
                {
                    id: 'shirt-005',
                    name: 'White Dress Shirt',
                    price: '65.99',
                    rating: 4.8,
                    image: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=200&h=200&fit=crop&auto=format'
                },
                {
                    id: 'shirt-006',
                    name: 'Casual Plaid',
                    price: '44.99',
                    rating: 4.3,
                    image: 'https://images.unsplash.com/photo-1602810319428-019690571b5b?w=200&h=200&fit=crop&auto=format'
                },
                {
                    id: 'shirt-007',
                    name: 'Black Formal',
                    price: '89.99',
                    rating: 4.9,
                    image: 'https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=200&h=200&fit=crop&auto=format'
                },
                {
                    id: 'shirt-008',
                    name: 'Striped Casual',
                    price: '42.99',
                    rating: 4.2,
                    image: 'https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?w=200&h=200&fit=crop&auto=format'
                }
            ];
        } else {
            // Default products for other categories
            return [
                {
                    id: 'item-001',
                    name: 'Premium Item',
                    price: '75.99',
                    rating: 4.5,
                    image: 'https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=200&h=200&fit=crop&auto=format'
                },
                {
                    id: 'item-002',
                    name: 'Casual Style',
                    price: '55.99',
                    rating: 4.3,
                    image: 'https://images.unsplash.com/photo-1564584217132-2271339d4337?w=200&h=200&fit=crop&auto=format'
                }
            ];
        }
    }
    
    addQuickReplies(searchTerm) {
        const replies = this.getQuickReplies(searchTerm);
        
        let quickRepliesHTML = `
            <div style="margin: 12px 0;">
                <div style="font-size: 12px; color: #64748b; margin-bottom: 8px;">Quick actions:</div>
                <div class="quick-replies">
        `;
        
        replies.forEach(reply => {
            quickRepliesHTML += `
                <button class="quick-reply-btn" onclick="enhancedChatbot.handleQuickReply('${reply.action}', '${reply.text}')">
                    ${reply.icon} ${reply.text}
                </button>
            `;
        });
        
        quickRepliesHTML += `
                </div>
            </div>
        `;
        
        this.addMessage(quickRepliesHTML, 'bot', true);
    }
    
    getQuickReplies(searchTerm) {
        const baseReplies = [
            { icon: '📏', text: 'Size Guide', action: 'size_guide' },
            { icon: '🎨', text: 'More Colors', action: 'more_colors' },
            { icon: '💰', text: 'Best Deals', action: 'best_deals' },
            { icon: '⭐', text: 'Top Rated', action: 'top_rated' }
        ];
        
        if (searchTerm === 'blue shirts') {
            return [
                { icon: '🔍', text: 'Navy Shirts', action: 'navy_shirts' },
                { icon: '👔', text: 'Formal Shirts', action: 'formal_shirts' },
                ...baseReplies.slice(0, 2)
            ];
        }
        
        return baseReplies;
    }

    generateFollowUpMessage(searchTerm) {
        const followUps = [
            `Would you like me to filter these ${searchTerm} by size, price range, or brand?`,
            `I can also help you find matching accessories or suggest complete outfits with these ${searchTerm}.`,
            `Need help choosing the right size? I can guide you through our sizing recommendations.`,
            `Would you like to see customer reviews for any of these ${searchTerm}?`
        ];
        
        return followUps[Math.floor(Math.random() * followUps.length)];
    }

    generateAIResponse(message) {
        const lowerMessage = message.toLowerCase();
        
        // Greeting responses
        if (lowerMessage.includes('hello') || lowerMessage.includes('hi') || lowerMessage.includes('hey')) {
            return `Hello! 👋 I'm your AI fashion assistant. I can help you find the perfect clothing items, suggest outfits, or answer any questions about our products. What are you looking for today?`;
        }
        
        // Help responses
        if (lowerMessage.includes('help')) {
            return `I'm here to help! 🤝 I can assist you with:
                   <br><br>🔍 <strong>Product Search</strong> - Find specific items
                   <br>💡 <strong>Style Recommendations</strong> - Get personalized suggestions  
                   <br>📏 <strong>Size Guide</strong> - Help with sizing
                   <br>🎨 <strong>Color Matching</strong> - Coordinate outfits
                   <br>💰 <strong>Deals & Offers</strong> - Find the best prices
                   <br><br>Just ask me anything or try: "Show me blue shirts" or "I need a formal outfit"`;
        }
        
        // Size related
        if (lowerMessage.includes('size')) {
            return `📏 I can help you find the right size! Our size guide includes detailed measurements for all items. Would you like me to:
                   <br><br>• Show you the size chart for a specific item
                   <br>• Help you determine your size based on measurements
                   <br>• Recommend sizes based on fit preference (slim, regular, relaxed)
                   <br><br>What specific item are you looking to size?`;
        }
        
        // Price related
        if (lowerMessage.includes('price') || lowerMessage.includes('cost') || lowerMessage.includes('cheap') || lowerMessage.includes('expensive')) {
            return `💰 I can help you find items within your budget! Our products range from £25-£150. Would you like me to:
                   <br><br>• Show items under a specific price
                   <br>• Find the best deals and discounts
                   <br>• Compare prices across similar items
                   <br><br>What's your preferred price range?`;
        }
        
        // Style recommendations
        if (lowerMessage.includes('recommend') || lowerMessage.includes('suggest') || lowerMessage.includes('style')) {
            return `✨ I'd love to help you find your perfect style! To give you the best recommendations, could you tell me:
                   <br><br>🎯 What occasion? (casual, formal, work, date)
                   <br>🌡️ What season/weather?
                   <br>🎨 Any color preferences?
                   <br>💼 Your style preference? (classic, trendy, minimalist)
                   <br><br>Or I can start with our trending items right now!`;
        }
        
        // Default response
        return `I understand you're asking about "${message}". While I'm getting smarter every day, I might need a bit more context to give you the best answer! 🤖
               <br><br>Try asking me about:
               <br>• Specific products (shirts, jackets, accessories)
               <br>• Colors or styles you like
               <br>• Size or fit questions
               <br>• Style recommendations
               <br><br>I'm here to make your shopping experience amazing! 🛍️`;
    }

    getBlueShirts() {
        return this.products.filter(product => 
            product.type === 'shirt' && 
            product.colors.some(color => 
                color.toLowerCase().includes('blue') || 
                color.toLowerCase().includes('navy')
            )
        );
    }

    getAllShirts() {
        return this.products.filter(product => product.type === 'shirt');
    }

    getProductsByCategory(category) {
        const categoryMap = {
            'jackets': 'jacket',
            't-shirts': 'tshirt',
            'pants': 'pants',
            'jeans': 'jeans'
        };
        
        const productType = categoryMap[category] || category.replace('s', '');
        return this.products.filter(product => product.type.includes(productType));
    }

    viewProducts(searchTerm) {
        // This would typically navigate to a products page
        // For demo purposes, we'll show a message
        this.addMessage(`🔄 Redirecting you to browse all ${searchTerm}... In a real implementation, this would take you to the filtered products page!`, 'bot');
        
        // You could implement actual navigation here:
        // window.location.href = `/products?search=${encodeURIComponent(searchTerm)}`;
    }
    
    viewProduct(productId) {
        this.addMessage(`👀 Opening product details for ${productId}... In a real implementation, this would show the product page with full details, size options, and purchase options!`, 'bot');
    }
    
    handleQuickReply(action, text) {
        // Add user message to show what they clicked
        this.addMessage(text, 'user');
        
        // Handle the action
        setTimeout(() => {
            this.processQuickReplyAction(action);
        }, 500);
    }
    
    async processQuickReplyAction(action) {
        this.showTypingIndicator();
        await this.delay(1000);
        this.hideTypingIndicator();
        
        switch (action) {
            case 'size_guide':
                this.showSizeGuide();
                break;
            case 'more_colors':
                this.showMoreColors();
                break;
            case 'best_deals':
                this.showBestDeals();
                break;
            case 'top_rated':
                this.showTopRated();
                break;
            case 'navy_shirts':
                this.simulateProductSearch('navy shirts');
                break;
            case 'formal_shirts':
                this.simulateProductSearch('formal shirts');
                break;
            default:
                this.addMessage('🤖 I\'m working on this feature! It will be available soon. Is there anything else I can help you with?', 'bot');
        }
    }
    
    showSizeGuide() {
        const sizeGuideHTML = `
            <div class="product-card">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
                    <span style="font-size: 18px;">📏</span>
                    <span style="font-weight: 600; color: #1e293b;">Size Guide</span>
                </div>
                <div style="background: linear-gradient(145deg, #f8fafc, #e2e8f0); border-radius: 12px; padding: 16px; margin: 12px 0;">
                    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; text-align: center; font-size: 12px;">
                        <div style="font-weight: 600; padding: 8px; background: #667eea; color: white; border-radius: 6px;">Size</div>
                        <div style="font-weight: 600; padding: 8px; background: #667eea; color: white; border-radius: 6px;">Chest</div>
                        <div style="font-weight: 600; padding: 8px; background: #667eea; color: white; border-radius: 6px;">Length</div>
                        <div style="font-weight: 600; padding: 8px; background: #667eea; color: white; border-radius: 6px;">Shoulder</div>
                        <div style="padding: 6px;">S</div><div style="padding: 6px;">36-38"</div><div style="padding: 6px;">28"</div><div style="padding: 6px;">17"</div>
                        <div style="padding: 6px;">M</div><div style="padding: 6px;">38-40"</div><div style="padding: 6px;">29"</div><div style="padding: 6px;">18"</div>
                        <div style="padding: 6px;">L</div><div style="padding: 6px;">40-42"</div><div style="padding: 6px;">30"</div><div style="padding: 6px;">19"</div>
                        <div style="padding: 6px;">XL</div><div style="padding: 6px;">42-44"</div><div style="padding: 6px;">31"</div><div style="padding: 6px;">20"</div>
                    </div>
                </div>
                <div style="font-size: 11px; color: #64748b; text-align: center;">
                    💡 Need help measuring? I can guide you through the process!
                </div>
            </div>
        `;
        this.addMessage(sizeGuideHTML, 'bot', true);
    }
    
    showMoreColors() {
        const colorsHTML = `
            <div class="product-card">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
                    <span style="font-size: 18px;">🎨</span>
                    <span style="font-weight: 600; color: #1e293b;">Available Colors</span>
                </div>
                <div style="display: flex; flex-wrap: wrap; gap: 12px; justify-content: center; margin: 16px 0;">
                    <div style="text-align: center; cursor: pointer;" onclick="enhancedChatbot.selectColor('Navy')">
                        <div style="width: 40px; height: 40px; background: #1e3a8a; border-radius: 50%; margin: 0 auto 4px; border: 3px solid #e5e7eb; transition: all 0.2s;"></div>
                        <div style="font-size: 11px;">Navy</div>
                    </div>
                    <div style="text-align: center; cursor: pointer;" onclick="enhancedChatbot.selectColor('Light Blue')">
                        <div style="width: 40px; height: 40px; background: #93c5fd; border-radius: 50%; margin: 0 auto 4px; border: 3px solid #e5e7eb;"></div>
                        <div style="font-size: 11px;">Light Blue</div>
                    </div>
                    <div style="text-align: center; cursor: pointer;" onclick="enhancedChatbot.selectColor('Royal Blue')">
                        <div style="width: 40px; height: 40px; background: #2563eb; border-radius: 50%; margin: 0 auto 4px; border: 3px solid #e5e7eb;"></div>
                        <div style="font-size: 11px;">Royal Blue</div>
                    </div>
                    <div style="text-align: center; cursor: pointer;" onclick="enhancedChatbot.selectColor('Denim')">
                        <div style="width: 40px; height: 40px; background: #4a90e2; border-radius: 50%; margin: 0 auto 4px; border: 3px solid #e5e7eb;"></div>
                        <div style="font-size: 11px;">Denim</div>
                    </div>
                </div>
                <div style="font-size: 11px; color: #64748b; text-align: center;">
                    Click on any color to see shirts in that shade!
                </div>
            </div>
        `;
        this.addMessage(colorsHTML, 'bot', true);
    }
    
    showBestDeals() {
        const dealsHTML = `
            <div class="product-card">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
                    <span style="font-size: 18px;">💰</span>
                    <span style="font-weight: 600; color: #1e293b;">Best Deals</span>
                    <span style="background: #ef4444; color: white; padding: 2px 8px; border-radius: 12px; font-size: 10px;">HOT</span>
                </div>
                <div style="background: linear-gradient(145deg, #fef3c7, #fcd34d); border-radius: 12px; padding: 16px; margin: 12px 0; border: 2px dashed #f59e0b;">
                    <div style="text-align: center;">
                        <div style="font-size: 24px; margin-bottom: 8px;">🔥</div>
                        <div style="font-weight: 700; color: #92400e; font-size: 16px;">Flash Sale!</div>
                        <div style="font-size: 14px; color: #b45309; margin: 4px 0;">Up to 40% off Blue Shirts</div>
                        <div style="font-size: 11px; color: #a16207;">⏰ Ends in 4 hours 23 minutes</div>
                    </div>
                </div>
                <div style="font-size: 12px; color: #059669; margin: 8px 0;">
                    ✨ Oxford Blue Shirt: <s>£59.99</s> <strong>£35.99</strong><br>
                    ✨ Denim Chambray: <s>£52.99</s> <strong>£31.79</strong><br>
                    ✨ Navy Dress Shirt: <s>£69.99</s> <strong>£41.99</strong>
                </div>
            </div>
        `;
        this.addMessage(dealsHTML, 'bot', true);
    }
    
    showTopRated() {
        const topRatedHTML = `
            <div class="product-card">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
                    <span style="font-size: 18px;">⭐</span>
                    <span style="font-weight: 600; color: #1e293b;">Top Rated Items</span>
                </div>
                <div style="font-size: 12px; color: #059669; margin: 8px 0;">
                    🏆 Navy Dress Shirt - ⭐⭐⭐⭐⭐ 4.9/5 (324 reviews)<br>
                    🥇 Oxford Blue Shirt - ⭐⭐⭐⭐⭐ 4.7/5 (567 reviews)<br>
                    🥈 Premium Cotton Shirt - ⭐⭐⭐⭐⭐ 4.6/5 (423 reviews)<br>
                    🥉 Classic Fit Blue - ⭐⭐⭐⭐⭐ 4.5/5 (298 reviews)
                </div>
                <div style="background: #f0f9ff; border-radius: 8px; padding: 12px; margin: 12px 0; border-left: 4px solid #0ea5e9;">
                    <div style="font-size: 11px; color: #0369a1;">
                        💬 "Exceptional quality and fit!" - Verified Customer
                    </div>
                </div>
            </div>
        `;
        this.addMessage(topRatedHTML, 'bot', true);
    }
    
    selectColor(color) {
        this.addMessage(`I'd like to see ${color} shirts`, 'user');
        setTimeout(() => {
            this.addMessage(`🎨 Great choice! Searching for ${color.toLowerCase()} shirts...`, 'bot');
            setTimeout(() => {
                this.simulateProductSearch(`${color.toLowerCase()} shirts`);
            }, 800);
        }, 300);
    }

    clearChat() {
        const messagesContainer = document.getElementById('chat-messages-enhanced');
        messagesContainer.innerHTML = '';
        this.showWelcomeMessage();
    }

    showWelcomeMessage() {
        setTimeout(() => {
            const welcomeHTML = `
                <div style="text-align: center; padding: 8px;">
                    <div style="font-size: 24px; margin-bottom: 8px;">🤖✨</div>
                    <div style="font-weight: 600; margin-bottom: 4px;">Welcome to MANVUE AI!</div>
                    <div style="font-size: 12px; color: #64748b; margin-bottom: 12px;">Your intelligent fashion assistant</div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 11px;">
                        <div style="background: #f1f5f9; padding: 8px; border-radius: 8px; text-align: center;">
                            <div>🔍</div>
                            <div>Product Search</div>
                        </div>
                        <div style="background: #f1f5f9; padding: 8px; border-radius: 8px; text-align: center;">
                            <div>💡</div>
                            <div>Style Tips</div>
                        </div>
                        <div style="background: #f1f5f9; padding: 8px; border-radius: 8px; text-align: center;">
                            <div>📏</div>
                            <div>Size Guide</div>
                        </div>
                        <div style="background: #f1f5f9; padding: 8px; border-radius: 8px; text-align: center;">
                            <div>🎨</div>
                            <div>Outfit Builder</div>
                        </div>
                    </div>
                    <div style="margin-top: 12px; font-size: 12px; color: #64748b;">
                        Try: "Show me blue shirts" or "I need a formal outfit"
                    </div>
                </div>
            `;
            this.addMessage(welcomeHTML, 'bot', true);
        }, 500);
    }

    startVoiceInput() {
        // Voice input functionality placeholder
        this.addMessage("🎤 Voice input is coming soon! For now, please type your message.", 'bot');
    }

    attachFile() {
        // File attachment functionality placeholder
        this.addMessage("📎 Image search is coming soon! You'll be able to upload photos to find similar products.", 'bot');
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    setupResizeFunctionality() {
        const chatbot = document.getElementById('enhanced-chatbot');
        const resizeHandle = document.getElementById('resize-handle');
        
        if (!resizeHandle) return;

        // Mouse events for resizing
        resizeHandle.addEventListener('mousedown', (e) => {
            e.preventDefault();
            this.isResizing = true;
            this.startX = e.clientX;
            this.startY = e.clientY;
            this.startWidth = chatbot.offsetWidth;
            this.startHeight = chatbot.offsetHeight;
            
            document.addEventListener('mousemove', this.handleResize.bind(this));
            document.addEventListener('mouseup', this.stopResize.bind(this));
        });

        // Touch events for mobile
        resizeHandle.addEventListener('touchstart', (e) => {
            e.preventDefault();
            this.isResizing = true;
            this.startX = e.touches[0].clientX;
            this.startY = e.touches[0].clientY;
            this.startWidth = chatbot.offsetWidth;
            this.startHeight = chatbot.offsetHeight;
            
            document.addEventListener('touchmove', this.handleResize.bind(this));
            document.addEventListener('touchend', this.stopResize.bind(this));
        });
    }

    handleResize(e) {
        if (!this.isResizing) return;
        
        const chatbot = document.getElementById('enhanced-chatbot');
        const clientX = e.type === 'touchmove' ? e.touches[0].clientX : e.clientX;
        const clientY = e.type === 'touchmove' ? e.touches[0].clientY : e.clientY;
        
        const deltaX = clientX - this.startX;
        const deltaY = clientY - this.startY;
        
        const newWidth = Math.max(300, Math.min(window.innerWidth * 0.9, this.startWidth + deltaX));
        const newHeight = Math.max(400, Math.min(window.innerHeight * 0.9, this.startHeight + deltaY));
        
        chatbot.style.width = newWidth + 'px';
        chatbot.style.height = newHeight + 'px';
    }

    stopResize() {
        this.isResizing = false;
        document.removeEventListener('mousemove', this.handleResize.bind(this));
        document.removeEventListener('mouseup', this.stopResize.bind(this));
        document.removeEventListener('touchmove', this.handleResize.bind(this));
        document.removeEventListener('touchend', this.stopResize.bind(this));
    }

    toggleResize() {
        const chatbot = document.getElementById('enhanced-chatbot');
        const resizeHandle = document.getElementById('resize-handle');
        
        this.resizeMode = !this.resizeMode;
        
        if (this.resizeMode) {
            chatbot.style.resize = 'both';
            chatbot.style.overflow = 'auto';
            resizeHandle.style.display = 'block';
            resizeHandle.style.opacity = '1';
        } else {
            chatbot.style.resize = 'none';
            chatbot.style.overflow = 'hidden';
            resizeHandle.style.display = 'none';
            resizeHandle.style.opacity = '0';
        }
    }
}

// Initialize the enhanced chatbot when the page loads
let enhancedChatbot;

document.addEventListener('DOMContentLoaded', function() {
    enhancedChatbot = new EnhancedChatbot();
    
    // Make it globally accessible
    window.enhancedChatbot = enhancedChatbot;
    
    console.log('🤖 Enhanced MANVUE AI Chatbot initialized successfully!');
});
