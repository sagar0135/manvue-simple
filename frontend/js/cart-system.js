/**
 * ManVue Enhanced Cart System
 * Handles cart functionality, user authentication, and checkout process
 */

class ManVueCartSystem {
    constructor() {
        this.cart = this.loadCart();
        this.user = this.loadUser();
        this.isAuthenticated = this.checkAuthentication();
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.updateCartDisplay();
        this.updateUserDisplay();
    }

    setupEventListeners() {
        // Cart toggle
        document.addEventListener('click', (e) => {
            if (e.target.closest('.cart-icon')) {
                this.toggleCart();
            }
            if (e.target.closest('.wishlist-icon')) {
                this.toggleWishlist();
            }
        });

        // Close cart when clicking outside
        document.addEventListener('click', (e) => {
            const cartSidebar = document.getElementById('cart-sidebar');
            const wishlistSidebar = document.getElementById('wishlist-sidebar');
            
            if (cartSidebar && !cartSidebar.contains(e.target) && !e.target.closest('.cart-icon')) {
                cartSidebar.classList.remove('open');
            }
            if (wishlistSidebar && !wishlistSidebar.contains(e.target) && !e.target.closest('.wishlist-icon')) {
                wishlistSidebar.classList.remove('open');
            }
        });
    }

    // Cart Management
    addToCart(product) {
        const existingItem = this.cart.find(item => 
            item.id === product.id && 
            item.size === product.size && 
            item.color === product.color
        );

        if (existingItem) {
            existingItem.quantity += product.quantity;
        } else {
            this.cart.push({
                ...product,
                addedAt: new Date().toISOString()
            });
        }

        this.saveCart();
        this.updateCartDisplay();
        this.showNotification('Added to cart!', 'success');
    }

    removeFromCart(itemId, size, color) {
        this.cart = this.cart.filter(item => 
            !(item.id === itemId && item.size === size && item.color === color)
        );
        
        this.saveCart();
        this.updateCartDisplay();
        this.showNotification('Removed from cart', 'info');
    }

    updateQuantity(itemId, size, color, newQuantity) {
        const item = this.cart.find(item => 
            item.id === itemId && item.size === size && item.color === color
        );
        
        if (item) {
            if (newQuantity <= 0) {
                this.removeFromCart(itemId, size, color);
            } else {
                item.quantity = newQuantity;
                this.saveCart();
                this.updateCartDisplay();
            }
        }
    }

    clearCart() {
        this.cart = [];
        this.saveCart();
        this.updateCartDisplay();
        this.showNotification('Cart cleared', 'info');
    }

    // Wishlist Management
    addToWishlist(product) {
        let wishlist = this.loadWishlist();
        
        const existingItem = wishlist.find(item => item.id === product.id);
        if (!existingItem) {
            wishlist.push({
                id: product.id,
                name: product.name,
                price: product.price,
                image: product.image,
                addedAt: new Date().toISOString()
            });
            
            this.saveWishlist(wishlist);
            this.updateWishlistDisplay();
            this.showNotification('Added to wishlist!', 'success');
        } else {
            this.showNotification('Already in wishlist', 'info');
        }
    }

    removeFromWishlist(productId) {
        let wishlist = this.loadWishlist();
        wishlist = wishlist.filter(item => item.id !== productId);
        
        this.saveWishlist(wishlist);
        this.updateWishlistDisplay();
        this.showNotification('Removed from wishlist', 'info');
    }

    // Display Updates
    updateCartDisplay() {
        const cartCount = this.cart.reduce((sum, item) => sum + item.quantity, 0);
        const cartTotal = this.cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
        
        // Update cart icon
        const cartIcon = document.querySelector('.cart-icon');
        if (cartIcon) {
            const countSpan = cartIcon.querySelector('#cart-count');
            if (countSpan) {
                countSpan.textContent = cartCount;
            }
        }

        // Update cart sidebar
        const cartSidebar = document.getElementById('cart-sidebar');
        if (cartSidebar) {
            const cartItems = cartSidebar.querySelector('#cart-items');
            const cartTotalElement = cartSidebar.querySelector('#cart-total');
            
            if (cartItems) {
                cartItems.innerHTML = this.renderCartItems();
            }
            if (cartTotalElement) {
                cartTotalElement.textContent = cartTotal.toFixed(2);
            }
        }
    }

