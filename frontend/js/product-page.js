// Product Page JavaScript
const API_BASE_URL = "http://localhost:5001"; // Updated to use enhanced backend

// Global variables
let currentProduct = null;
let selectedSize = null;
let selectedColor = null;
let quantity = 1;
let cart = JSON.parse(localStorage.getItem('cart')) || [];

// Authentication variables
let currentUser = null;

// Authentication Functions
function initializeAuth() {
    // Check if user is logged in (from localStorage)
    const savedUser = localStorage.getItem('manvue_user');
    if (savedUser) {
        currentUser = JSON.parse(savedUser);
        updateAuthUI();
        showProductContent();
    } else {
        showAuthRequiredOverlay();
    }
}

function updateAuthUI() {
    const userMenuContent = document.getElementById('user-menu-content');
    const userIconText = document.getElementById('user-icon-text');
    const cartCount = document.getElementById('cart-count');
    
    if (currentUser) {
        // User is logged in
        userIconText.textContent = currentUser.name ? currentUser.name.charAt(0).toUpperCase() : '👤';
        
        userMenuContent.innerHTML = `
            <div class="user-info">
                <div class="user-avatar">${currentUser.name ? currentUser.name.charAt(0).toUpperCase() : '👤'}</div>
                <div class="user-details">
                    <div class="user-name">${currentUser.name || 'User'}</div>
                    <div class="user-email">${currentUser.email}</div>
                </div>
            </div>
            <div class="user-menu-links">
                <a href="#" onclick="showProfile()">Profile Settings</a>
                <a href="#" onclick="showOrders()">My Orders</a>
                <a href="#" onclick="toggleWishlist()">Wishlist</a>
                <a href="#" onclick="logout()" class="logout-link">Sign Out</a>
            </div>
        `;
        
        // Update cart count
        updateCartCount();
    } else {
        // User is not logged in
        userIconText.textContent = '👤';
        userMenuContent.innerHTML = `
            <div class="guest-menu">
                <p>Sign in for a personalized experience</p>
                <button onclick="showLogin()" class="btn btn-primary">Sign In</button>
                <button onclick="showRegister()" class="btn btn-outline">Create Account</button>
            </div>
        `;
        
        if (cartCount) cartCount.textContent = '0';
    }
}

function showAuthRequiredOverlay() {
    const overlay = document.getElementById('auth-required-overlay');
    const productMain = document.querySelector('.product-main');
    
    if (overlay && productMain) {
        overlay.style.display = 'flex';
        productMain.style.filter = 'blur(5px)';
        productMain.style.pointerEvents = 'none';
        
        // Add authentication required styling to all interactive elements
        addAuthRequiredStyling();
    }
}

function addAuthRequiredStyling() {
    // Disable all interactive elements visually
    const interactiveElements = [
        '.size-option',
        '.color-option', 
        '.quantity-controls button',
        '.add-to-cart button',
        '.btn',
        '.thumbnail'
    ];
    
    interactiveElements.forEach(selector => {
        const elements = document.querySelectorAll(selector);
        elements.forEach(element => {
            element.style.opacity = '0.5';
            element.style.cursor = 'not-allowed';
            element.style.pointerEvents = 'none';
        });
    });
    
    // Add overlay message to product info
    const productInfo = document.querySelector('.product-info');
    if (productInfo && !document.querySelector('.auth-warning')) {
        const authWarning = document.createElement('div');
        authWarning.className = 'auth-warning';
        authWarning.innerHTML = `
            <div style="background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 8px; padding: 1rem; margin: 1rem 0; text-align: center;">
                <strong>🔒 Account Required</strong><br>
                <small>Please sign in to interact with this product</small>
            </div>
        `;
        productInfo.insertBefore(authWarning, productInfo.firstChild);
    }
}

function hideAuthRequiredOverlay() {
    const overlay = document.getElementById('auth-required-overlay');
    const productMain = document.querySelector('.product-main');
    
    if (overlay && productMain) {
        overlay.style.display = 'none';
        productMain.style.filter = 'none';
        productMain.style.pointerEvents = 'auto';
        
        // Remove authentication required styling
        removeAuthRequiredStyling();
    }
}

function removeAuthRequiredStyling() {
    // Re-enable all interactive elements
    const interactiveElements = [
        '.size-option',
        '.color-option', 
        '.quantity-controls button',
        '.add-to-cart button',
        '.btn',
        '.thumbnail'
    ];
    
    interactiveElements.forEach(selector => {
        const elements = document.querySelectorAll(selector);
        elements.forEach(element => {
            element.style.opacity = '';
            element.style.cursor = '';
            element.style.pointerEvents = '';
        });
    });
    
    // Remove auth warning message
    const authWarning = document.querySelector('.auth-warning');
    if (authWarning) {
        authWarning.remove();
    }
}

