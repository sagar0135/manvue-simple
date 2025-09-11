/**
 * ManVue Voice Commands Integration
 * 
 * This file bridges voice commands with the existing ManVue application functions
 */

class ManVueVoiceIntegration {
    constructor() {
        this.isInitialized = false;
        this.currentProduct = null;
        this.init();
    }
    
    init() {
        // Wait for ManVue functions to be available
        if (typeof window.searchProducts === 'function' && 
            typeof window.addToCart === 'function' && 
            typeof window.toggleCart === 'function') {
            this.isInitialized = true;
            console.log('ManVue Voice Integration initialized successfully');
            this.setupVoiceInterface();
        } else {
            // Retry after a short delay
            setTimeout(() => this.init(), 500);
        }
    }
    
    setupVoiceInterface() {
        if (!window.VoiceInterface) {
            console.warn('VoiceInterface not available');
            return;
        }
        
        
        // Initialize voice interface with ManVue integration
        window.manvueVoice = new VoiceInterface({
            continuous: true,
            interimResults: true,
            onResult: this.handleVoiceResult.bind(this),
            onError: this.handleVoiceError.bind(this),
            onStart: this.handleVoiceStart.bind(this),
            onEnd: this.handleVoiceEnd.bind(this)
        });
        
        // Override command execution to use ManVue functions
        this.overrideCommandExecution();
        
        console.log('Voice interface setup completed');
    }
    
    overrideCommandExecution() {
        if (!window.manvueVoice) return;
        
        // Override the executeCommand method to use actual ManVue functions
        const originalExecuteCommand = window.manvueVoice.executeCommand.bind(window.manvueVoice);
        
        window.manvueVoice.executeCommand = (commandResult) => {
            console.log('Executing ManVue voice command:', commandResult);
            
            const { action, parameters } = commandResult;
            let success = false;
            
            try {
                switch (action) {
                    case 'navigate_to_page':
                        success = this.handleNavigation(parameters);
                        break;
                    case 'search_products':
                        success = this.handleSearch(parameters);
                        break;
                    case 'open_cart':
                        success = this.handleOpenCart();
                        break;
                    case 'add_to_cart':
                        success = this.handleAddToCart(parameters);
                        break;
                    case 'show_product_details':
                        success = this.handleShowDetails(parameters);
                        break;
                    case 'filter_by_category':
                        success = this.handleCategoryFilter(parameters);
                        break;
                    case 'filter_by_color':
                        success = this.handleColorFilter(parameters);
                        break;
                    case 'filter_by_price':
                        success = this.handlePriceFilter(parameters);
                        break;
                    default:
                        // Fall back to original implementation
                        originalExecuteCommand(commandResult);
                        return;
                }
                
                // Provide feedback
                if (success) {
                    this.showSuccess(`✅ ${action.replace('_', ' ')} completed`);
                    this.speakFeedback(`Command executed: ${action.replace('_', ' ')}`);
                } else {
                    this.showError(`❌ Failed to execute ${action.replace('_', ' ')}`);
                    this.speakFeedback(`Sorry, I couldn't complete that action`);
                }
                
            } catch (error) {
                console.error('Error executing ManVue voice command:', error);
                this.showError('❌ Command execution failed');
                this.speakFeedback('Sorry, something went wrong');
            }
        };
    }
    
    // Navigation handlers
    handleNavigation(parameters) {
        const { page, url } = parameters;
        
        switch (page) {
            case 'home':
                if (typeof window.goHome === 'function') {
                    window.goHome();
                    return true;
                } else if (typeof window.showSection === 'function') {
                    window.showSection('home');
                    return true;
                }
                break;
                
            case 'products':
                if (typeof window.showSection === 'function') {
                    window.showSection('products');
                    return true;
                }
                break;
                
            default:
                if (url) {
                    window.location.href = url;
                    return true;
                }
        }
        
        return false;
    }
    
    // Search handlers
    handleSearch(parameters) {
        const { query, type } = parameters;
        
        if (!query && !parameters.category && !parameters.color) {
            console.warn('No search terms provided');
            return false;
        }
        
        try {
            // Use the existing searchProducts function
            if (typeof window.searchProducts === 'function') {
                // Build search query from parameters
                let searchTerm = query || '';
                
                if (parameters.color && parameters.item) {
                    searchTerm = `${parameters.color} ${parameters.item}`;
                } else if (parameters.category) {
                    searchTerm = parameters.category;
                } else if (parameters.color) {
                    searchTerm = parameters.color;
                }
                
                // Set the search input and trigger search
                const searchInput = document.getElementById('search-input');
                if (searchInput) {
                    searchInput.value = searchTerm;
                }
                
                window.searchProducts(searchTerm);
                return true;
            }
        } catch (error) {
            console.error('Search error:', error);
        }
        
        return false;
    }
    
    // Cart handlers
    handleOpenCart() {
        try {
            if (typeof window.toggleCart === 'function') {
                window.toggleCart();
                return true;
            }
        } catch (error) {
            console.error('Cart open error:', error);
        }
        return false;
    }
    
