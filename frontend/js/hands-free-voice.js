/**
 * Hands-Free Voice Commands for ManVue
 * 
 * A truly hands-free voice system that automatically listens
 * and responds to voice commands without any button clicks.
 */

class HandsFreeVoice {
    constructor() {
        this.isSupported = this.checkSupport();
        this.isListening = false;
        this.isActive = false;
        this.recognition = null;
        this.wakeWord = 'hey manvue';
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
        console.log('🎤 Initializing Hands-Free Voice Commands...');
        
        // Initialize speech recognition
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        this.recognition = new SpeechRecognition();
        
        // Configure for continuous listening
        this.recognition.continuous = true;
        this.recognition.interimResults = true;
        this.recognition.lang = 'en-US';
        this.recognition.maxAlternatives = 1;
        
        // Set up event listeners
        this.setupEventListeners();
        
        // Start listening automatically
        this.startListening();
        
        console.log('✅ Hands-Free Voice Commands initialized and listening');
    }
    
    setupEventListeners() {
        this.recognition.onstart = () => {
            console.log('🎤 Hands-free voice recognition started');
            this.isListening = true;
            this.showStatus('Listening for "Hey MANVUE"...', 'info');
        };
        
        this.recognition.onresult = (event) => {
            let finalTranscript = '';
            let interimTranscript = '';
            
            // Process all results
            for (let i = event.resultIndex; i < event.results.length; i++) {
                const transcript = event.results[i][0].transcript.toLowerCase();
                
                if (event.results[i].isFinal) {
                    finalTranscript += transcript;
                } else {
                    interimTranscript += transcript;
                }
            }
            
            // Show interim results
            if (interimTranscript) {
                this.showStatus(`Hearing: "${interimTranscript}"`, 'info');
            }
            
            // Process final results
            if (finalTranscript) {
                console.log(`🎤 Final transcript: "${finalTranscript}"`);
                this.processTranscript(finalTranscript);
            }
        };
        
        this.recognition.onerror = (event) => {
            console.error('🎤 Voice recognition error:', event.error);
            if (event.error !== 'no-speech') {
                this.showStatus(`Error: ${event.error}`, 'error');
            }
        };
        
        this.recognition.onend = () => {
            console.log('🎤 Voice recognition ended, restarting...');
            this.isListening = false;
            
            // Automatically restart listening for hands-free operation
            setTimeout(() => {
                if (!this.isListening) {
                    this.startListening();
                }
            }, 1000);
        };
    }
    
    initializeCommands() {
        return {
            // Navigation
            'go home': () => this.executeCommand('navigate', 'home'),
            'home': () => this.executeCommand('navigate', 'home'),
            
            // Search
            'search': (query) => this.executeCommand('search', query),
            'find': (query) => this.executeCommand('search', query),
            'look for': (query) => this.executeCommand('search', query),
            
            // Cart
            'add to cart': () => this.executeCommand('addToCart'),
            'add this': () => this.executeCommand('addToCart'),
            'cart': () => this.executeCommand('openCart'),
            'show cart': () => this.executeCommand('openCart'),
            
            // Categories
            'shirts': () => this.executeCommand('filter', 'shirts'),
            't-shirts': () => this.executeCommand('filter', 'tshirts'),
            'pants': () => this.executeCommand('filter', 'bottoms'),
            'jeans': () => this.executeCommand('filter', 'bottoms'),
            'jackets': () => this.executeCommand('filter', 'jackets'),
            'accessories': () => this.executeCommand('filter', 'accessories'),
            
            // Help
            'help': () => this.executeCommand('help'),
            'what can you do': () => this.executeCommand('help'),
            
            // Control
            'stop': () => this.executeCommand('stop'),
            'sleep': () => this.executeCommand('sleep')
        };
    }
    
    processTranscript(transcript) {
        console.log(`🔍 Processing: "${transcript}"`);
        
        // Check for wake word
        if (transcript.includes(this.wakeWord)) {
            console.log('👂 Wake word detected!');
            this.isActive = true;
            this.showStatus('MANVUE is listening...', 'success');
            
            // Extract command after wake word
            const command = transcript.replace(this.wakeWord, '').trim();
            if (command) {
                this.processCommand(command);
            }
            return;
        }
        
        // If already active, process any command
        if (this.isActive) {
            this.processCommand(transcript);
        }
    }
    
    processCommand(command) {
        console.log(`🎯 Processing command: "${command}"`);
        
        // Direct command match
        if (this.commands[command]) {
            console.log(`✅ Direct match: ${command}`);
            this.commands[command]();
            this.isActive = false;
            return;
        }
        
        // Search for partial matches
        for (const [cmd, action] of Object.entries(this.commands)) {
            if (command.includes(cmd)) {
                console.log(`✅ Partial match: ${cmd}`);
                
                // Extract parameters for search commands
                if (cmd === 'search' || cmd === 'find' || cmd === 'look for') {
                    const query = command.replace(cmd, '').trim();
                    if (query) {
                        action(query);
                        this.isActive = false;
                        return;
                    }
                } else {
                    action();
                    this.isActive = false;
                    return;
                }
            }
        }
        
        // No command found
        console.log(`❌ No command found for: "${command}"`);
        this.showStatus(`Command not recognized: "${command}"`, 'error');
        this.isActive = false;
    }
    
    executeCommand(action, parameter = null) {
        console.log(`🚀 Executing: ${action}${parameter ? ` (${parameter})` : ''}`);
        
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
                    
                case 'sleep':
                    this.isActive = false;
                    this.showStatus('MANVUE is sleeping. Say "Hey MANVUE" to wake up.', 'info');
                    break;
                    
                default:
                    console.log(`❌ Unknown command: ${action}`);
            }
        } catch (error) {
            console.error(`❌ Error executing ${action}:`, error);
            this.showStatus(`Error: ${error.message}`, 'error');
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
            const searchInput = document.getElementById('search-input');
            if (searchInput) {
                searchInput.value = query;
                searchInput.focus();
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
            const cartBtn = document.querySelector('.cart-btn, .cart-toggle, [data-action="cart"]');
            if (cartBtn) {
                cartBtn.click();
            }
        }
        this.showStatus('Cart opened', 'success');
    }
    
    filterByCategory(category) {
        console.log(`🏷️ Filtering by: ${category}`);
        if (typeof window.filterProducts === 'function') {
            window.filterProducts(category);
        } else {
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
            alert('Hands-Free Voice Commands:\n\nSay "Hey MANVUE" then:\n\n• "Go home" - Navigate to homepage\n• "Search [item]" - Search products\n• "Add to cart" - Add current item\n• "Cart" - Open shopping cart\n• "Shirts" - Show shirts\n• "Help" - Show this help\n• "Sleep" - Stop listening\n• "Stop" - Stop voice system');
        }
        this.showStatus('Help displayed', 'success');
    }
    
    stopListening() {
        console.log('🛑 Stopping hands-free voice system');
        this.recognition.stop();
        this.isListening = false;
        this.isActive = false;
        this.showStatus('Voice system stopped', 'info');
    }
    
    startListening() {
        if (!this.isSupported) {
            console.error('Voice recognition not supported');
            return false;
        }
        
        if (this.isListening) {
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
                if (display.style.display !== 'none') {
                    display.style.display = 'none';
                }
            }, 3000);
        }
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Initializing Hands-Free Voice Commands...');
    
    // Create global instance
    window.handsFreeVoice = new HandsFreeVoice();
    
    console.log('✅ Hands-Free Voice Commands ready - Just say "Hey MANVUE"!');
});