function showProductContent() {
    hideAuthRequiredOverlay();
}

// Modal Functions
function showModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'block';
        document.body.style.overflow = 'hidden';
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
}

function showLogin() {
    showModal('login-modal');
}

function showRegister() {
    showModal('register-modal');
}

function switchToRegister() {
    closeModal('login-modal');
    showModal('register-modal');
}

function switchToLogin() {
    closeModal('register-modal');
    closeModal('forgot-password-modal');
    showModal('login-modal');
}

function showForgotPassword() {
    closeModal('login-modal');
    showModal('forgot-password-modal');
}

function handleLogin(event) {
    event.preventDefault();
    
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    
    // Simulate login validation
    if (email && password) {
        // Check if user exists in localStorage
        const existingUsers = JSON.parse(localStorage.getItem('manvue_users') || '[]');
        const user = existingUsers.find(u => u.email === email && u.password === password);
        
        if (user) {
            // Login successful
            currentUser = user;
            localStorage.setItem('manvue_user', JSON.stringify(currentUser));
            
            closeModal('login-modal');
            updateAuthUI();
            showProductContent();
            showMessage('Welcome back! Successfully signed in.');
            
            // Clear form
            document.getElementById('login-form').reset();
        } else {
            showMessage('Invalid email or password. Please try again.');
        }
    } else {
        showMessage('Please fill in all fields.');
    }
}

function handleRegister(event) {
    event.preventDefault();
    
    const name = document.getElementById('register-name').value.trim();
    const email = document.getElementById('register-email').value.trim();
    const phone = document.getElementById('register-phone').value.trim();
    const password = document.getElementById('register-password').value;
    const confirmPassword = document.getElementById('register-confirm-password').value;
    const termsAccepted = document.getElementById('terms-agreement').checked;
    const marketingConsent = document.getElementById('marketing-consent').checked;
    
    // Comprehensive validation
    if (!name || name.length < 2) {
        showMessage('Please enter your full name (minimum 2 characters).', 'error');
        return;
    }
    
    if (!email || !isValidEmail(email)) {
        showMessage('Please enter a valid email address.', 'error');
        return;
    }
    
    if (!phone || !isValidPhone(phone)) {
        showMessage('Please enter a valid phone number (minimum 10 digits).', 'error');
        return;
    }
    
    if (!password || password.length < 6) {
        showMessage('Password must be at least 6 characters long.', 'error');
        return;
    }
    
    if (password !== confirmPassword) {
        showMessage('Passwords do not match.', 'error');
        return;
    }
    
    if (!termsAccepted) {
        showMessage('You must agree to the Terms & Conditions and Privacy Policy.', 'error');
        return;
    }
    
    // Check if user already exists (email or phone)
    const existingUsers = JSON.parse(localStorage.getItem('manvue_users') || '[]');
    
    if (existingUsers.some(u => u.email === email)) {
        showMessage('An account with this email already exists. Please sign in or use a different email.', 'error');
        return;
    }
    
    if (existingUsers.some(u => u.phone === phone)) {
        showMessage('An account with this phone number already exists. Please use a different number.', 'error');
        return;
    }
    
    // Create new user with all required fields
    const newUser = {
        id: Date.now().toString(),
        name: name,
        email: email,
        phone: phone,
        password: password, // In production, this should be hashed
        marketingConsent: marketingConsent,
        createdAt: new Date().toISOString(),
        isVerified: false, // Email/phone verification status
        lastLogin: new Date().toISOString()
    };
    
    existingUsers.push(newUser);
    localStorage.setItem('manvue_users', JSON.stringify(existingUsers));
    
    // Auto-login after successful registration
    currentUser = newUser;
    localStorage.setItem('manvue_user', JSON.stringify(currentUser));
    
    closeModal('register-modal');
    updateAuthUI();
    showProductContent();
    showMessage('🎉 Account created successfully! Welcome to MANVUE.', 'success');
    
    // Clear form
    document.getElementById('register-form').reset();
    
    // Log registration event
    logUserEvent('user_registered', {
        user_id: newUser.id,
        registration_date: newUser.createdAt
    });
}

function handleForgotPassword(event) {
    event.preventDefault();
    
    const email = document.getElementById('forgot-email').value;
    
    // Simulate password reset
    showMessage('If an account with this email exists, we\'ve sent a password reset link.');
    closeModal('forgot-password-modal');
    document.getElementById('forgot-password-form').reset();
}

