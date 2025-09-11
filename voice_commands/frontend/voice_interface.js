/**
 * Voice Interface for ManVue Application
 * 
 * This module provides client-side voice recognition and command processing
 * using the Web Speech API.
 */

class VoiceInterface {
    constructor(options = {}) {
        console.log(`🔧 FUNCTION CALLED: VoiceInterface constructor`);
        console.log(`🎤 VoiceInterface constructor called with options:`, options);
        
        this.isSupported = this.checkSupport();
        console.log(`🔍 Speech recognition supported: ${this.isSupported}`);
        
        this.isListening = false;
        this.recognition = null;
        this.config = {
            language: options.language || 'en-US',
            continuous: options.continuous !== false,
            interimResults: options.interimResults !== false,
            maxAlternatives: options.maxAlternatives || 3,
            autoStart: options.autoStart || false,
            ...options
        };
        console.log(`⚙️ Voice config:`, this.config);
        
        this.callbacks = {
            onResult: options.onResult || this.defaultResultHandler.bind(this),
            onError: options.onError || this.defaultErrorHandler.bind(this),
            onStart: options.onStart || (() => {}),
            onEnd: options.onEnd || (() => {}),
            onNoMatch: options.onNoMatch || (() => {})
        };
        console.log(`📞 Callbacks configured:`, Object.keys(this.callbacks));
        
        this.commandProcessor = new VoiceCommandProcessor();
        this.ui = new VoiceUI();
        console.log(`🔧 Command processor and UI initialized`);
        
        this.init();
        console.log(`🏁 FUNCTION COMPLETED: VoiceInterface constructor`);
    }
    
    checkSupport() {
        console.log(`🔧 FUNCTION CALLED: checkSupport()`);
        
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            console.warn('Speech recognition not supported in this browser');
            console.log(`🏁 FUNCTION COMPLETED: checkSupport (not supported)`);
            return false;
        }
        
