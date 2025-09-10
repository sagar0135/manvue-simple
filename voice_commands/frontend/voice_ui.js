/**
 * Voice UI Components for ManVue Application
 * 
 * This module handles the user interface elements for voice commands
 */

class VoiceUI {
    constructor(options = {}) {
        this.config = {
            containerSelector: options.containerSelector || 'body',
            theme: options.theme || 'light',
            position: options.position || 'bottom-right',
            showTranscript: options.showTranscript !== false,
            showConfidence: options.showConfidence || false,
            autoHide: options.autoHide !== false,
            hideDelay: options.hideDelay || 3000,
            ...options
        };
        
        this.elements = {};
        this.isVisible = false;
        this.hideTimeout = null;
    }
    
    init() {
        this.createElements();
        this.attachEventListeners();
        this.applyTheme();
        console.log('Voice UI initialized');
    }
    
    createElements() {
        // Main container
        this.elements.container = this.createElement('div', 'voice-ui-container', {
            'data-position': this.config.position,
            'data-theme': this.config.theme
        });
        
        // Voice button
        this.elements.button = this.createElement('button', 'voice-btn', {
            'title': 'Click to start voice commands',
            'aria-label': 'Voice commands'
        });
        this.elements.button.innerHTML = `
            <svg class="voice-icon" viewBox="0 0 24 24" width="24" height="24">
                <path d="M12 1c-1.6 0-3 1.4-3 3v8c0 1.6 1.4 3 3 3s3-1.4 3-3V4c0-1.6-1.4-3-3-3z"/>
                <path d="M19 10v2c0 3.9-3.1 7-7 7s-7-3.1-7-7v-2"/>
                <path d="M12 19v4"/>
                <path d="M8 23h8"/>
            </svg>
            <div class="pulse-ring"></div>
        `;
        
        // Status indicator
        this.elements.status = this.createElement('div', 'voice-status');
        this.elements.statusText = this.createElement('span', 'voice-status-text');
        this.elements.status.appendChild(this.elements.statusText);
        
        // Transcript display
        if (this.config.showTranscript) {
            this.elements.transcript = this.createElement('div', 'voice-transcript');
            this.elements.transcriptContent = this.createElement('div', 'transcript-content');
            this.elements.transcriptInterim = this.createElement('div', 'transcript-interim');
            
            this.elements.transcript.appendChild(this.elements.transcriptContent);
            this.elements.transcript.appendChild(this.elements.transcriptInterim);
        }
        
        // Feedback panel
        this.elements.feedback = this.createElement('div', 'voice-feedback');
        
        // Help panel
        this.elements.help = this.createElement('div', 'voice-help hidden');
        this.elements.helpContent = this.createElement('div', 'help-content');
        this.elements.helpClose = this.createElement('button', 'help-close');
        this.elements.helpClose.innerHTML = '×';
        
        this.elements.help.appendChild(this.elements.helpClose);
        this.elements.help.appendChild(this.elements.helpContent);
        
        // Assemble container
        this.elements.container.appendChild(this.elements.button);
        this.elements.container.appendChild(this.elements.status);
        
        if (this.elements.transcript) {
            this.elements.container.appendChild(this.elements.transcript);
        }
        
        this.elements.container.appendChild(this.elements.feedback);
        this.elements.container.appendChild(this.elements.help);
        
        // Add to page
        const targetContainer = document.querySelector(this.config.containerSelector);
        if (targetContainer) {
            targetContainer.appendChild(this.elements.container);
        } else {
            document.body.appendChild(this.elements.container);
        }
    }
    
    createElement(tag, className, attributes = {}) {
        const element = document.createElement(tag);
        element.className = className;
        
        Object.entries(attributes).forEach(([key, value]) => {
            element.setAttribute(key, value);
        });
        
        return element;
    }
    
    attachEventListeners() {
        // Voice button click
        this.elements.button.addEventListener('click', () => {
            this.onVoiceButtonClick();
        });
        
        // Help close button
        if (this.elements.helpClose) {
            this.elements.helpClose.addEventListener('click', () => {
                this.hideVoiceHelp();
            });
        }
        
        // Keyboard shortcuts
        document.addEventListener('keydown', (event) => {
            if (event.ctrlKey && event.shiftKey && event.code === 'KeyV') {
                event.preventDefault();
                this.onVoiceButtonClick();
            }
            
            if (event.code === 'Escape' && this.elements.help && !this.elements.help.classList.contains('hidden')) {
                this.hideVoiceHelp();
            }
        });
    }
    
    onVoiceButtonClick() {
        // This will be called by the parent VoiceInterface
        const event = new CustomEvent('voiceButtonClick');
        this.elements.button.dispatchEvent(event);
    }
    
    setListeningState(isListening) {
        if (isListening) {
            this.elements.button.classList.add('listening');
            this.elements.container.classList.add('active');
            this.setStatusText('Listening...', 'listening');
            this.show();
        } else {
            this.elements.button.classList.remove('listening');
            this.elements.container.classList.remove('active');
            this.setStatusText('Click to speak', 'idle');
            
            if (this.config.autoHide) {
                this.scheduleHide();
            }
        }
    }
    