function logout() {
    currentUser = null;
    localStorage.removeItem('manvue_user');
    
    // Clear cart and wishlist for security
    cart = [];
    localStorage.removeItem('cart');
    localStorage.removeItem('wishlist');
    
    updateAuthUI();
    showAuthRequiredOverlay();
    toggleUserMenu();
    showMessage('Successfully signed out. See you again soon!');
}

// User Menu Functions
function toggleUserMenu() {
    const userMenu = document.getElementById('user-menu');
    if (userMenu) {
        userMenu.classList.toggle('active');
    }
}

function showProfile() {
    showMessage('Profile settings feature coming soon!');
    toggleUserMenu();
}

function showOrders() {
    showMessage('Order history feature coming soon!');
    toggleUserMenu();
}

// Initialize page when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize authentication first
    initializeAuth();
    
    const urlParams = new URLSearchParams(window.location.search);
    const productId = urlParams.get('id');
    
    if (productId) {
        loadProduct(productId);
    } else {
        // Fallback to demo product
        loadDemoProduct();
    }
});

// Load product from API
async function loadProduct(productId) {
    try {
        showLoading();
        
        const response = await fetch(`${API_BASE_URL}/products/${productId}`);
        if (!response.ok) {
            throw new Error('Product not found');
        }
        
        const product = await response.json();
        currentProduct = product;
        displayProduct(product);
        
        // Load AI recommendations
        await loadAIRecommendations(product);
        
        hideLoading();
    } catch (error) {
        console.error('Error loading product:', error);
        showError('Failed to load product. Using demo data.');
        loadDemoProduct();
    }
}

// Load demo product (fallback)
function loadDemoProduct() {
    const demoProduct = {
        id: 1,
        name: "Classic White T-Shirt",
        title: "Classic White T-Shirt",
        price: 24.99,
        originalPrice: 32.99,
        image: "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=600&h=600&fit=crop",
        image_url: "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=600&h=600&fit=crop",
        category: "tops",
        type: "tshirts",
        description: "Comfortable cotton t-shirt perfect for everyday wear. Made from 100% organic cotton with a relaxed fit. This classic piece features a crew neckline and short sleeves, making it ideal for layering or wearing on its own.",
        brand: "MANVUE Basics",
        rating: 4.5,
        reviews: 127,
        colors: ["White", "Black", "Navy", "Grey"],
        sizes: ["S", "M", "L", "XL", "XXL"],
        tags: ["casual", "cotton", "basic", "everyday", "comfortable"],
        inStock: true,
        features: [
            "100% Organic Cotton",
            "Machine Washable",
            "Pre-shrunk Fabric",
            "Comfortable Fit",
            "Durable Construction"
        ]
    };
    
    currentProduct = demoProduct;
    displayProduct(demoProduct);
    loadAIRecommendations(demoProduct);
}

// Display product information
function displayProduct(product) {
    // Update page title
    const productTitle = product.title || product.name;
    document.title = `${productTitle} - ManVue`;
    document.getElementById('page-title').textContent = `${productTitle} - ManVue`;
    document.getElementById('breadcrumb-product').textContent = productTitle;
    
    // Main product info
    document.getElementById('product-title').textContent = productTitle;
    document.getElementById('product-description-text').textContent = product.description;
    document.getElementById('current-price').textContent = `£${product.price}`;
    document.getElementById('total-price').textContent = `£${product.price}`;
    
    // Rating
    const rating = product.rating || 4.5;
    const reviews = product.reviews || 127;
    document.getElementById('product-rating-text').textContent = `${rating} (${reviews} reviews)`;
    document.getElementById('product-stars').textContent = '⭐'.repeat(Math.floor(rating));
    
    // Original price and discount
    if (product.originalPrice && product.originalPrice > product.price) {
        document.getElementById('original-price').textContent = `£${product.originalPrice}`;
        const discount = Math.round(((product.originalPrice - product.price) / product.originalPrice) * 100);
        document.getElementById('discount').textContent = `${discount}% OFF`;
    } else {
        document.getElementById('original-price').style.display = 'none';
        document.getElementById('discount').style.display = 'none';
    }
    
    // Main image - handle MongoDB image URLs
    let imageUrl = product.image; // Backward compatibility
    if (!imageUrl && product.image_urls && product.image_urls.length > 0) {
        imageUrl = product.image_urls[0];
    } else if (!imageUrl && product.image_ids && product.image_ids.length > 0) {
        imageUrl = `${API_BASE_URL}/api/images/${product.image_ids[0]}`;
    } else if (!imageUrl) {
        // Fallback to placeholder
        imageUrl = "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=600&h=600&fit=crop";
    }
    
    document.getElementById('main-product-image').src = imageUrl;
    document.getElementById('main-product-image').alt = productTitle;
    
    // Thumbnails
    createThumbnails(product);
    
    // Size options
    createSizeOptions(product.sizes || ["S", "M", "L", "XL"]);
    
    // Color options
    createColorOptions(product.colors || ["White", "Black"]);
    
    // Features
    createFeatures(product.features || []);
    
    // Reviews
    createReviews(product);
}

