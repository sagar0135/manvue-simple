/**
 * Simple Voice Commands Fix for ManVue
 * 
 * This is a simplified, working version that fixes the unresponsive voice commands
 */

(function() {
    'use strict';
    
    console.log('🎤 Loading Simple Voice Fix...');
    
    // Simple action handler registry
    const actionHandlers = new Map();
    
    // Register an action handler (this is the equivalent of register_action_handler)
    function registerActionHandler(action, handler) {
        console.log(`🔧 FUNCTION CALLED: registerActionHandler(${action})`);

        actionHandlers.set(action, handler);
        console.log(`✅ Registered handler for action: ${action}`);
        console.log(`📊 Total handlers registered: ${actionHandlers.size}`);
        console.log(`🏁 FUNCTION COMPLETED: registerActionHandler`);
    }
    
    // Execute an action
    function executeAction(action, parameters) {
        console.log(`🔧 FUNCTION CALLED: executeAction(${action})`);
        console.log(`🚀 EXECUTE ACTION CALLED: ${action}`);
        alert(`🚀 EXECUTE ACTION CALLED: ${action}`);
        
        const handler = actionHandlers.get(action);
        console.log(`🔍 Handler found: ${handler ? 'YES' : 'NO'}`);
        
        if (handler) {
            console.log(`🎯 Executing action: ${action}`, parameters);
            alert(`🎯 EXECUTING ACTION: ${action}`);
            try {
                const result = handler(parameters);
                console.log(`✅ Action completed: ${action}`);
                console.log(`📤 Action result:`, result);
                alert(`✅ ACTION COMPLETED: ${action}`);
                console.log(`🏁 FUNCTION COMPLETED: executeAction`);
                return result;
            } catch (error) {
                console.error(`❌ Action failed: ${action}`, error);
                alert(`❌ ACTION FAILED: ${action} - ${error.message}`);
                console.log(`🏁 FUNCTION COMPLETED: executeAction (with error)`);
                return false;
            }
        } else {
            console.warn(`⚠️  No handler for action: ${action}`);
            alert(`⚠️ NO HANDLER FOR ACTION: ${action}`);
            console.log(`🏁 FUNCTION COMPLETED: executeAction (no handler)`);
            return false;
        }
    }
    
    // Register ManVue action handlers
    function setupManVueHandlers() {
        console.log(`🔧 FUNCTION CALLED: setupManVueHandlers()`);
        console.log('🔧 Setting up ManVue action handlers...');
        
        // Navigation actions
        registerActionHandler('navigate_to_page', function(params) {
            console.log('🎯 EXECUTING: navigate_to_page command');
            alert('🎯 VOICE COMMAND EXECUTED: navigate_to_page');
            
            const page = params.page || params.url;
            console.log('📄 Navigation target:', page);
            
            if (page === 'home' || page === '/index.html') {
                if (typeof window.goHome === 'function') {
                    console.log('🏠 Calling goHome() function');
                    window.goHome();
                    showFeedback('Navigated to home');
                    alert('✅ SUCCESS: goHome() function called');
                    return true;
                } else if (typeof window.showSection === 'function') {
                    console.log('🏠 Calling showSection("home") function');
                    window.showSection('home');
                    showFeedback('Showing home section');
                    alert('✅ SUCCESS: showSection("home") function called');
                    return true;
                }
            } else if (page === 'products') {
                if (typeof window.showSection === 'function') {
                    console.log('🛍️ Calling showSection("products") function');
                    window.showSection('products');
                    showFeedback('Showing products');
                    alert('✅ SUCCESS: showSection("products") function called');
                    return true;
                }
            }
            
            console.log('❌ Navigation failed - no suitable function found');
            alert('❌ FAILED: No navigation function available');
            return false;
        });
        
        // Search actions
        registerActionHandler('search_products', function(params) {
            console.log('🎯 EXECUTING: search_products command');
            alert('🎯 VOICE COMMAND EXECUTED: search_products');
            
            let query = params.query || '';
            console.log('🔍 Search parameters:', params);
            
            // Handle color + item combinations
            if (params.color && params.item) {
                query = `${params.color} ${params.item}`;
                console.log('🎨 Color + item search:', query);
            } else if (params.color) {
                query = params.color;
                console.log('🎨 Color search:', query);
            } else if (params.category) {
                query = params.category;
                console.log('📂 Category search:', query);
            }
            
            console.log('🔍 Final search query:', query);
            
            if (query && typeof window.searchProducts === 'function') {
                console.log('✅ searchProducts function available');
                
                // Set search input if it exists
                const searchInput = document.querySelector('#search-input, .search-input, input[type="search"], #main-search-input');
                if (searchInput) {
                    console.log('📝 Setting search input value:', query);
                    searchInput.value = query;
                } else {
                    console.log('⚠️ No search input found');
                }
                
                console.log('🚀 Calling searchProducts with query:', query);
                window.searchProducts(query);
                showFeedback(`Searching for: ${query}`);
                alert(`✅ SUCCESS: searchProducts("${query}") function called`);
                return true;
            }
            
            console.log('❌ Search failed - no query or function not available');
            alert('❌ FAILED: Search function not available or no query provided');
            return false;
        });
        
        // Cart actions
        registerActionHandler('open_cart', function(params) {
            console.log('🎯 EXECUTING: open_cart command');
            alert('🎯 VOICE COMMAND EXECUTED: open_cart');
            
            if (typeof window.toggleCart === 'function') {
                console.log('🛒 Calling toggleCart() function');
                window.toggleCart();
                showFeedback('Opening cart');
                alert('✅ SUCCESS: toggleCart() function called');
                return true;
            }
            
            console.log('❌ Cart toggle failed - function not available');
            alert('❌ FAILED: toggleCart function not available');
            return false;
        });
        
        registerActionHandler('add_to_cart', function(params) {
            console.log('🎯 EXECUTING: add_to_cart command');
            alert('🎯 VOICE COMMAND EXECUTED: add_to_cart');
            
            // Try to find current product ID
            let productId = getCurrentProductId();
            console.log('🛍️ Current product ID:', productId);
            
            if (productId && typeof window.addToCart === 'function') {
                console.log('✅ addToCart function available');
                console.log('🚀 Calling addToCart with productId:', productId);
                window.addToCart(productId);
                showFeedback('Added to cart');
                alert(`✅ SUCCESS: addToCart(${productId}) function called`);
                return true;
            } else {
                console.log('❌ Add to cart failed - no product or function not available');
                showFeedback('No product selected', 'error');
                alert('❌ FAILED: No product selected or addToCart function not available');
                return false;
            }
        });
        
        // Filter actions
        registerActionHandler('filter_by_category', function(params) {
            console.log('🎯 EXECUTING: filter_by_category command');
            alert('🎯 VOICE COMMAND EXECUTED: filter_by_category');
            
            const category = params.category;
            console.log('📂 Category to filter:', category);
            
            if (category && typeof window.filterProducts === 'function') {
                console.log('✅ filterProducts function available');
                console.log('🚀 Calling filterProducts with category:', category);
                window.filterProducts(category);
                showFeedback(`Filtering by: ${category}`);
                alert(`✅ SUCCESS: filterProducts("${category}") function called`);
                return true;
            }
            
            console.log('❌ Category filter failed - no category or function not available');
            alert('❌ FAILED: No category provided or filterProducts function not available');
            return false;
        });
        
        registerActionHandler('filter_by_color', function(params) {
            console.log('🎯 EXECUTING: filter_by_color command');
            alert('🎯 VOICE COMMAND EXECUTED: filter_by_color');
            
            const color = params.color;
            console.log('🎨 Color to filter:', color);
            
            if (color) {
                if (typeof window.searchByColor === 'function') {
                    console.log('✅ searchByColor function available');
                    console.log('🚀 Calling searchByColor with color:', color);
                    window.searchByColor(color);
                    showFeedback(`Searching for ${color} items`);
                    alert(`✅ SUCCESS: searchByColor("${color}") function called`);
                    return true;
                } else if (typeof window.searchProducts === 'function') {
                    console.log('✅ searchProducts function available (fallback)');
                    console.log('🚀 Calling searchProducts with color:', color);
                    window.searchProducts(color);
                    showFeedback(`Searching for ${color} items`);
                    alert(`✅ SUCCESS: searchProducts("${color}") function called`);
                    return true;
                }
            }
            
            console.log('❌ Color filter failed - no color or functions not available');
            alert('❌ FAILED: No color provided or search functions not available');
            return false;
        });
        
        // Product detail actions
        registerActionHandler('show_product_details', function(params) {
            console.log('🎯 EXECUTING: show_product_details command');
            alert('🎯 VOICE COMMAND EXECUTED: show_product_details');
            
            const productId = getCurrentProductId();
            console.log('🛍️ Current product ID:', productId);
            
            if (productId) {
                if (typeof window.quickView === 'function') {
                    console.log('✅ quickView function available');
                    console.log('🚀 Calling quickView with productId:', productId);
                    window.quickView(productId);
                    showFeedback('Showing product details');
                    alert(`✅ SUCCESS: quickView(${productId}) function called`);
                    return true;
                } else if (typeof window.viewProduct === 'function') {
                    console.log('✅ viewProduct function available');
                    console.log('🚀 Calling viewProduct with productId:', productId);
                    window.viewProduct(productId);
                    showFeedback('Viewing product');
                    alert(`✅ SUCCESS: viewProduct(${productId}) function called`);
                    return true;
                }
            } else {
                console.log('❌ No product selected');
                showFeedback('No product selected', 'error');
                alert('❌ FAILED: No product selected');
            }
            return false;
        });
        
        // Help action
        registerActionHandler('show_voice_help', function(params) {
            console.log('🎯 EXECUTING: show_voice_help command');
            alert('🎯 VOICE COMMAND EXECUTED: show_voice_help');
            
            const helpMessage = `Voice Commands Available:
• "Go home" - Return to main page
• "Search for [item]" - Search products  
• "Open cart" - View shopping cart
• "Add to cart" - Add current product
• "Show products" - View catalog
• "Help" - Show this message`;
            
            console.log('📖 Showing help message');
            showFeedback(helpMessage);
            alert('✅ SUCCESS: Help message displayed');
            return true;
        });
        
        // Voice control actions
        registerActionHandler('stop_voice_recognition', function(params) {
            console.log('🎯 EXECUTING: stop_voice_recognition command');
            alert('🎯 VOICE COMMAND EXECUTED: stop_voice_recognition');
            
            if (window.manvueVoice && window.manvueVoice.stopListening) {
                console.log('✅ manvueVoice.stopListening available');
                console.log('🚀 Calling stopListening()');
                window.manvueVoice.stopListening();
                showFeedback('Voice recognition stopped');
                alert('✅ SUCCESS: Voice recognition stopped');
                return true;
            }
            
            console.log('❌ Stop voice recognition failed - function not available');
            alert('❌ FAILED: Voice recognition stop function not available');
            return false;
        });
        
        registerActionHandler('start_voice_recognition', function(params) {
            console.log('🎯 EXECUTING: start_voice_recognition command');
            alert('🎯 VOICE COMMAND EXECUTED: start_voice_recognition');
            
            if (window.manvueVoice && window.manvueVoice.startListening) {
                console.log('✅ manvueVoice.startListening available');
                console.log('🚀 Calling startListening()');
                window.manvueVoice.startListening();
                showFeedback('Voice recognition started');
                alert('✅ SUCCESS: Voice recognition started');
                return true;
            }
            
            console.log('❌ Start voice recognition failed - function not available');
            alert('❌ FAILED: Voice recognition start function not available');
            return false;
        });
        
        console.log(`✅ Registered ${actionHandlers.size} action handlers`);
        console.log(`🏁 FUNCTION COMPLETED: setupManVueHandlers`);
    }
    
    // Get current product ID from various sources
    function getCurrentProductId() {
        console.log(`🔧 FUNCTION CALLED: getCurrentProductId()`);
        
        // Check for product page
        const productElement = document.querySelector('[data-product-id]');
        console.log(`🔍 Product element found: ${productElement ? 'YES' : 'NO'}`);
        if (productElement) {
            const productId = parseInt(productElement.getAttribute('data-product-id'));
            console.log(`📦 Product ID from element: ${productId}`);
            console.log(`🏁 FUNCTION COMPLETED: getCurrentProductId`);
            return productId;
        }
        
        // Check quick view modal
        const modal = document.getElementById('quick-view-modal');
        console.log(`🔍 Quick view modal found: ${modal ? 'YES' : 'NO'}`);
        if (modal && modal.style.display !== 'none') {
            const modalProductId = modal.getAttribute('data-product-id');
            if (modalProductId) {
                const productId = parseInt(modalProductId);
                console.log(`📦 Product ID from modal: ${productId}`);
                console.log(`🏁 FUNCTION COMPLETED: getCurrentProductId`);
                return productId;
            }
        }
        
        // Check highlighted/selected product
        const highlighted = document.querySelector('.product-card.selected, .product-card:hover, .product-card.highlighted');
        console.log(`🔍 Highlighted product found: ${highlighted ? 'YES' : 'NO'}`);
        if (highlighted) {
            const id = highlighted.getAttribute('data-product-id');
            if (id) {
                const productId = parseInt(id);
                console.log(`📦 Product ID from highlighted: ${productId}`);
                console.log(`🏁 FUNCTION COMPLETED: getCurrentProductId`);
                return productId;
            }
        }
        
        // Default to first visible product as fallback
        const firstProduct = document.querySelector('.product-card:not(.hidden)');
        console.log(`🔍 First visible product found: ${firstProduct ? 'YES' : 'NO'}`);
        if (firstProduct) {
            const id = firstProduct.getAttribute('data-product-id');
            if (id) {
                const productId = parseInt(id);
                console.log(`📦 Product ID from first visible: ${productId}`);
                console.log(`🏁 FUNCTION COMPLETED: getCurrentProductId`);
                return productId;
            }
        }
        
        console.log(`📦 Using fallback product ID: 1`);
        console.log(`🏁 FUNCTION COMPLETED: getCurrentProductId`);
        return 1; // Fallback product ID
    }
    
    // Show feedback to user
    function showFeedback(message, type = 'success') {
        console.log(`🔧 FUNCTION CALLED: showFeedback(${message}, ${type})`);
        console.log(`📢 Feedback: ${message}`);
        
        // Try to use existing ManVue message system
        if (typeof window.showMessage === 'function') {
            console.log(`✅ Using ManVue showMessage function`);
            window.showMessage(message);
        } else {
            console.log(`⚠️ ManVue showMessage not available, using simple feedback`);
            // Create a simple feedback display
            showSimpleFeedback(message, type);
        }
        console.log(`🏁 FUNCTION COMPLETED: showFeedback`);
    }
    
    // Simple feedback display
    function showSimpleFeedback(message, type) {
        console.log(`🔧 FUNCTION CALLED: showSimpleFeedback(${message}, ${type})`);
        
        // Remove existing feedback
        const existing = document.getElementById('voice-feedback');
        console.log(`🔍 Existing feedback element: ${existing ? 'FOUND' : 'NOT FOUND'}`);
        if (existing) {
            console.log(`🗑️ Removing existing feedback`);
            existing.remove();
        }
        
        // Create feedback element
        console.log(`🆕 Creating new feedback element`);
        const feedback = document.createElement('div');
        feedback.id = 'voice-feedback';
        feedback.textContent = message;
        feedback.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'error' ? '#f44336' : '#4caf50'};
            color: white;
            padding: 12px 20px;
            border-radius: 4px;
            z-index: 10000;
            font-family: system-ui, sans-serif;
            font-size: 14px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            max-width: 300px;
            word-wrap: break-word;
        `;
        
        console.log(`📝 Adding feedback to DOM`);
        document.body.appendChild(feedback);
        
        // Auto-remove after 3 seconds
        console.log(`⏰ Setting auto-remove timer (3 seconds)`);
        setTimeout(() => {
            if (feedback.parentNode) {
                console.log(`🗑️ Auto-removing feedback element`);
                feedback.remove();
            }
        }, 3000);
        
        console.log(`🏁 FUNCTION COMPLETED: showSimpleFeedback`);
    }
    
    // Setup voice interface integration
    function setupVoiceIntegration() {
        console.log(`🔧 FUNCTION CALLED: setupVoiceIntegration()`);
        console.log('🎤 Setting up voice integration...');
        
        // Wait for VoiceInterface to be available
        const checkVoiceInterface = () => {
            if (typeof window.VoiceInterface !== 'undefined') {
                console.log('✅ VoiceInterface found, initializing...');
                
                // Create voice interface instance
                window.manvueVoice = new VoiceInterface({
                    continuous: true,
                    interimResults: true,
                    onResult: handleVoiceResult,
                    onError: handleVoiceError,
                    onStart: () => showFeedback('Listening...', 'info'),
                    onEnd: () => showFeedback('Voice stopped', 'info')
                });
                
                // Override executeCommand to use our action handlers
                if (window.manvueVoice.executeCommand) {
                    const originalExecute = window.manvueVoice.executeCommand.bind(window.manvueVoice);
                    
                    window.manvueVoice.executeCommand = function(commandResult) {
                        if (commandResult && commandResult.action) {
                            console.log('🎯 Voice command received:', commandResult);
                            
                            const success = executeAction(commandResult.action, commandResult.parameters);
                            
                            if (!success) {
                                // Try original implementation as fallback
                                console.log('🔄 Trying original implementation...');
                                originalExecute(commandResult);
                            }
                        }
                    };
                }
                
                console.log('✅ Voice integration setup complete');
                showFeedback('Voice commands ready!');
                
                // Make it globally available
                window.voiceActionHandlers = {
                    register: registerActionHandler,
                    execute: executeAction,
                    handlers: actionHandlers
                };
                
                console.log(`🏁 FUNCTION COMPLETED: setupVoiceIntegration`);
                
            } else {
                console.log('⏳ Waiting for VoiceInterface...');
                setTimeout(checkVoiceInterface, 500);
            }
        };
        
        checkVoiceInterface();
    }
    
    // Handle voice results
    function handleVoiceResult(transcript, confidence, commandResult) {
        console.log(`🔧 FUNCTION CALLED: handleVoiceResult(${transcript}, ${confidence})`);
        console.log(`🎤 Voice: "${transcript}" (${Math.round(confidence * 100)}%)`, commandResult);
        
        // Show recognized text on the page
        showVoiceTextOnPage(transcript, confidence, commandResult);
        
        if (commandResult) {
            console.log(`✅ Command result found: ${commandResult.action}`);
            showFeedback(`Recognized: "${transcript}"`);
        } else {
            console.log(`❌ No command result found`);
            showFeedback(`"${transcript}" - command not recognized`, 'error');
        }
        
        console.log(`🏁 FUNCTION COMPLETED: handleVoiceResult`);
    }
    
    // Show voice recognized text on the page
    function showVoiceTextOnPage(transcript, confidence, commandResult) {
        console.log(`🔧 FUNCTION CALLED: showVoiceTextOnPage(${transcript}, ${confidence})`);
        
        const display = document.getElementById('voice-recognition-display');
        const textElement = document.getElementById('voice-recognized-text');
        const confidenceElement = document.getElementById('voice-confidence');
        
        console.log(`🔍 Display elements found:`, {
            display: display ? 'YES' : 'NO',
            textElement: textElement ? 'YES' : 'NO',
            confidenceElement: confidenceElement ? 'YES' : 'NO'
        });
        
        if (display && textElement && confidenceElement) {
            console.log(`📱 Showing voice text display`);
            
            // Show the display
            display.style.display = 'block';
            console.log(`👁️ Display set to visible`);
            
            // Update text
            textElement.textContent = transcript;
            console.log(`📝 Text updated: "${transcript}"`);
            
            // Update confidence
            confidenceElement.textContent = `${Math.round(confidence * 100)}%`;
            console.log(`📊 Confidence updated: ${Math.round(confidence * 100)}%`);
            
            // Auto-hide after 3 seconds
            console.log(`⏰ Setting auto-hide timer (3 seconds)`);
            setTimeout(() => {
                display.style.display = 'none';
                console.log(`👁️ Display hidden after timeout`);
            }, 3000);
            
            console.log(`📱 Voice text displayed on page: "${transcript}"`);
        } else {
            console.log(`❌ Voice display elements not found`);
        }
        
        console.log(`🏁 FUNCTION COMPLETED: showVoiceTextOnPage`);
    }
    
    // Handle voice errors
    function handleVoiceError(error, message) {
        console.log(`🔧 FUNCTION CALLED: handleVoiceError(${error}, ${message})`);
        console.error('🔴 Voice error:', error, message);
        showFeedback(`Voice error: ${message}`, 'error');
        console.log(`🏁 FUNCTION COMPLETED: handleVoiceError`);
    }
    
    // Initialize when DOM is ready
    function initialize() {
        console.log(`🔧 FUNCTION CALLED: initialize()`);
        console.log('🚀 Initializing Simple Voice Fix...');
        
        // Setup ManVue handlers first
        console.log(`🔧 Calling setupManVueHandlers()`);
        setupManVueHandlers();
        
        // Then setup voice integration
        console.log(`🔧 Calling setupVoiceIntegration()`);
        setupVoiceIntegration();
        
        console.log('✅ Simple Voice Fix loaded successfully');
        console.log(`🏁 FUNCTION COMPLETED: initialize`);
    }
    
    // Start initialization
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initialize);
    } else {
        // DOM already loaded
        setTimeout(initialize, 100);
    }
    
    // Export for debugging
    window.SimpleVoiceFix = {
        registerActionHandler,
        executeAction,
        actionHandlers,
        getCurrentProductId,
        showFeedback
    };
    
})();