    updateWishlistDisplay() {
        const wishlist = this.loadWishlist();
        const wishlistCount = wishlist.length;
        
        // Update wishlist icon
        const wishlistIcon = document.querySelector('.wishlist-icon');
        if (wishlistIcon) {
            if (wishlistCount > 0) {
                wishlistIcon.innerHTML = `♡ <span>${wishlistCount}</span>`;
            } else {
                wishlistIcon.innerHTML = '♡';
            }
        }

        // Update wishlist sidebar
        const wishlistSidebar = document.getElementById('wishlist-sidebar');
        if (wishlistSidebar) {
            const wishlistItems = wishlistSidebar.querySelector('#wishlist-items');
            if (wishlistItems) {
                wishlistItems.innerHTML = this.renderWishlistItems();
            }
        }
    }

    renderCartItems() {
        if (this.cart.length === 0) {
            return '<p>Your cart is empty</p>';
        }

        return this.cart.map(item => `
            <div class="cart-item">
                <img src="${item.image}" alt="${item.name}" class="cart-item-image">
                <div class="cart-item-info">
                    <h4>${item.name}</h4>
                    <p>Size: ${item.size} | Color: ${item.color}</p>
                    <div class="cart-item-controls">
                        <button onclick="cartSystem.updateQuantity('${item.id}', '${item.size}', '${item.color}', ${item.quantity - 1})">-</button>
                        <span>${item.quantity}</span>
                        <button onclick="cartSystem.updateQuantity('${item.id}', '${item.size}', '${item.color}', ${item.quantity + 1})">+</button>
                    </div>
                    <div class="cart-item-price">£${(item.price * item.quantity).toFixed(2)}</div>
                    <button onclick="cartSystem.removeFromCart('${item.id}', '${item.size}', '${item.color}')" class="remove-btn">Remove</button>
                </div>
            </div>
        `).join('');
    }

    renderWishlistItems() {
        const wishlist = this.loadWishlist();
        
        if (wishlist.length === 0) {
            return '<p>Your wishlist is empty</p>';
        }

        return wishlist.map(item => `
            <div class="wishlist-item">
                <img src="${item.image}" alt="${item.name}" class="wishlist-item-image">
                <div class="wishlist-item-info">
                    <h4>${item.name}</h4>
                    <p>£${item.price.toFixed(2)}</p>
                    <button onclick="cartSystem.addToCart({id: '${item.id}', name: '${item.name}', price: ${item.price}, image: '${item.image}', size: 'M', color: 'Black', quantity: 1})" class="add-to-cart-btn">Add to Cart</button>
                    <button onclick="cartSystem.removeFromWishlist('${item.id}')" class="remove-btn">Remove</button>
                </div>
            </div>
        `).join('');
    }

    // UI Controls
    toggleCart() {
        const cartSidebar = document.getElementById('cart-sidebar');
        if (cartSidebar) {
            cartSidebar.classList.toggle('open');
        }
    }

    toggleWishlist() {
        const wishlistSidebar = document.getElementById('wishlist-sidebar');
        if (wishlistSidebar) {
            wishlistSidebar.classList.toggle('open');
        }
    }

    // Checkout Process
    async proceedToCheckout() {
        if (this.cart.length === 0) {
            this.showNotification('Your cart is empty', 'error');
            return;
        }

        if (!this.isAuthenticated) {
            this.showLoginModal();
            return;
        }

        // Proceed to payment
        this.showPaymentModal();
    }

    showLoginModal() {
        const modal = document.createElement('div');
        modal.className = 'modal';
        modal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h3>Sign In Required</h3>
                    <button onclick="this.closest('.modal').remove()">✕</button>
                </div>
                <div class="modal-body">
                    <p>Please sign in to proceed with checkout</p>
                    <div class="auth-options">
                        <button class="btn-primary" onclick="cartSystem.showLoginForm()">Sign In</button>
                        <button class="btn-secondary" onclick="cartSystem.showRegisterForm()">Create Account</button>
                    </div>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
    }