// Create thumbnail images
function createThumbnails(product) {
    const thumbnailContainer = document.getElementById('thumbnail-images');
    thumbnailContainer.innerHTML = '';
    
    let thumbnails = [];
    
    // Collect all available images
    if (product.image_urls && product.image_urls.length > 0) {
        // Use image URLs from MongoDB
        thumbnails = [...product.image_urls];
    } else if (product.image_ids && product.image_ids.length > 0) {
        // Generate URLs from GridFS image IDs
        thumbnails = product.image_ids.map(id => `${API_BASE_URL}/api/images/${id}`);
    } else if (product.image) {
        // Fallback to single image
        thumbnails = [product.image];
    } else {
        // Use placeholder
        thumbnails = ["https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=300&h=300&fit=crop"];
    }
    
    // Add additional images if available (legacy support)
    if (product.additionalImages) {
        thumbnails.push(...product.additionalImages);
    }
    
    thumbnails.forEach((imageUrl, index) => {
        const thumbnail = document.createElement('div');
        thumbnail.className = `thumbnail ${index === 0 ? 'active' : ''}`;
        thumbnail.onclick = () => selectThumbnail(index, imageUrl);
        
        const img = document.createElement('img');
        img.src = imageUrl;
        img.alt = `${product.title || product.name} - Image ${index + 1}`;
        
        thumbnail.appendChild(img);
        thumbnailContainer.appendChild(thumbnail);
    });
}

// Select thumbnail
function selectThumbnail(index, imageUrl) {
    // Update active thumbnail
    document.querySelectorAll('.thumbnail').forEach((thumb, i) => {
        thumb.classList.toggle('active', i === index);
    });
    
    // Update main image
    document.getElementById('main-product-image').src = imageUrl;
}

// Create size options
function createSizeOptions(sizes) {
    const sizeContainer = document.getElementById('size-options');
    sizeContainer.innerHTML = '';
    
    sizes.forEach(size => {
        const sizeOption = document.createElement('div');
        sizeOption.className = 'size-option';
        sizeOption.textContent = size;
        sizeOption.onclick = () => selectSize(size, sizeOption);
        
        // Mark some sizes as unavailable for demo
        if (size === 'XXL' && Math.random() > 0.5) {
            sizeOption.classList.add('unavailable');
        }
        
        sizeContainer.appendChild(sizeOption);
    });
}

// Select size
function selectSize(size, element) {
    if (!requireAuthentication('select product options')) return;
    
    if (element.classList.contains('unavailable')) {
        showMessage('This size is currently unavailable.', 'warning');
        return;
    }
    
    // Update selected size
    document.querySelectorAll('.size-option').forEach(option => {
        option.classList.remove('selected');
    });
    element.classList.add('selected');
    
    selectedSize = size;
    updateTotalPrice();
    
    // Log size selection
    logUserEvent('size_selected', {
        product_id: currentProduct?.id,
        size: size
    });
}

// Create color options
function createColorOptions(colors) {
    const colorContainer = document.getElementById('color-options');
    colorContainer.innerHTML = '';
    
    const colorMap = {
        'White': '#ffffff',
        'Black': '#000000',
        'Navy': '#000080',
        'Grey': '#808080',
        'Red': '#ff0000',
        'Blue': '#0000ff',
        'Green': '#008000',
        'Brown': '#8b4513'
    };
    
    colors.forEach(color => {
        const colorOption = document.createElement('div');
        colorOption.className = 'color-option';
        colorOption.style.backgroundColor = colorMap[color] || '#cccccc';
        colorOption.title = color;
        colorOption.onclick = () => selectColor(color, colorOption);
        
        colorContainer.appendChild(colorOption);
    });
}

// Select color
function selectColor(color, element) {
    if (!requireAuthentication('select product options')) return;
    
    // Update selected color
    document.querySelectorAll('.color-option').forEach(option => {
        option.classList.remove('selected');
    });
    element.classList.add('selected');
    
    selectedColor = color;
    updateTotalPrice();
    
    // Log color selection
    logUserEvent('color_selected', {
        product_id: currentProduct?.id,
        color: color
    });
}

// Create features list
function createFeatures(features) {
    const featuresContainer = document.getElementById('product-features');
    featuresContainer.innerHTML = '';
    
    features.forEach(feature => {
        const li = document.createElement('li');
        li.textContent = feature;
        featuresContainer.appendChild(li);
    });
}