    setStatusText(text, state = 'idle') {
        if (this.elements.statusText) {
            this.elements.statusText.textContent = text;
            this.elements.status.className = `voice-status ${state}`;
        }
    }
    
    showInterimResult(text) {
        if (this.elements.transcriptInterim) {
            this.elements.transcriptInterim.textContent = text;
            this.elements.transcriptInterim.style.opacity = '0.7';
            this.show();
        }
    }
    
    showFinalResult(text, confidence) {
        if (this.elements.transcriptContent) {
            const resultElement = this.createElement('div', 'transcript-result');
            
            if (this.config.showConfidence) {
                resultElement.innerHTML = `
                    <span class="transcript-text">${text}</span>
                    <span class="confidence">${Math.round(confidence * 100)}%</span>
                `;
            } else {
                resultElement.textContent = text;
            }
            
            this.elements.transcriptContent.appendChild(resultElement);
            
            // Limit number of results shown
            const results = this.elements.transcriptContent.querySelectorAll('.transcript-result');
            if (results.length > 5) {
                results[0].remove();
            }
        }
        
        // Clear interim result
        if (this.elements.transcriptInterim) {
            this.elements.transcriptInterim.textContent = '';
        }
    }
    
    showFeedback(message, type = 'info') {
        const feedbackElement = this.createElement('div', `voice-feedback-item ${type}`);
        feedbackElement.textContent = message;
        
        this.elements.feedback.appendChild(feedbackElement);
        this.show();
        
        // Auto-remove feedback after delay
        setTimeout(() => {
            if (feedbackElement.parentNode) {
                feedbackElement.remove();
            }
        }, 3000);
        
        // Limit number of feedback items
        const items = this.elements.feedback.querySelectorAll('.voice-feedback-item');
        if (items.length > 3) {
            items[0].remove();
        }
    }
    
    showError(message) {
        this.showFeedback(message, 'error');
        this.setStatusText('Error occurred', 'error');
    }
    
    showVoiceHelp() {
        if (this.elements.help) {
            this.elements.helpContent.innerHTML = this.getHelpContent();
            this.elements.help.classList.remove('hidden');
            this.show();
        }
    }
    
    hideVoiceHelp() {
        if (this.elements.help) {
            this.elements.help.classList.add('hidden');
        }
    }
    
    getHelpContent() {
        return `
            <h3>Voice Commands</h3>
            <div class="help-section">
                <h4>Navigation</h4>
                <ul>
                    <li>"Go home" - Return to main page</li>
                    <li>"Show products" - View product catalog</li>
                    <li>"Open cart" - View shopping cart</li>
                </ul>
            </div>
            <div class="help-section">
                <h4>Search</h4>
                <ul>
                    <li>"Search for [product]" - Find specific products</li>
                    <li>"Show me [color] [item]" - Filter by color</li>
                    <li>"Find [category] items" - Browse categories</li>
                </ul>
            </div>
            <div class="help-section">
                <h4>Actions</h4>
                <ul>
                    <li>"Add to cart" - Add current product</li>
                    <li>"Show details" - View product information</li>
                    <li>"Filter by price" - Apply price filters</li>
                </ul>
            </div>
            <div class="help-section">
                <h4>Tips</h4>
                <ul>
                    <li>Speak clearly and at normal pace</li>
                    <li>Use Ctrl+Shift+V to toggle voice recognition</li>
                    <li>Say "help" anytime for this guide</li>
                </ul>
            </div>
        `;
    }
    
    show() {
        if (!this.isVisible) {
            this.elements.container.classList.add('visible');
            this.isVisible = true;
        }
        
        // Clear any pending hide
        if (this.hideTimeout) {
            clearTimeout(this.hideTimeout);
            this.hideTimeout = null;
        }
    }
    
    hide() {
        if (this.isVisible) {
            this.elements.container.classList.remove('visible');
            this.isVisible = false;
        }
    }
    
    scheduleHide() {
        if (this.hideTimeout) {
            clearTimeout(this.hideTimeout);
        }
        
        this.hideTimeout = setTimeout(() => {
            this.hide();
        }, this.config.hideDelay);
    }
    
    applyTheme() {
        // Theme will be applied via CSS based on data-theme attribute
        document.documentElement.setAttribute('data-voice-theme', this.config.theme);
    }
    
    setTheme(theme) {
        this.config.theme = theme;
        this.elements.container.setAttribute('data-theme', theme);
        this.applyTheme();
    }
    
    setPosition(position) {
        this.config.position = position;
        this.elements.container.setAttribute('data-position', position);
    }
    
    destroy() {
        if (this.hideTimeout) {
            clearTimeout(this.hideTimeout);
        }
        
        if (this.elements.container && this.elements.container.parentNode) {
            this.elements.container.parentNode.removeChild(this.elements.container);
        }
        
        this.elements = {};
        this.isVisible = false;
    }
}

/**
 * Voice Command Processor for Frontend
 */
class VoiceCommandProcessor {
    constructor() {
        this.commands = this.loadCommands();
        this.context = {};
    }
    