    showLoginForm() {
        const modal = document.createElement('div');
        modal.className = 'modal';
        modal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h3>Sign In</h3>
                    <button onclick="this.closest('.modal').remove()">✕</button>
                </div>
                <form id="login-form" onsubmit="cartSystem.handleLogin(event)">
                    <div class="form-group">
                        <label for="login-email">Email</label>
                        <input type="email" id="login-email" required>
                    </div>
                    <div class="form-group">
                        <label for="login-password">Password</label>
                        <input type="password" id="login-password" required>
                    </div>
                    <button type="submit" class="btn-primary full-width">Sign In</button>
                    <p>Don't have an account? <a href="#" onclick="cartSystem.showRegisterForm()">Sign up</a></p>
                </form>
            </div>
        `;
        document.body.appendChild(modal);
    }

    showRegisterForm() {
        const modal = document.createElement('div');
        modal.className = 'modal';
        modal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h3>Create Account</h3>
                    <button onclick="this.closest('.modal').remove()">✕</button>
                </div>
                <form id="register-form" onsubmit="cartSystem.handleRegister(event)">
                    <div class="form-group">
                        <label for="register-name">Full Name</label>
                        <input type="text" id="register-name" required>
                    </div>
                    <div class="form-group">
                        <label for="register-email">Email</label>
                        <input type="email" id="register-email" required>
                    </div>
                    <div class="form-group">
                        <label for="register-password">Password</label>
                        <input type="password" id="register-password" required minlength="6">
                    </div>
                    <div class="form-group">
                        <label for="register-phone">Phone (Optional)</label>
                        <input type="tel" id="register-phone">
                    </div>
                    <button type="submit" class="btn-primary full-width">Create Account</button>
                    <p>Already have an account? <a href="#" onclick="cartSystem.showLoginForm()">Sign in</a></p>
                </form>
            </div>
        `;
        document.body.appendChild(modal);
    }