// Create reviews
function createReviews(product) {
    const reviewsContainer = document.getElementById('reviews-list');
    reviewsContainer.innerHTML = '';
    
    const sampleReviews = [
        {
            name: "John D.",
            rating: 5,
            text: "Great quality t-shirt! Fits perfectly and the material is very comfortable. Will definitely buy again."
        },
        {
            name: "Mike S.",
            rating: 4,
            text: "Good product overall. The sizing is accurate and the fabric feels nice. Shipping was fast too."
        },
        {
            name: "Alex R.",
            rating: 5,
            text: "Love this shirt! The quality is excellent and it's become one of my favorites. Highly recommended!"
        }
    ];
    
    sampleReviews.forEach(review => {
        const reviewItem = document.createElement('div');
        reviewItem.className = 'review-item';
        
        reviewItem.innerHTML = `
            <div class="review-header">
                <span class="reviewer-name">${review.name}</span>
                <span class="review-rating">${'⭐'.repeat(review.rating)}</span>
            </div>
            <div class="review-text">${review.text}</div>
        `;
        
        reviewsContainer.appendChild(reviewItem);
    });
}

// Load AI recommendations
async function loadAIRecommendations(product) {
    try {
        showRecommendationsLoading();
        
        // Try to get AI recommendations from API
        const response = await fetch(`${API_BASE_URL}/products/search`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: `similar to ${product.title}`,
                category: product.category
            })
        });
        
        if (response.ok) {
            const results = await response.json();
            displayRecommendations(results.results || []);
        } else {
            throw new Error('API not available');
        }
    } catch (error) {
        console.log('Using fallback recommendations');
        displayFallbackRecommendations(product);
    }
}

// Display AI recommendations
function displayRecommendations(products) {
    // Perfect matches (same category)
    const perfectMatches = products.filter(p => p.category === currentProduct.category).slice(0, 3);
    displayRecommendationCategory('perfect-matches', perfectMatches, 'Perfect Matches');
    
    // Style complements (different but complementary categories)
    const styleComplements = products.filter(p => p.category !== currentProduct.category).slice(0, 3);
    displayRecommendationCategory('style-complements', styleComplements, 'Style Complements');
    
    // Frequently bought together (mix of categories)
    const frequentlyBought = products.slice(0, 3);
    displayRecommendationCategory('frequently-bought', frequentlyBought, 'Frequently Bought Together');
}

// Display fallback recommendations
function displayFallbackRecommendations(product) {
    const fallbackProducts = [
        {
            id: 2,
            name: "Premium Denim Jeans",
            title: "Premium Denim Jeans",
            price: 64.99,
            image: "https://images.unsplash.com/photo-1542272604-787c3835535d?w=300&h=300&fit=crop",
            image_url: "https://images.unsplash.com/photo-1542272604-787c3835535d?w=300&h=300&fit=crop",
            category: "bottoms"
        },
        {
            id: 3,
            name: "Cotton Dress Shirt",
            title: "Cotton Dress Shirt",
            price: 39.99,
            image: "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=300&h=300&fit=crop",
            image_url: "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=300&h=300&fit=crop",
            category: "tops"
        },
        {
            id: 4,
            name: "Athletic Running Trainers",
            title: "Athletic Running Trainers",
            price: 89.99,
            image: "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=300&h=300&fit=crop",
            image_url: "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=300&h=300&fit=crop",
            category: "shoes"
        }
    ];
    
    displayRecommendationCategory('perfect-matches', fallbackProducts.slice(0, 2), 'Perfect Matches');
    displayRecommendationCategory('style-complements', fallbackProducts.slice(1, 3), 'Style Complements');
    displayRecommendationCategory('frequently-bought', fallbackProducts, 'Frequently Bought Together');
}

// Display recommendation category
function displayRecommendationCategory(containerId, products, title) {
    const container = document.getElementById(containerId);
    container.innerHTML = '';
    
    if (products.length === 0) {
        container.innerHTML = '<p>No recommendations available</p>';
        return;
    }
    
    products.forEach(product => {
        const item = document.createElement('div');
        item.className = 'recommendation-item';
        item.onclick = () => goToProduct(product.id);
        
        item.innerHTML = `
            <img src="${product.image_url || product.image}" alt="${product.title || product.name}">
            <h4>${product.title || product.name}</h4>
            <div class="price">£${product.price}</div>
        `;
        
        container.appendChild(item);
    });
}

// Quantity controls
function increaseQuantity() {
    if (!requireAuthentication('adjust quantity')) return;
    
    const quantityInput = document.getElementById('quantity');
    const currentValue = parseInt(quantityInput.value);
    if (currentValue < 10) {
        quantityInput.value = currentValue + 1;
        quantity = currentValue + 1;
        updateTotalPrice();
        
        // Log quantity change
        logUserEvent('quantity_increased', {
            product_id: currentProduct?.id,
            new_quantity: quantity
        });
    } else {
        showMessage('Maximum quantity is 10 items.', 'warning');
    }
}