        console.log(`✅ Speech recognition is supported`);
        console.log(`🏁 FUNCTION COMPLETED: checkSupport (supported)`);
        return true;
    }
    
    init() {
        console.log(`🔧 FUNCTION CALLED: init()`);
        
        if (!this.isSupported) {
            console.log(`❌ Speech recognition not supported, showing error`);
            this.ui.showError('Voice commands are not supported in this browser');
            console.log(`🏁 FUNCTION COMPLETED: init (not supported)`);
            return;
        }
        
        console.log(`🔧 Initializing speech recognition`);
        // Initialize speech recognition
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        this.recognition = new SpeechRecognition();
        console.log(`✅ Speech recognition object created`);
        
        console.log(`⚙️ Configuring recognition settings`);
        // Configure recognition
        this.recognition.continuous = this.config.continuous;
        this.recognition.interimResults = this.config.interimResults;
        this.recognition.lang = this.config.language;
        this.recognition.maxAlternatives = this.config.maxAlternatives;
        console.log(`✅ Recognition configured:`, {
            continuous: this.recognition.continuous,
            interimResults: this.recognition.interimResults,
            lang: this.recognition.lang,
            maxAlternatives: this.recognition.maxAlternatives
        });
        
        console.log(`🔧 Setting up event listeners`);
        // Set up event listeners
        this.setupEventListeners();
        
        console.log(`🔧 Initializing UI`);
        // Initialize UI
        this.ui.init();
        
        // Auto-start if configured
        if (this.config.autoStart) {
            console.log(`🔧 Auto-start enabled, starting listening`);
            this.startListening();
        } else {
            console.log(`⏸️ Auto-start disabled`);
        }
        
        console.log('Voice interface initialized');
        console.log(`🏁 FUNCTION COMPLETED: init`);
    }
    
    setupEventListeners() {
        if (!this.recognition) return;
        
        this.recognition.onstart = () => {
            this.isListening = true;
            this.ui.setListeningState(true);
            this.callbacks.onStart();
            console.log('Voice recognition started');
        };
        
        this.recognition.onend = () => {
            this.isListening = false;
            this.ui.setListeningState(false);
            this.callbacks.onEnd();
            console.log('Voice recognition ended');
        };
        
        this.recognition.onresult = (event) => {
            this.handleResults(event);
        };
        
        this.recognition.onerror = (event) => {
            this.handleError(event);
        };
        
        this.recognition.onnomatch = () => {
            this.ui.showFeedback('No command recognized', 'warning');
            this.callbacks.onNoMatch();
        };
    }
    
    handleResults(event) {
        let finalTranscript = '';
        let interimTranscript = '';
        
        for (let i = event.resultIndex; i < event.results.length; ++i) {
            const result = event.results[i];
            const transcript = result[0].transcript;
            
            if (result.isFinal) {
                finalTranscript += transcript;
            } else {
                interimTranscript += transcript;
            }
        }
        
        // Update UI with interim results
        if (interimTranscript) {
            this.ui.showInterimResult(interimTranscript);
        }
        
        // Process final results
        if (finalTranscript) {
            const confidence = event.results[event.resultIndex][0].confidence;
            this.processFinalResult(finalTranscript.trim(), confidence);
        }
    }
    
    processFinalResult(transcript, confidence) {
        console.log('Final result:', transcript, 'Confidence:', confidence);
        
        this.ui.showFinalResult(transcript, confidence);
        
        // Process command
        const commandResult = this.commandProcessor.processCommand(transcript, confidence);
        
        if (commandResult) {
            this.executeCommand(commandResult);
            this.ui.showFeedback(`Executing: ${commandResult.action}`, 'success');
        } else {
            this.ui.showFeedback('Command not recognized', 'warning');
        }
        
        // Call result callback
        this.callbacks.onResult(transcript, confidence, commandResult);
    }
    
    handleError(event) {
        console.error('Speech recognition error:', event.error);
        
        let errorMessage = 'Voice recognition error';
        switch (event.error) {
            case 'no-speech':
                errorMessage = 'No speech detected';
                break;
            case 'audio-capture':
                errorMessage = 'Microphone access denied';
                break;
            case 'not-allowed':
                errorMessage = 'Microphone permission required';
                break;
            case 'network':
                errorMessage = 'Network error occurred';
                break;
        }
        
        this.ui.showError(errorMessage);
        this.callbacks.onError(event.error, errorMessage);
    }
    
    executeCommand(commandResult) {
        const { action, parameters } = commandResult;
        
        try {
            switch (action) {
                case 'navigate_to_page':
                    this.navigateToPage(parameters);
                    break;
                case 'search_products':
                    this.searchProducts(parameters);
                    break;
                case 'open_cart':
                    this.openCart();
                    break;
                case 'add_to_cart':
                    this.addToCart(parameters);
                    break;
                case 'show_product_details':
                    this.showProductDetails(parameters);
                    break;
                case 'filter_by_category':
                    this.filterByCategory(parameters);
                    break;
                case 'filter_by_color':
                    this.filterByColor(parameters);
                    break;
                case 'show_voice_help':
                    this.showVoiceHelp();
                    break;
                case 'stop_voice_recognition':
                    this.stopListening();
                    break;
                case 'start_voice_recognition':
                    this.startListening();
                    break;
                default:
                    console.warn('Unknown action:', action);
            }
        } catch (error) {
            console.error('Error executing command:', error);
            this.ui.showError('Failed to execute command');
        }
    }
    
    // Command execution methods
    navigateToPage(parameters) {
        const { url, page } = parameters;
        if (url) {
            window.location.href = url;
        } else {
            console.warn('No URL specified for navigation');
        }
    }
    
    searchProducts(parameters) {
        const { query } = parameters;
        if (query && typeof window.searchProducts === 'function') {
            window.searchProducts(query);
        } else {
            // Fallback: try to use existing search functionality
            const searchInput = document.querySelector('#search-input, .search-input, input[type=\"search\"]');
            if (searchInput) {
                searchInput.value = query;
                searchInput.dispatchEvent(new Event('input'));
                
                // Try to submit search
                const searchForm = searchInput.closest('form');
                if (searchForm) {
                    searchForm.dispatchEvent(new Event('submit'));
                }
            }
        }
    }
    
    openCart() {
        if (typeof window.openCart === 'function') {
            window.openCart();
        } else {
            // Try to find and click cart button
            const cartButton = document.querySelector('.cart-btn, #cart-btn, .shopping-cart');
            if (cartButton) {
                cartButton.click();
            }
        }
    }
    
    addToCart(parameters) {
        if (typeof window.addToCart === 'function') {
            window.addToCart(parameters);
        } else {
            // Try to find add to cart button
            const addButton = document.querySelector('.add-to-cart, #add-to-cart, .btn-add-cart');
            if (addButton) {
                addButton.click();
            }
        }
    }
    
    showProductDetails(parameters) {
        // This would typically show a modal or navigate to product page
        console.log('Show product details:', parameters);
    }
    
    filterByCategory(parameters) {
        const { category } = parameters;
        if (category && typeof window.filterByCategory === 'function') {
            window.filterByCategory(category);
        }
    }
    
    filterByColor(parameters) {
        const { color } = parameters;
        if (color && typeof window.filterByColor === 'function') {
            window.filterByColor(color);
        }
    }
    
    showVoiceHelp() {
        this.ui.showVoiceHelp();
    }
    
    // Public API methods
    startListening() {
        console.log(`🔧 FUNCTION CALLED: startListening()`);
        
        if (!this.isSupported || this.isListening) {
            console.log(`❌ Cannot start listening: supported=${this.isSupported}, listening=${this.isListening}`);
            console.log(`🏁 FUNCTION COMPLETED: startListening (cannot start)`);
            return false;
        }
        
        console.log(`🎤 Starting voice recognition...`);
        try {
            this.recognition.start();
            console.log(`✅ Voice recognition started successfully`);
            console.log(`🏁 FUNCTION COMPLETED: startListening (success)`);
            return true;
        } catch (error) {
            console.error('Failed to start voice recognition:', error);
            console.log(`❌ Voice recognition start failed:`, error.message);
            this.ui.showError('Failed to start voice recognition');
            console.log(`🏁 FUNCTION COMPLETED: startListening (error)`);
            return false;
        }
    }
    
    stopListening() {
        if (!this.isSupported || !this.isListening) {
            return false;
        }
        
        try {
            this.recognition.stop();
            return true;
        } catch (error) {
            console.error('Failed to stop voice recognition:', error);
            return false;
        }
    }
    
    toggleListening() {
        return this.isListening ? this.stopListening() : this.startListening();
    }
    
    setLanguage(language) {
        this.config.language = language;
        if (this.recognition) {
            this.recognition.lang = language;
        }
    }
    
    isCurrentlyListening() {
        return this.isListening;
    }
    
    getSupported() {
        return this.isSupported;
    }
    
    // Default event handlers
    defaultResultHandler(transcript, confidence, commandResult) {
        console.log('Voice result:', { transcript, confidence, commandResult });
    }
    
    defaultErrorHandler(error, message) {
        console.error('Voice error:', error, message);
    }
    
    // Utility methods
    addCommand(pattern, action, parameters = {}) {
        this.commandProcessor.addCustomCommand(pattern, action, parameters);
    }
    
    setCallback(event, callback) {
        if (this.callbacks.hasOwnProperty(`on${event.charAt(0).toUpperCase()}${event.slice(1)}`)) {
            this.callbacks[`on${event.charAt(0).toUpperCase()}${event.slice(1)}`] = callback;
        }
    }
}