    async handleLogin(event) {
        event.preventDefault();
        
        const email = document.getElementById('login-email').value;
        const password = document.getElementById('login-password').value;

        try {
            const response = await fetch('/api/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, password })
            });

            if (response.ok) {
                const userData = await response.json();
                this.user = userData;
                this.isAuthenticated = true;
                this.saveUser(userData);
                this.updateUserDisplay();
                
                // Close modal and proceed to checkout
                document.querySelector('.modal').remove();
                this.showPaymentModal();
                
                this.showNotification('Welcome back!', 'success');
            } else {
                this.showNotification('Invalid credentials', 'error');
            }
        } catch (error) {
            console.error('Login error:', error);
            this.showNotification('Login failed. Please try again.', 'error');
        }
    }

    async handleRegister(event) {
        event.preventDefault();
        
        const name = document.getElementById('register-name').value;
        const email = document.getElementById('register-email').value;
        const password = document.getElementById('register-password').value;
        const phone = document.getElementById('register-phone').value;

        try {
            const response = await fetch('/api/auth/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ name, email, password, phone })
            });

            if (response.ok) {
                const userData = await response.json();
                this.user = userData;
                this.isAuthenticated = true;
                this.saveUser(userData);
                this.updateUserDisplay();
                
                // Close modal and proceed to checkout
                document.querySelector('.modal').remove();
                this.showPaymentModal();
                
                this.showNotification('Account created successfully!', 'success');
            } else {
                this.showNotification('Registration failed. Please try again.', 'error');
            }
        } catch (error) {
            console.error('Registration error:', error);
            this.showNotification('Registration failed. Please try again.', 'error');
        }
    }

    showPaymentModal() {
        const modal = document.createElement('div');
        modal.className = 'modal';
        modal.innerHTML = `
            <div class="modal-content large">
                <div class="modal-header">
                    <h3>Checkout</h3>
                    <button onclick="this.closest('.modal').remove()">✕</button>
                </div>
                <div class="checkout-content">
                    <div class="checkout-summary">
                        <h4>Order Summary</h4>
                        <div id="checkout-items">
                            ${this.renderCheckoutItems()}
                        </div>
                        <div class="checkout-total">
                            <strong>Total: £${this.getCartTotal().toFixed(2)}</strong>
                        </div>
                    </div>
                    <div class="payment-form">
                        <h4>Payment Information</h4>
                        <form id="payment-form" onsubmit="cartSystem.processPayment(event)">
                            <div class="form-group">
                                <label for="card-number">Card Number</label>
                                <input type="text" id="card-number" placeholder="1234 5678 9012 3456" required>
                            </div>
                            <div class="form-row">
                                <div class="form-group">
                                    <label for="expiry">Expiry Date</label>
                                    <input type="text" id="expiry" placeholder="MM/YY" required>
                                </div>
                                <div class="form-group">
                                    <label for="cvv">CVV</label>
                                    <input type="text" id="cvv" placeholder="123" required>
                                </div>
                            </div>
                            <div class="form-group">
                                <label for="cardholder-name">Cardholder Name</label>
                                <input type="text" id="cardholder-name" required>
                            </div>
                            <button type="submit" class="btn-primary full-width">Complete Payment</button>
                        </form>
                    </div>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
    }

    renderCheckoutItems() {
        return this.cart.map(item => `
            <div class="checkout-item">
                <img src="${item.image}" alt="${item.name}" class="checkout-item-image">
                <div class="checkout-item-info">
                    <h5>${item.name}</h5>
                    <p>Size: ${item.size} | Color: ${item.color} | Qty: ${item.quantity}</p>
                    <span>£${(item.price * item.quantity).toFixed(2)}</span>
                </div>
            </div>
        `).join('');
    }

    async processPayment(event) {
        event.preventDefault();
        
        const paymentData = {
            cardNumber: document.getElementById('card-number').value,
            expiry: document.getElementById('expiry').value,
            cvv: document.getElementById('cvv').value,
            cardholderName: document.getElementById('cardholder-name').value,
            amount: this.getCartTotal(),
            items: this.cart
        };

        try {
            // Show loading state
            const submitBtn = event.target.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            submitBtn.textContent = 'Processing...';
            submitBtn.disabled = true;

            const response = await fetch('/api/payment/process', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(paymentData)
            });

            if (response.ok) {
                const result = await response.json();
                
                // Clear cart
                this.clearCart();
                
                // Show success message
                this.showNotification('Payment successful! Order confirmed.', 'success');
                
                // Close modal
                document.querySelector('.modal').remove();
                
                // Redirect to order confirmation
                window.location.href = `/order-confirmation?orderId=${result.orderId}`;
            } else {
                this.showNotification('Payment failed. Please try again.', 'error');
            }
        } catch (error) {
            console.error('Payment error:', error);
            this.showNotification('Payment failed. Please try again.', 'error');
        } finally {
            // Reset button
            const submitBtn = event.target.querySelector('button[type="submit"]');
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        }
    }

    // Utility Methods
    getCartTotal() {
        return this.cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    }

    loadCart() {
        return JSON.parse(localStorage.getItem('manvue_cart') || '[]');
    }

    saveCart() {
        localStorage.setItem('manvue_cart', JSON.stringify(this.cart));
    }

    loadWishlist() {
        return JSON.parse(localStorage.getItem('manvue_wishlist') || '[]');
    }

    saveWishlist(wishlist) {
        localStorage.setItem('manvue_wishlist', JSON.stringify(wishlist));
    }

    loadUser() {
        return JSON.parse(localStorage.getItem('manvue_user') || 'null');
    }

    saveUser(user) {
        localStorage.setItem('manvue_user', JSON.stringify(user));
    }

    checkAuthentication() {
        return this.user !== null && this.user.id;
    }

    updateUserDisplay() {
        // Update user menu or login button
        const loginButton = document.querySelector('[onclick="toggleUserMenu()"]');
        if (loginButton) {
            if (this.isAuthenticated) {
                loginButton.textContent = this.user.name || 'Account';
            } else {
                loginButton.textContent = 'Login';
            }
        }
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'success' ? '#28a745' : type === 'error' ? '#dc3545' : '#007bff'};
            color: white;
            padding: 15px 20px;
            border-radius: 8px;
            z-index: 10000;
            font-weight: 500;
            max-width: 300px;
        `;
        notification.textContent = message;
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
}

// Initialize cart system
const cartSystem = new ManVueCartSystem();

// Global functions for backward compatibility
function addToCart(product) {
    cartSystem.addToCart(product);
}

function addToWishlist(product) {
    cartSystem.addToWishlist(product);
}

function toggleCart() {
    cartSystem.toggleCart();
}

function toggleWishlist() {
    cartSystem.toggleWishlist();
}

function proceedToCheckout() {
    cartSystem.proceedToCheckout();
}
