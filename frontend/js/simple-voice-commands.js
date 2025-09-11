/**
 * Simple Voice Commands for ManVue
 * 
 * A lightweight voice-to-text and text-to-command execution system
 * using the Web Speech API with simple command processing.
 */

class SimpleVoiceCommands {
    constructor() {
        this.isSupported = this.checkSupport();
        this.isListening = false;
        this.recognition = null;
        this.commands = this.initializeCommands();
        
        if (this.isSupported) {
            this.init();
        } else {
            console.warn('Voice recognition not supported in this browser');
        }
    }
    
    checkSupport() {
        return 'webkitSpeechRecognition' in window || 'SpeechRecognition' in window;
    }
    
    init() {
        console.log('🎤 Initializing Simple Voice Commands...');
        
        // Initialize speech recognition
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        this.recognition = new SpeechRecognition();
        
        // Configure recognition
        this.recognition.continuous = false;
        this.recognition.interimResults = false;
        this.recognition.lang = 'en-US';
        this.recognition.maxAlternatives = 1;
        
        // Set up event listeners
        this.setupEventListeners();
        
        console.log('✅ Simple Voice Commands initialized');
    }
    
    setupEventListeners() {
        this.recognition.onstart = () => {
            console.log('🎤 Voice recognition started');
            this.isListening = true;
            this.showStatus('Listening...');
        };
        
        this.recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript.toLowerCase().trim();
            const confidence = event.results[0][0].confidence;
            
            console.log(`🎤 Heard: "${transcript}" (${Math.round(confidence * 100)}%)`);
            this.showStatus(`Heard: "${transcript}"`);
            
            // Process the command
            this.processCommand(transcript);
        };
        
        this.recognition.onerror = (event) => {
            console.error('🎤 Voice recognition error:', event.error);
            this.showStatus(`Error: ${event.error}`, 'error');
            this.isListening = false;
        };
        