function decreaseQuantity() {
    if (!requireAuthentication('adjust quantity')) return;
    
    const quantityInput = document.getElementById('quantity');
    const currentValue = parseInt(quantityInput.value);
    if (currentValue > 1) {
        quantityInput.value = currentValue - 1;
        quantity = currentValue - 1;
        updateTotalPrice();
        
        // Log quantity change
        logUserEvent('quantity_decreased', {
            product_id: currentProduct?.id,
            new_quantity: quantity
        });
    } else {
        showMessage('Minimum quantity is 1 item.', 'warning');
    }
}

// Update total price
function updateTotalPrice() {
    if (currentProduct) {
        const total = currentProduct.price * quantity;
        document.getElementById('total-price').textContent = `£${total.toFixed(2)}`;
    }
}

// Add to cart
function addToCart() {
    // Check if user is authenticated
    if (!currentUser) {
        showMessage('Please sign in to add items to your cart.', 'error');
        showLogin();
        return;
    }
    
    if (!currentProduct) {
        showMessage('Product information not available.', 'error');
        return;
    }
    
    if (!selectedSize) {
        showMessage('Please select a size.', 'warning');
        return;
    }
    
    if (!selectedColor) {
        showMessage('Please select a color.', 'warning');
        return;
    }
    
    const cartItem = {
        id: currentProduct.id,
        title: currentProduct.title || currentProduct.name,
        price: currentProduct.price,
        image_url: getProductImageUrl(currentProduct),
        size: selectedSize,
        color: selectedColor,
        quantity: quantity,
        addedAt: new Date().toISOString()
    };
    
    // Check if item already exists in cart
    const existingItemIndex = cart.findIndex(item => 
        item.id === cartItem.id && 
        item.size === cartItem.size && 
        item.color === cartItem.color
    );
    
    if (existingItemIndex > -1) {
        cart[existingItemIndex].quantity += quantity;
        showMessage(`✅ Updated quantity to ${cart[existingItemIndex].quantity}!`, 'success');
    } else {
        cart.push(cartItem);
        showMessage('✅ Product added to cart!', 'success');
    }
    
    localStorage.setItem('cart', JSON.stringify(cart));
    
    // Update cart count
    updateCartCount();
    
    // Animate the cart icon
    animateCartIcon();
}

// Add to wishlist
function addToWishlist() {
    // Check if user is authenticated
    if (!currentUser) {
        showMessage('Please sign in to add items to your wishlist.', 'error');
        showLogin();
        return;
    }
    
    if (!currentProduct) {
        showMessage('Product information not available.', 'error');
        return;
    }
    
    let wishlist = JSON.parse(localStorage.getItem('wishlist')) || [];
    
    const wishlistItem = {
        id: currentProduct.id,
        title: currentProduct.title || currentProduct.name,
        price: currentProduct.price,
        image_url: getProductImageUrl(currentProduct),
        addedAt: new Date().toISOString()
    };
    
    // Check if already in wishlist
    const exists = wishlist.some(item => item.id === wishlistItem.id);
    
    if (!exists) {
        wishlist.push(wishlistItem);
        localStorage.setItem('wishlist', JSON.stringify(wishlist));
        showMessage('❤️ Added to wishlist!', 'success');
        
        // Animate wishlist icon
        const wishlistIcon = document.querySelector('.wishlist-icon');
        if (wishlistIcon) {
            wishlistIcon.classList.add('bounce');
            setTimeout(() => {
                wishlistIcon.classList.remove('bounce');
            }, 600);
        }
    } else {
        showMessage('Already in wishlist!', 'info');
    }
}

// Image zoom functionality
function toggleImageZoom() {
    if (!requireAuthentication('view product images')) return;
    
    const modal = document.getElementById('image-zoom-modal');
    const zoomedImage = document.getElementById('zoomed-image');
    const mainImage = document.getElementById('main-product-image');
    
    zoomedImage.src = mainImage.src;
    modal.style.display = 'block';
    
    // Log image zoom
    logUserEvent('image_zoomed', {
        product_id: currentProduct?.id,
        image_url: mainImage.src
    });
}

function closeImageZoom() {
    const modal = document.getElementById('image-zoom-modal');
    modal.style.display = 'none';
}

// Navigate to product
function goToProduct(productId) {
    if (!requireAuthentication('view other products')) return;
    
    // Log product navigation
    logUserEvent('product_navigation', {
        from_product_id: currentProduct?.id,
        to_product_id: productId
    });
    
    window.location.href = `product.html?id=${productId}`;
}

