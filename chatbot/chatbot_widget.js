/**
 * ManVue Chatbot Widget Integration
 * Easily integrates the chatbot into any ManVue page
 */

class ManVueChatbotWidget {
    constructor(options = {}) {
        this.options = {
            serverUrl: options.serverUrl || 'http://localhost:5055',
            websocketUrl: options.websocketUrl || 'ws://localhost:5055/ws',
            autoLoad: options.autoLoad !== false,
            position: options.position || 'bottom-right',
            theme: options.theme || 'default',
            showWelcome: options.showWelcome !== false,
            enableVoice: options.enableVoice !== false,
            ...options
        };
        
        this.isLoaded = false;
        this.isInitialized = false;
        
        if (this.options.autoLoad) {
            this.init();
        }
    }
    
    async init() {
        if (this.isInitialized) return;
        
        try {
            await this.loadStyles();
            await this.loadWidget();
            this.setupIntegration();
            this.isInitialized = true;
            
            console.log('✅ ManVue Chatbot Widget initialized');
        } catch (error) {
            console.error('❌ Failed to initialize chatbot widget:', error);
        }
    }
    
    async loadStyles() {
        return new Promise((resolve, reject) => {
            const link = document.createElement('link');
            link.rel = 'stylesheet';
            link.href = `${this.options.serverUrl}/static/chatbot.css`;
            link.onload = resolve;
            link.onerror = () => {
                // Fallback: inject basic styles
                this.injectFallbackStyles();
                resolve();
            };
            document.head.appendChild(link);
        });
    }
    
    injectFallbackStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .manvue-chatbot-widget {
                position: fixed;
                bottom: 20px;
                right: 20px;
                z-index: 9999;
                font-family: Arial, sans-serif;
            }
            .manvue-chatbot-toggle {
                width: 60px;
                height: 60px;
                background: linear-gradient(135deg, #3498db, #2c3e50);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                color: white;
                font-size: 24px;
                border: none;
                transition: transform 0.3s ease;
            }
            .manvue-chatbot-toggle:hover {
                transform: scale(1.1);
            }
        `;
        document.head.appendChild(style);
    }
    
    async loadWidget() {
        try {
            const response = await fetch(`${this.options.serverUrl}/static/chatbot.html`);
            const html = await response.text();
            
            // Create widget container
            const widgetContainer = document.createElement('div');
            widgetContainer.id = 'manvue-chatbot-widget';
            widgetContainer.className = 'manvue-chatbot-widget';
            widgetContainer.innerHTML = html;
            
            // Apply position
            this.applyPosition(widgetContainer);
            
            document.body.appendChild(widgetContainer);
            
            // Load the chatbot JavaScript
            await this.loadChatbotScript();
            
        } catch (error) {
            console.error('Failed to load chatbot widget, using fallback');
            this.createFallbackWidget();
        }
    }
    
    async loadChatbotScript() {
        return new Promise((resolve, reject) => {
            const script = document.createElement('script');
            script.src = `${this.options.serverUrl}/static/chatbot.js`;
            script.onload = () => {
                // Override chatbot options
                if (window.ManVueChatbot) {
                    this.chatbot = new window.ManVueChatbot({
                        ...this.options,
                        websocketUrl: this.options.websocketUrl,
                        serverUrl: this.options.serverUrl
                    });
                }
                resolve();
            };
            script.onerror = reject;
            document.head.appendChild(script);
        });
    }
    
    createFallbackWidget() {
        const widget = document.createElement('div');
        widget.className = 'manvue-chatbot-widget';
        widget.innerHTML = `
            <button class="manvue-chatbot-toggle" onclick="window.open('${this.options.serverUrl}', '_blank', 'width=400,height=600')">
                💬
            </button>
        `;
        this.applyPosition(widget);
        document.body.appendChild(widget);
    }
    
    applyPosition(element) {
        const positions = {
            'bottom-right': { bottom: '20px', right: '20px' },
            'bottom-left': { bottom: '20px', left: '20px' },
            'top-right': { top: '20px', right: '20px' },
            'top-left': { top: '20px', left: '20px' }
        };
        
        const pos = positions[this.options.position] || positions['bottom-right'];
        Object.assign(element.style, {
            position: 'fixed',
            zIndex: '9999',
            ...pos
        });
    }
    
    setupIntegration() {
        // Custom integration for ManVue
        this.setupProductIntegration();
        this.setupUserIntegration();
        this.setupAnalytics();
    }
    
    setupProductIntegration() {
        // Detect current product page and provide context
        const productId = this.getCurrentProductId();
        const category = this.getCurrentCategory();
        
        if (productId || category) {
            this.setContext({
                currentProduct: productId,
                currentCategory: category,
                page: window.location.pathname
            });
        }
    }
    
    setupUserIntegration() {
        // Integrate with ManVue user session if available
        const user = this.getCurrentUser();
        if (user) {
            this.setUser(user);
        }
    }
    
    setupAnalytics() {
        // Track chatbot interactions
        this.on('message_sent', (data) => {
            this.trackEvent('chatbot_message_sent', {
                message_length: data.message.length,
                session_id: data.session_id
            });
        });
        
        this.on('chatbot_opened', () => {
            this.trackEvent('chatbot_opened', {
                page: window.location.pathname,
                timestamp: new Date().toISOString()
            });
        });
    }
    
    getCurrentProductId() {
        // Extract product ID from URL or page data
        const urlMatch = window.location.pathname.match(/\/products?\/([^\/]+)/);
        if (urlMatch) return urlMatch[1];
        
        // Try to find product data in page
        const productElement = document.querySelector('[data-product-id]');
        if (productElement) return productElement.dataset.productId;
        
        return null;
    }
    
    getCurrentCategory() {
        // Extract category from URL or page data
        const urlMatch = window.location.pathname.match(/\/categories?\/([^\/]+)/);
        if (urlMatch) return urlMatch[1];
        
        // Try to find category data in page
        const categoryElement = document.querySelector('[data-category]');
        if (categoryElement) return categoryElement.dataset.category;
        
        return null;
    }
    
    getCurrentUser() {
        // Try to get user data from various sources
        if (window.manvueUser) return window.manvueUser;
        if (window.currentUser) return window.currentUser;
        
        // Try localStorage
        const userData = localStorage.getItem('manvue_user');
        if (userData) {
            try {
                return JSON.parse(userData);
            } catch (e) {
                return null;
            }
        }
        
        return null;
    }
    
    setContext(context) {
        if (this.chatbot && this.chatbot.setContext) {
            this.chatbot.setContext(context);
        } else {
            this.pendingContext = context;
        }
    }
    
    setUser(user) {
        if (this.chatbot && this.chatbot.setUser) {
            this.chatbot.setUser(user);
        } else {
            this.pendingUser = user;
        }
    }
    
    sendMessage(message) {
        if (this.chatbot && this.chatbot.sendMessage) {
            this.chatbot.sendMessage(message);
        }
    }
    
    open() {
        if (this.chatbot && this.chatbot.open) {
            this.chatbot.open();
        }
    }
    
    close() {
        if (this.chatbot && this.chatbot.close) {
            this.chatbot.close();
        }
    }
    
    on(event, callback) {
        if (!this.eventListeners) this.eventListeners = {};
        if (!this.eventListeners[event]) this.eventListeners[event] = [];
        this.eventListeners[event].push(callback);
    }
    
    emit(event, data) {
        if (this.eventListeners && this.eventListeners[event]) {
            this.eventListeners[event].forEach(callback => callback(data));
        }
    }
    
    trackEvent(eventName, data) {
        // Integration with analytics
        if (window.gtag) {
            window.gtag('event', eventName, data);
        }
        if (window.analytics) {
            window.analytics.track(eventName, data);
        }
        console.log('📊 Chatbot Event:', eventName, data);
    }
    
    // Static method for easy initialization
    static init(options = {}) {
        if (!window.manvueChatbotWidget) {
            window.manvueChatbotWidget = new ManVueChatbotWidget(options);
        }
        return window.manvueChatbotWidget;
    }
}

// Auto-initialize if data attributes are present
document.addEventListener('DOMContentLoaded', () => {
    const autoInit = document.querySelector('[data-manvue-chatbot]');
    if (autoInit) {
        const options = {};
        
        // Parse options from data attributes
        Object.keys(autoInit.dataset).forEach(key => {
            if (key.startsWith('chatbot')) {
                const optionKey = key.replace('chatbot', '').toLowerCase();
                options[optionKey] = autoInit.dataset[key];
            }
        });
        
        ManVueChatbotWidget.init(options);
    }
});

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ManVueChatbotWidget;
}

// Global namespace
window.ManVueChatbotWidget = ManVueChatbotWidget;