    loadCommands() {
        // Basic command patterns - would normally be loaded from server
        return {
            navigation: [
                { patterns: ['go home', 'home page', 'main page'], action: 'navigate_to_page', params: { url: '/index.html' } },
                { patterns: ['show products', 'view products', 'product catalog'], action: 'navigate_to_page', params: { url: '/index.html#products' } },
                { patterns: ['open cart', 'shopping cart', 'view cart'], action: 'open_cart' },
            ],
            search: [
                { patterns: ['search for *', 'find *', 'look for *'], action: 'search_products', paramNames: ['query'] },
                { patterns: ['show * items', 'find * products'], action: 'filter_by_category', paramNames: ['category'] },
                { patterns: ['show * *', 'find * *'], action: 'search_products', paramNames: ['color', 'item'] },
            ],
            actions: [
                { patterns: ['add to cart', 'buy this', 'purchase'], action: 'add_to_cart' },
                { patterns: ['show details', 'product details', 'more info'], action: 'show_product_details' },
                { patterns: ['help', 'voice help', 'what can i say'], action: 'show_voice_help' },
                { patterns: ['stop listening', 'turn off voice'], action: 'stop_voice_recognition' },
                { patterns: ['start listening', 'turn on voice'], action: 'start_voice_recognition' },
            ]
        };
    }
    
    processCommand(text, confidence) {
        text = text.toLowerCase().trim();
        
        // Try to match against all command categories
        for (const [category, commandList] of Object.entries(this.commands)) {
            for (const command of commandList) {
                const match = this.matchPattern(text, command);
                if (match) {
                    return {
                        action: command.action,
                        parameters: { ...command.params, ...match.parameters },
                        confidence: confidence,
                        matchConfidence: match.confidence,
                        category: category,
                        originalText: text
                    };
                }
            }
        }
        
        // Fallback to general search
        if (this.looksLikeSearch(text)) {
            return {
                action: 'search_products',
                parameters: { query: this.extractSearchTerms(text) },
                confidence: confidence,
                matchConfidence: 0.7,
                category: 'search',
                originalText: text
            };
        }
        
        return null;
    }
    
    matchPattern(text, command) {
        for (const pattern of command.patterns) {
            const match = this.matchSinglePattern(text, pattern, command.paramNames);
            if (match) {
                return match;
            }
        }
        return null;
    }
    
    matchSinglePattern(text, pattern, paramNames = []) {
        // Simple pattern matching with wildcards
        const patternRegex = pattern.replace(/\*/g, '(.+?)');
        const regex = new RegExp(`^${patternRegex}$`, 'i');
        const match = text.match(regex);
        
        if (match) {
            const parameters = {};
            
            // Extract parameters from wildcards
            if (paramNames && match.length > 1) {
                for (let i = 0; i < paramNames.length && i < match.length - 1; i++) {
                    parameters[paramNames[i]] = match[i + 1].trim();
                }
            }
            
            return {
                confidence: 0.9,
                parameters: parameters
            };
        }
        
        // Fuzzy matching fallback
        const similarity = this.calculateSimilarity(text, pattern);
        if (similarity > 0.7) {
            return {
                confidence: similarity,
                parameters: {}
            };
        }
        
        return null;
    }
    
    calculateSimilarity(str1, str2) {
        // Simple similarity calculation
        const longer = str1.length > str2.length ? str1 : str2;
        const shorter = str1.length > str2.length ? str2 : str1;
        
        if (longer.length === 0) {
            return 1.0;
        }
        
        const editDistance = this.levenshteinDistance(longer, shorter);
        return (longer.length - editDistance) / longer.length;
    }
    
    levenshteinDistance(str1, str2) {
        const matrix = [];
        
        for (let i = 0; i <= str2.length; i++) {
            matrix[i] = [i];
        }
        
        for (let j = 0; j <= str1.length; j++) {
            matrix[0][j] = j;
        }
        
        for (let i = 1; i <= str2.length; i++) {
            for (let j = 1; j <= str1.length; j++) {
                if (str2.charAt(i - 1) === str1.charAt(j - 1)) {
                    matrix[i][j] = matrix[i - 1][j - 1];
                } else {
                    matrix[i][j] = Math.min(
                        matrix[i - 1][j - 1] + 1,
                        matrix[i][j - 1] + 1,
                        matrix[i - 1][j] + 1
                    );
                }
            }
        }
        
        return matrix[str2.length][str1.length];
    }
    
    looksLikeSearch(text) {
        const searchIndicators = ['search', 'find', 'look', 'show', 'get', 'where'];
        return searchIndicators.some(indicator => text.includes(indicator));
    }
    
    extractSearchTerms(text) {
        // Remove common command words
        const stopWords = ['search', 'for', 'find', 'look', 'show', 'me', 'get', 'where', 'is', 'the'];
        return text.split(' ')
            .filter(word => !stopWords.includes(word))
            .join(' ')
            .trim();
    }
    
    addCustomCommand(pattern, action, parameters = {}) {
        if (!this.commands.custom) {
            this.commands.custom = [];
        }
        
        this.commands.custom.push({
            patterns: [pattern],
            action: action,
            params: parameters
        });
    }
}