// Utility functions
function showLoading() {
    // Add loading indicator
    const loading = document.createElement('div');
    loading.id = 'loading-indicator';
    loading.innerHTML = '<div class="loading-spinner">Loading...</div>';
    loading.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(255,255,255,0.9);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1000;
    `;
    document.body.appendChild(loading);
}

function hideLoading() {
    const loading = document.getElementById('loading-indicator');
    if (loading) {
        loading.remove();
    }
}

function showError(message) {
    showMessage(message, 'error');
}

function showMessage(message, type = 'info') {
    // Remove any existing messages
    const existingMessages = document.querySelectorAll('.toast-message');
    existingMessages.forEach(msg => msg.remove());
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `toast-message toast-${type}`;
    messageDiv.innerHTML = `
        <div class="toast-content">
            <span class="toast-icon">${getToastIcon(type)}</span>
            <span class="toast-text">${message}</span>
            <button class="toast-close" onclick="this.parentElement.parentElement.remove()">×</button>
        </div>
    `;
    
    messageDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        min-width: 300px;
        max-width: 500px;
        background: white;
        border-radius: 8px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
        z-index: 2001;
        animation: slideInRight 0.3s ease;
        border-left: 4px solid ${getToastColor(type)};
    `;
    
    const toastContent = messageDiv.querySelector('.toast-content');
    toastContent.style.cssText = `
        display: flex;
        align-items: center;
        padding: 1rem;
        gap: 0.5rem;
    `;
    
    const toastIcon = messageDiv.querySelector('.toast-icon');
    toastIcon.style.cssText = `
        font-size: 1.2rem;
        color: ${getToastColor(type)};
    `;
    
    const toastText = messageDiv.querySelector('.toast-text');
    toastText.style.cssText = `
        flex: 1;
        color: #333;
        font-weight: 500;
    `;
    
    const toastClose = messageDiv.querySelector('.toast-close');
    toastClose.style.cssText = `
        background: none;
        border: none;
        font-size: 1.5rem;
        color: #999;
        cursor: pointer;
        padding: 0;
        margin-left: auto;
    `;
    
    document.body.appendChild(messageDiv);
    
    // Auto-remove after duration based on type
    const duration = type === 'error' ? 5000 : 3000;
    setTimeout(() => {
        if (messageDiv.parentElement) {
            messageDiv.remove();
        }
    }, duration);
}

function getToastIcon(type) {
    switch (type) {
        case 'success': return '✅';
        case 'error': return '❌';
        case 'warning': return '⚠️';
        case 'info': return 'ℹ️';
        default: return 'ℹ️';
    }
}

function getToastColor(type) {
    switch (type) {
        case 'success': return '#28a745';
        case 'error': return '#dc3545';
        case 'warning': return '#ffc107';
        case 'info': return '#17a2b8';
        default: return '#6c757d';
    }
}

function showRecommendationsLoading() {
    const containers = ['perfect-matches', 'style-complements', 'frequently-bought'];
    containers.forEach(id => {
        const container = document.getElementById(id);
        container.innerHTML = '<div class="loading">🤖 AI is analyzing...</div>';
    });
}

function updateCartCount() {
    // Update cart count in header if it exists
    const cartCount = document.querySelector('.cart-count');
    if (cartCount) {
        const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
        cartCount.textContent = totalItems;
    }
}

// Animate cart icon when item is added
function animateCartIcon() {
    const cartIcon = document.querySelector('.cart-icon');
    if (cartIcon) {
        cartIcon.classList.add('bounce');
        setTimeout(() => {
            cartIcon.classList.remove('bounce');
        }, 600);
    }
}

// Cart and Wishlist Management
function toggleCart() {
    if (!currentUser) {
        showMessage('Please sign in to view your cart.', 'warning');
        showLogin();
        return;
    }
    
    const cartSidebar = document.getElementById('cart-sidebar');
    if (cartSidebar) {
        cartSidebar.classList.toggle('active');
        updateCartDisplay();
    }
}

function toggleWishlist() {
    if (!currentUser) {
        showMessage('Please sign in to view your wishlist.', 'warning');
        showLogin();
        return;
    }
    
    const wishlistSidebar = document.getElementById('wishlist-sidebar');
    if (wishlistSidebar) {
        wishlistSidebar.classList.toggle('active');
        updateWishlistDisplay();
    }
}