    handleAddToCart(parameters) {
        try {
            // If we're on a product page, get current product
            const currentProductId = this.getCurrentProductId();
            
            if (currentProductId && typeof window.addToCart === 'function') {
                window.addToCart(currentProductId);
                return true;
            } else {
                // Show message if no product is selected
                this.showError('Please select a product first');
                return false;
            }
        } catch (error) {
            console.error('Add to cart error:', error);
        }
        return false;
    }
    
    // Filter handlers
    handleCategoryFilter(parameters) {
        const { category } = parameters;
        
        try {
            if (typeof window.filterProducts === 'function') {
                window.filterProducts(category);
                return true;
            }
        } catch (error) {
            console.error('Category filter error:', error);
        }
        return false;
    }
    
    handleColorFilter(parameters) {
        const { color } = parameters;
        
        try {
            // Use color-based search
            if (typeof window.searchByColor === 'function') {
                window.searchByColor(color);
                return true;
            } else if (typeof window.searchProducts === 'function') {
                window.searchProducts(color);
                return true;
            }
        } catch (error) {
            console.error('Color filter error:', error);
        }
        return false;
    }
    
    handlePriceFilter(parameters) {
        const { price, amount } = parameters;
        
        try {
            // Try to use existing price filter functions
            if (typeof window.filterByPrice === 'function') {
                window.filterByPrice(amount || price);
                return true;
            }
        } catch (error) {
            console.error('Price filter error:', error);
        }
        return false;
    }
    
    handleShowDetails(parameters) {
        try {
            const currentProductId = this.getCurrentProductId();
            
            if (currentProductId && typeof window.quickView === 'function') {
                window.quickView(currentProductId);
                return true;
            } else if (currentProductId && typeof window.viewProduct === 'function') {
                window.viewProduct(currentProductId);
                return true;
            }
        } catch (error) {
            console.error('Show details error:', error);
        }
        return false;
    }
    
    // Utility functions
    getCurrentProductId() {
        // Try to get current product ID from various sources
        
        // Check if we're on product page
        const productElement = document.querySelector('[data-product-id]');
        if (productElement) {
            return parseInt(productElement.getAttribute('data-product-id'));
        }
        
        // Check for selected product in quick view
        const quickViewModal = document.getElementById('quick-view-modal');
        if (quickViewModal && quickViewModal.style.display !== 'none') {
            const modalProductId = quickViewModal.getAttribute('data-product-id');
            if (modalProductId) {
                return parseInt(modalProductId);
            }
        }
        
        // Check for currently highlighted product
        const highlightedProduct = document.querySelector('.product-card.highlighted, .product-card:hover');
        if (highlightedProduct) {
            const productId = highlightedProduct.getAttribute('data-product-id');
            if (productId) {
                return parseInt(productId);
            }
        }
        
        // Check if there's a single visible product
        const visibleProducts = document.querySelectorAll('.product-card:not(.hidden)');
        if (visibleProducts.length === 1) {
            const productId = visibleProducts[0].getAttribute('data-product-id');
            if (productId) {
                return parseInt(productId);
            }
        }
        
        return null;
    }
    
    // Feedback functions
    showSuccess(message) {
        this.showMessage(message, 'success');
    }
    
    showError(message) {
        this.showMessage(message, 'error');
    }
    
    showMessage(message, type = 'info') {
        // Use existing ManVue message system if available
        if (typeof window.showMessage === 'function') {
            window.showMessage(message);
        } else {
            // Fallback to console
            console.log(`[Voice ${type.toUpperCase()}] ${message}`);
        }
        
        // Also show in voice UI if available
        if (window.manvueVoice && window.manvueVoice.ui) {
            window.manvueVoice.ui.showFeedback(message, type);
        }
    }
    
    speakFeedback(message) {
        // Use TTS if available
        if (window.manvueVoice && window.manvueVoice.tts && typeof window.manvueVoice.tts.speak === 'function') {
            window.manvueVoice.tts.speak(message);
        }
    }
    
    // Voice event handlers
    handleVoiceResult(transcript, confidence, commandResult) {
        console.log('Voice result:', { transcript, confidence, commandResult });
        
        if (commandResult) {
            this.showSuccess(`🎤 "${transcript}"`);
        } else {
            this.showError(`🎤 "${transcript}" - command not recognized`);
        }
    }
    
    handleVoiceError(error, message) {
        console.error('Voice error:', error, message);
        this.showError(`Voice error: ${message}`);
    }
    
    handleVoiceStart() {
        this.showMessage('🎤 Listening...', 'info');
    }
    
    handleVoiceEnd() {
        this.showMessage('🎤 Voice recognition stopped', 'info');
    }
    
    // Public API
    startListening() {
        if (window.manvueVoice) {
            return window.manvueVoice.startListening();
        }
        return false;
    }
    
    stopListening() {
        if (window.manvueVoice) {
            return window.manvueVoice.stopListening();
        }
        return false;
    }
    
    isListening() {
        if (window.manvueVoice) {
            return window.manvueVoice.isCurrentlyListening();
        }
        return false;
    }
}

// Initialize integration when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Wait a bit for other scripts to load
    setTimeout(() => {
        window.manvueVoiceIntegration = new ManVueVoiceIntegration();
    }, 1000);
});

// Export for use in other modules
window.ManVueVoiceIntegration = ManVueVoiceIntegration;