        this.recognition.onend = () => {
            console.log('🎤 Voice recognition ended');
            this.isListening = false;
            this.hideStatus();
        };
    }
    
    initializeCommands() {
        return {
            // Navigation commands
            'go home': () => this.executeCommand('navigate', 'home'),
            'go to home': () => this.executeCommand('navigate', 'home'),
            'home page': () => this.executeCommand('navigate', 'home'),
            
            // Search commands
            'search for': (query) => this.executeCommand('search', query),
            'find': (query) => this.executeCommand('search', query),
            'look for': (query) => this.executeCommand('search', query),
            
            // Cart commands
            'add to cart': () => this.executeCommand('addToCart'),
            'add this to cart': () => this.executeCommand('addToCart'),
            'open cart': () => this.executeCommand('openCart'),
            'show cart': () => this.executeCommand('openCart'),
            'view cart': () => this.executeCommand('openCart'),
            
            // Category commands
            'show shirts': () => this.executeCommand('filter', 'shirts'),
            'show t-shirts': () => this.executeCommand('filter', 'tshirts'),
            'show pants': () => this.executeCommand('filter', 'bottoms'),
            'show jeans': () => this.executeCommand('filter', 'bottoms'),
            'show jackets': () => this.executeCommand('filter', 'jackets'),
            'show accessories': () => this.executeCommand('filter', 'accessories'),
            
            // Help commands
            'help': () => this.executeCommand('help'),
            'what can you do': () => this.executeCommand('help'),
            'voice commands': () => this.executeCommand('help'),
            
            // Stop commands
            'stop': () => this.executeCommand('stop'),
            'stop listening': () => this.executeCommand('stop')
        };
    }
    
    processCommand(transcript) {
        console.log(`🔍 Processing command: "${transcript}"`);
        
        // Direct command match
        if (this.commands[transcript]) {
            console.log(`✅ Direct command match: ${transcript}`);
            this.commands[transcript]();
            return;
        }
        
        // Search for partial matches
        for (const [command, action] of Object.entries(this.commands)) {
            if (transcript.includes(command)) {
                console.log(`✅ Partial command match: ${command}`);
                
                // Extract parameters for search commands
                if (command === 'search for' || command === 'find' || command === 'look for') {
                    const query = transcript.replace(command, '').trim();
                    if (query) {
                        action(query);
                        return;
                    }
                } else {
                    action();
                    return;
                }
            }
        }
        
        // No command found
        console.log(`❌ No command found for: "${transcript}"`);
        this.showStatus(`Command not recognized: "${transcript}"`, 'error');
    }
    
    executeCommand(action, parameter = null) {
        console.log(`🚀 Executing command: ${action}${parameter ? ` with parameter: ${parameter}` : ''}`);
        
        try {
            switch (action) {
                case 'navigate':
                    if (parameter === 'home') {
                        this.navigateToHome();
                    }
                    break;
                    
                case 'search':
                    if (parameter) {
                        this.searchProducts(parameter);
                    }
                    break;
                    
                case 'addToCart':
                    this.addToCart();
                    break;
                    
                case 'openCart':
                    this.openCart();
                    break;
                    
                case 'filter':
                    if (parameter) {
                        this.filterByCategory(parameter);
                    }
                    break;
                    
                case 'help':
                    this.showHelp();
                    break;
                    
                case 'stop':
                    this.stopListening();
                    break;
                    
                default:
                    console.log(`❌ Unknown command: ${action}`);
            }
        } catch (error) {
            console.error(`❌ Error executing command ${action}:`, error);
            this.showStatus(`Error executing command: ${error.message}`, 'error');
        }
    }
    
    // Command implementations
    navigateToHome() {
        console.log('🏠 Navigating to home');
        if (typeof window.goHome === 'function') {
            window.goHome();
        } else {
            window.location.href = 'index.html';
        }
        this.showStatus('Navigated to home', 'success');
    }
    
    searchProducts(query) {
        console.log(`🔍 Searching for: ${query}`);
        if (typeof window.searchProducts === 'function') {
            window.searchProducts(query);
        } else {
            // Fallback: focus search input and set value
            const searchInput = document.getElementById('search-input');
            if (searchInput) {
                searchInput.value = query;
                searchInput.focus();
                // Trigger search
                const event = new Event('input', { bubbles: true });
                searchInput.dispatchEvent(event);
            }
        }
        this.showStatus(`Searching for: ${query}`, 'success');
    }
    
    addToCart() {
        console.log('🛒 Adding to cart');
        if (typeof window.addToCart === 'function') {
            window.addToCart();
        } else {
            // Find and click add to cart button
            const addToCartBtn = document.querySelector('.add-to-cart-btn, .btn-add-to-cart, [data-action="add-to-cart"]');
            if (addToCartBtn) {
                addToCartBtn.click();
            }
        }
        this.showStatus('Added to cart', 'success');
    }
    
    openCart() {
        console.log('🛒 Opening cart');
        if (typeof window.toggleCart === 'function') {
            window.toggleCart();
        } else {
            // Find and click cart button
            const cartBtn = document.querySelector('.cart-btn, .cart-toggle, [data-action="cart"]');
            if (cartBtn) {
                cartBtn.click();
            }
        }
        this.showStatus('Cart opened', 'success');
    }
    
    filterByCategory(category) {
        console.log(`🏷️ Filtering by category: ${category}`);
        if (typeof window.filterProducts === 'function') {
            window.filterProducts(category);
        } else {
            // Find and click category filter
            const categoryBtn = document.querySelector(`[data-category="${category}"], .category-${category}`);
            if (categoryBtn) {
                categoryBtn.click();
            }
        }
        this.showStatus(`Filtered by: ${category}`, 'success');
    }
    
    showHelp() {
        console.log('❓ Showing help');
        const helpModal = document.getElementById('voice-commands-modal');
        if (helpModal) {
            helpModal.style.display = 'block';
        } else {
            alert('Voice Commands:\n\n• "Go home" - Navigate to homepage\n• "Search for [item]" - Search products\n• "Add to cart" - Add current item to cart\n• "Open cart" - View shopping cart\n• "Show [category]" - Filter by category\n• "Help" - Show this help\n• "Stop" - Stop listening');
        }
        this.showStatus('Help displayed', 'success');
    }
    
    stopListening() {
        console.log('🛑 Stopping voice recognition');
        if (this.isListening) {
            this.recognition.stop();
        }
        this.showStatus('Voice recognition stopped', 'info');
    }
    
    // Voice control methods
    startListening() {
        if (!this.isSupported) {
            console.error('Voice recognition not supported');
            this.showStatus('Voice recognition not supported', 'error');
            return false;
        }
        
        if (this.isListening) {
            console.log('Already listening');
            return true;
        }
        
        try {
            this.recognition.start();
            return true;
        } catch (error) {
            console.error('Failed to start voice recognition:', error);
            this.showStatus('Failed to start voice recognition', 'error');
            return false;
        }
    }
    
    // UI methods
    showStatus(message, type = 'info') {
        const display = document.getElementById('voice-recognition-display');
        const textElement = document.getElementById('voice-recognized-text');
        const confidenceElement = document.getElementById('voice-confidence');
        
        if (display && textElement) {
            display.style.display = 'block';
            textElement.textContent = message;
            
            // Set color based on type
            if (type === 'error') {
                display.style.borderColor = '#ff4444';
                display.style.backgroundColor = 'rgba(255, 68, 68, 0.1)';
            } else if (type === 'success') {
                display.style.borderColor = '#44ff44';
                display.style.backgroundColor = 'rgba(68, 255, 68, 0.1)';
            } else {
                display.style.borderColor = '#e0e0e0';
                display.style.backgroundColor = 'rgba(255, 255, 255, 0.95)';
            }
            
            // Auto-hide after 3 seconds
            setTimeout(() => {
                this.hideStatus();
            }, 3000);
        }
    }
    
    hideStatus() {
        const display = document.getElementById('voice-recognition-display');
        if (display) {
            display.style.display = 'none';
        }
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Initializing Simple Voice Commands...');
    
    // Create global instance
    window.simpleVoiceCommands = new SimpleVoiceCommands();
    
    // Make it available globally
    window.startVoiceSearch = function() {
        console.log('🎤 Voice search button clicked');
        if (window.simpleVoiceCommands) {
            return window.simpleVoiceCommands.startListening();
        } else {
            console.error('Simple Voice Commands not initialized');
            return false;
        }
    };
    
    console.log('✅ Simple Voice Commands ready');
});