function updateCartDisplay() {
    const cartItems = document.getElementById('cart-items');
    const cartTotal = document.getElementById('cart-total');
    
    if (!cartItems || !cartTotal) return;
    
    if (cart.length === 0) {
        cartItems.innerHTML = '<div class="empty-cart">Your cart is empty</div>';
        cartTotal.textContent = '0.00';
        return;
    }
    
    let total = 0;
    cartItems.innerHTML = '';
    
    cart.forEach((item, index) => {
        total += item.price * item.quantity;
        
        const cartItem = document.createElement('div');
        cartItem.className = 'cart-item';
        cartItem.innerHTML = `
            <img src="${item.image_url}" alt="${item.title}" class="cart-item-image">
            <div class="cart-item-details">
                <h4>${item.title}</h4>
                <p>Size: ${item.size} | Color: ${item.color}</p>
                <div class="cart-item-price">£${item.price} x ${item.quantity}</div>
            </div>
            <button onclick="removeFromCart(${index})" class="remove-btn">×</button>
        `;
        cartItems.appendChild(cartItem);
    });
    
    cartTotal.textContent = total.toFixed(2);
}

function updateWishlistDisplay() {
    const wishlistItems = document.getElementById('wishlist-items');
    if (!wishlistItems) return;
    
    const wishlist = JSON.parse(localStorage.getItem('wishlist')) || [];
    
    if (wishlist.length === 0) {
        wishlistItems.innerHTML = '<div class="empty-wishlist">Your wishlist is empty</div>';
        return;
    }
    
    wishlistItems.innerHTML = '';
    
    wishlist.forEach((item, index) => {
        const wishlistItem = document.createElement('div');
        wishlistItem.className = 'wishlist-item';
        wishlistItem.innerHTML = `
            <img src="${item.image_url}" alt="${item.title}" class="wishlist-item-image">
            <div class="wishlist-item-details">
                <h4>${item.title}</h4>
                <div class="wishlist-item-price">£${item.price}</div>
            </div>
            <button onclick="removeFromWishlist(${index})" class="remove-btn">×</button>
        `;
        wishlistItems.appendChild(wishlistItem);
    });
}

function removeFromCart(index) {
    cart.splice(index, 1);
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartCount();
    updateCartDisplay();
    showMessage('Item removed from cart.', 'info');
}

function removeFromWishlist(index) {
    const wishlist = JSON.parse(localStorage.getItem('wishlist')) || [];
    wishlist.splice(index, 1);
    localStorage.setItem('wishlist', JSON.stringify(wishlist));
    updateWishlistDisplay();
    showMessage('Item removed from wishlist.', 'info');
}

function proceedToCheckout() {
    if (cart.length === 0) {
        showMessage('Your cart is empty.', 'warning');
        return;
    }
    
    showMessage('Checkout feature coming soon!', 'info');
}

// Utility function to navigate to search page
function goToSearchPage() {
    window.location.href = 'index.html#search';
}

// Validation Functions
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function isValidPhone(phone) {
    // Remove all non-digit characters for validation
    const phoneDigits = phone.replace(/\D/g, '');
    // Check if it has at least 10 digits (covers most international formats)
    return phoneDigits.length >= 10 && phoneDigits.length <= 15;
}

// Enhanced authentication check for all actions
function requireAuthentication(actionName = 'perform this action') {
    if (!currentUser) {
        showMessage(`🔒 Please sign in to ${actionName}.`, 'error');
        showLogin();
        return false;
    }
    return true;
}

// User event logging for analytics
function logUserEvent(eventType, eventData = {}) {
    const events = JSON.parse(localStorage.getItem('manvue_events') || '[]');
    events.push({
        type: eventType,
        data: eventData,
        timestamp: new Date().toISOString(),
        userId: currentUser?.id || null
    });
    localStorage.setItem('manvue_events', JSON.stringify(events));
}

// Terms and Privacy functions
function showTerms() {
    showMessage('Terms & Conditions: By creating an account, you agree to our terms of service. Full terms available at manvue.com/terms', 'info');
}

function showPrivacy() {
    showMessage('Privacy Policy: We protect your personal information. Read our full privacy policy at manvue.com/privacy', 'info');
}

// Helper function for getting product image URL (MongoDB-compatible)
function getProductImageUrl(product) {
    // Check for direct image property (backward compatibility)
    if (product.image) {
        return product.image;
    }
    
    // Check for image_urls array from MongoDB
    if (product.image_urls && product.image_urls.length > 0) {
        return product.image_urls[0];
    }
    
    // Check for image_ids array and generate GridFS URLs
    if (product.image_ids && product.image_ids.length > 0) {
        return `${API_BASE_URL}/api/images/${product.image_ids[0]}`;
    }
    
    // Fallback to placeholder image
    return "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop";
}

// Add CSS animation for messages
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    .loading-spinner {
        font-size: 1.2rem;
        color: #007bff;
    }
    
    .loading {
        text-align: center;
        padding: 2rem;
        color: #6c757d;
        font-style: italic;
    }
`;
document.head.appendChild(style);
