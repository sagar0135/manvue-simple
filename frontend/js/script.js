// MANVUE - Smart Fashion Store JavaScript

// Home Navigation Function
function goHome() {
    // Reset to home view
    showSection('home');
    clearAllFilters();
    scrollToTop();
    closeAllMenus();
}

// Scroll to top function
function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Enhanced Men's Fashion Data with Advanced Filtering
const products = [
    {
        id: 1,
        name: "Classic White T-Shirt",
        price: 24.99,
        originalPrice: 32.99,
        category: "men",
        type: "tops",
        size: ["S", "M", "L", "XL", "XXL"],
        color: ["White", "Black", "Navy", "Grey"],
        brand: "MANVUE Basics",
        rating: 4.5,
        reviews: 127,
        image: "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop",
        tags: ["casual", "cotton", "basic", "everyday", "comfortable"],
        inStock: true,
        description: "Comfortable cotton t-shirt perfect for everyday wear. Made from 100% organic cotton with a relaxed fit."
    },
    {
        id: 2,
        name: "Premium Denim Jeans",
        price: 64.99,
        originalPrice: 74.99,
        category: "men",
        type: "bottoms",
        size: ["30", "32", "34", "36", "38", "40"],
        color: ["Dark Blue", "Black", "Light Blue", "Grey"],
        brand: "MANVUE Denim",
        rating: 4.7,
        reviews: 189,
        image: "https://images.unsplash.com/photo-1542272604-787c3835535d?w=400&h=400&fit=crop",
        tags: ["denim", "classic", "casual", "slim-fit", "premium"],
        inStock: true,
        description: "Premium denim jeans with a perfect fit. Slim cut with stretch comfort and reinforced stitching."
    },
    {
        id: 3,
        name: "Athletic Running Trainers",
        price: 104.99,
        originalPrice: 124.99,
        category: "men",
        type: "shoes",
        size: ["7", "8", "9", "10", "11", "12"],
        color: ["White", "Black", "Grey", "Navy"],
        brand: "SportMax",
        rating: 4.8,
        reviews: 334,
        image: "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400&h=400&fit=crop",
        tags: ["sports", "running", "comfort", "breathable", "athletic"],
        inStock: true,
        description: "High-performance running trainers with breathable mesh upper and responsive cushioning."
    },
    {
        id: 4,
        name: "Business Formal Shirt",
        price: 44.99,
        originalPrice: 54.99,
        category: "men",
        type: "tops",
        size: ["S", "M", "L", "XL", "XXL"],
        color: ["White", "Light Blue", "Navy", "Pink"],
        brand: "MANVUE Professional",
        rating: 4.6,
        reviews: 256,
        image: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=400&fit=crop",
        tags: ["formal", "business", "professional", "cotton", "crisp"],
        inStock: true,
        description: "Professional dress shirt perfect for business meetings. Non-iron cotton with modern fit."
    },
    {
        id: 5,
        name: "Leather Wallet",
        price: 34.99,
        originalPrice: 44.99,
        category: "men",
        type: "accessories",
        size: ["One Size"],
        color: ["Brown", "Black", "Tan", "Navy"],
        brand: "LuxeLeather",
        rating: 4.9,
        reviews: 178,
        image: "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400&h=400&fit=crop",
        tags: ["luxury", "leather", "wallet", "essential", "premium"],
        inStock: true,
        description: "Premium leather wallet with RFID blocking. Multiple card slots and spacious bill compartment."
    },
    {
        id: 6,
        name: "Baseball Cap",
        price: 19.99,
        originalPrice: 24.99,
        category: "men",
        type: "accessories",
        size: ["One Size"],
        color: ["Navy", "Black", "White", "Grey"],
        brand: "MANVUE Sports",
        rating: 4.3,
        reviews: 192,
        image: "https://images.unsplash.com/photo-1575428652377-a4d25358c08c?w=400&h=400&fit=crop",
        tags: ["casual", "sports", "cap", "sun-protection", "adjustable"],
        inStock: true,
        description: "Classic baseball cap with adjustable strap. Perfect for casual outings and sun protection."
    },
    {
        id: 7,
        name: "Winter Puffer Jacket",
        price: 149.99,
        originalPrice: 189.99,
        category: "men",
        type: "outerwear",
        size: ["S", "M", "L", "XL", "XXL"],
        color: ["Black", "Navy", "Forest Green", "Charcoal"],
        brand: "WarmGuard",
        rating: 4.7,
        reviews: 245,
        image: "https://images.unsplash.com/photo-1551698618-1dfe5d97d256?w=400&h=400&fit=crop",
        tags: ["winter", "warm", "puffer", "waterproof", "insulated"],
        inStock: true,
        description: "Premium winter puffer jacket with down insulation. Water-resistant with adjustable hood."
    },
    {
        id: 8,
        name: "Classic Wrist Watch",
        price: 199.99,
        originalPrice: 249.99,
        category: "men",
        type: "accessories",
        size: ["One Size"],
        color: ["Silver", "Gold", "Black", "Rose Gold"],
        brand: "TimeClass",
        rating: 4.8,
        reviews: 267,
        image: "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=400&fit=crop",
        tags: ["elegant", "watch", "formal", "leather-strap", "classic"],
        inStock: true,
        description: "Elegant classic watch with leather strap. Water-resistant with precise quartz movement."
    },
    {
        id: 9,
        name: "Casual Polo Shirt",
        price: 39.99,
        originalPrice: 49.99,
        category: "men",
        type: "tops",
        size: ["S", "M", "L", "XL", "XXL"],
        color: ["Navy", "White", "Red", "Green", "Grey"],
        brand: "MANVUE Polo",
        rating: 4.4,
        reviews: 303,
        image: "https://images.unsplash.com/photo-1586790170083-2f9ceadc732d?w=400&h=400&fit=crop",
        tags: ["polo", "casual", "cotton", "collar", "versatile"],
        inStock: true,
        description: "Classic polo shirt perfect for casual or smart-casual occasions. 100% cotton pique fabric."
    },
    {
        id: 10,
        name: "Dress Shoes",
        price: 89.99,
        originalPrice: 119.99,
        category: "men",
        type: "shoes",
        size: ["7", "8", "9", "10", "11", "12"],
        color: ["Black", "Brown", "Tan"],
        brand: "FormalSteps",
        rating: 4.5,
        reviews: 124,
        image: "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400&h=400&fit=crop",
        tags: ["formal", "dress", "leather", "professional", "elegant"],
        inStock: true,
        description: "Classic leather dress shoes perfect for business and formal occasions. Genuine leather construction."
    },
    {
        id: 11,
        name: "Cargo Shorts",
        price: 32.99,
        originalPrice: 42.99,
        category: "men",
        type: "bottoms",
        size: ["30", "32", "34", "36", "38"],
        color: ["Khaki", "Navy", "Black", "Olive"],
        brand: "MANVUE Outdoor",
        rating: 4.1,
        reviews: 187,
        image: "https://images.unsplash.com/photo-1473966968600-fa801b869a1a?w=400&h=400&fit=crop",
        tags: ["casual", "shorts", "cargo", "summer", "practical"],
        inStock: true,
        description: "Comfortable cargo shorts with multiple utility pockets. Perfect for outdoor activities and summer wear."
    },
    {
        id: 12,
        name: "Wool Scarf",
        price: 24.99,
        originalPrice: 34.99,
        category: "men",
        type: "accessories",
        size: ["One Size"],
        color: ["Charcoal", "Navy", "Burgundy", "Camel"],
        brand: "WoolCraft",
        rating: 4.6,
        reviews: 145,
        image: "https://images.unsplash.com/photo-1551698618-1dfe5d97d256?w=400&h=400&fit=crop",
        tags: ["wool", "winter", "scarf", "warm", "sophisticated"],
        inStock: true,
        description: "Premium wool scarf with classic patterns. Essential winter accessory for style and warmth."
    }
];

// Shopping Cart
let cart = [];
let currentFilter = 'all';
let currentSection = 'home';

// Filter State
let currentFilters = {
    category: 'all',
    type: '',
    brand: '',
    priceMin: 0,
    priceMax: 250,
    inStockOnly: true,
    sortBy: 'name'
};

let currentView = 'grid';
let displayedProducts = [];
let currentPage = 1;
const productsPerPage = 6;

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
    loadProducts();
    showSection('home');
});

// Section Navigation
function showSection(sectionName) {
    // Hide all sections
    const sections = document.querySelectorAll('.section');
    sections.forEach(section => section.classList.remove('active'));
    
    // Show selected section
    const targetSection = document.getElementById(sectionName);
    if (targetSection) {
        targetSection.classList.add('active');
        currentSection = sectionName;
    }
    
    // Close mobile menu if open
    closeMobileMenu();
}

// Mobile Menu Functions
function toggleMobileMenu() {
    const navMobile = document.querySelector('.nav-mobile');
    navMobile.classList.toggle('active');
}

function closeMobileMenu() {
    const navMobile = document.querySelector('.nav-mobile');
    navMobile.classList.remove('active');
}

// Search Functions
function toggleSearch() {
    const searchBar = document.querySelector('.search-bar');
    const overlay = document.getElementById('overlay');
    
    searchBar.classList.toggle('active');
    
    if (searchBar.classList.contains('active')) {
        overlay.classList.add('active');
        document.getElementById('search-input').focus();
    } else {
        overlay.classList.remove('active');
    }
}

function searchProducts() {
    const searchTerm = document.getElementById('search-input').value.toLowerCase();
    
    if (!searchTerm) {
        loadProducts();
        return;
    }
    
    const filteredProducts = products.filter(product => 
        product.name.toLowerCase().includes(searchTerm) ||
        product.description.toLowerCase().includes(searchTerm) ||
        product.category.toLowerCase().includes(searchTerm)
    );
    
    displayProducts(filteredProducts);
    showSection('products');
    toggleSearch();
}

// Voice Search Function (Basic Implementation)
function startVoiceSearch() {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = 'en-US';
        recognition.continuous = false;
        recognition.interimResults = false;
        
        recognition.onstart = function() {
            console.log('Voice search started');
            alert('Voice search started! Speak now...');
        };
        
        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            document.getElementById('search-input').value = transcript;
            searchProducts();
        };
        
        recognition.onerror = function(event) {
            console.error('Voice search error:', event.error);
            alert('Voice search not available. Please type your search.');
        };
        
        recognition.start();
    } else {
        alert('Voice search not supported in this browser. Please type your search.');
    }
}

// Product Functions
function loadProducts() {
    displayProducts(products);
}

function filterProducts(category) {
    currentFilter = category;
    currentFilters.category = category;
    
    // Update filter buttons
    const categoryBtns = document.querySelectorAll('.filter-group:first-child .filter-btn');
    categoryBtns.forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    
    applyAllFilters();
    showSection('products');
}

function displayProducts(productsToShow) {
    const productGrid = document.getElementById('product-grid');
    productGrid.innerHTML = '';
    
    // Update results count
    updateResultsCount(productsToShow.length);
    
    if (productsToShow.length === 0) {
        productGrid.innerHTML = '<div style="text-align: center; padding: 40px; color: #666;"><h3>No products found</h3><p>Try adjusting your filters or search terms.</p></div>';
        return;
    }
    
    // Store displayed products for pagination
    displayedProducts = productsToShow;
    
    // Show products based on pagination
    const startIndex = (currentPage - 1) * productsPerPage;
    const endIndex = startIndex + productsPerPage;
    const paginatedProducts = productsToShow.slice(startIndex, endIndex);
    
    paginatedProducts.forEach(product => {
        const productCard = document.createElement('div');
        productCard.className = 'product-card';
        
        // Calculate discount percentage
        const discount = product.originalPrice > product.price ? 
            Math.round(((product.originalPrice - product.price) / product.originalPrice) * 100) : 0;
        
        // Generate star rating
        const stars = generateStars(product.rating);
        
        productCard.innerHTML = `
            <div class="product-image">
                <img src="${product.image}" alt="${product.name}" />
            </div>
            <div class="product-info">
                <div class="product-brand">${product.brand}</div>
                <h3 class="product-title">${product.name}</h3>
                <div class="product-rating">
                    <span class="stars">${stars}</span>
                    <span class="review-count">(${product.reviews})</span>
                </div>
                <div class="product-price">
                    <span class="current-price">£${product.price}</span>
                    ${product.originalPrice > product.price ? 
                        `<span class="original-price">£${product.originalPrice}</span>
                         <span class="discount-badge">${discount}% OFF</span>` : ''}
                </div>
                <div class="stock-status ${product.inStock ? 'in-stock' : 'out-of-stock'}">
                    ${product.inStock ? '✓ In Stock' : '✗ Out of Stock'}
                </div>
                <div class="product-actions">
                    <button class="add-to-cart" onclick="addToCart(${product.id})" 
                            ${!product.inStock ? 'disabled style="opacity: 0.5; cursor: not-allowed;"' : ''}>
                        ${product.inStock ? 'Add to Cart' : 'Out of Stock'}
                    </button>
                    <button class="quick-view" onclick="quickView(${product.id})">
                        Quick View
                    </button>
                </div>
            </div>
        `;
        productGrid.appendChild(productCard);
    });
    
    // Show/hide load more button
    updateLoadMoreButton();
}

function generateStars(rating) {
    const fullStars = Math.floor(rating);
    const halfStar = rating % 1 >= 0.5;
    const emptyStars = 5 - fullStars - (halfStar ? 1 : 0);
    
    return '★'.repeat(fullStars) + 
           (halfStar ? '☆' : '') + 
           '☆'.repeat(emptyStars);
}

function updateResultsCount(count) {
    const resultsCount = document.getElementById('results-count');
    if (count === products.length) {
        resultsCount.textContent = `Showing all ${count} products`;
    } else {
        resultsCount.textContent = `Showing ${count} of ${products.length} products`;
    }
}

function updateLoadMoreButton() {
    const loadMoreBtn = document.getElementById('load-more-btn');
    const totalPages = Math.ceil(displayedProducts.length / productsPerPage);
    
    if (currentPage < totalPages) {
        loadMoreBtn.style.display = 'block';
        loadMoreBtn.textContent = `Load More (${displayedProducts.length - (currentPage * productsPerPage)} remaining)`;
    } else {
        loadMoreBtn.style.display = 'none';
    }
}

function quickView(productId) {
    const product = products.find(p => p.id === productId);
    if (product) {
        alert(`${product.name}\n\nPrice: $${product.price}\n\n${product.description}\n\nCategory: ${product.category}`);
    }
}

// Cart Functions
function addToCart(productId) {
    const product = products.find(p => p.id === productId);
    if (product) {
        cart.push(product);
        updateCartDisplay();
        showMessage(`${product.name} added to cart!`);
    }
}

function toggleCart() {
    const cartSidebar = document.getElementById('cart-sidebar');
    const overlay = document.getElementById('overlay');
    
    cartSidebar.classList.toggle('active');
    overlay.classList.toggle('active');
    
    if (cartSidebar.classList.contains('active')) {
        updateCartItems();
    }
}

function updateCartDisplay() {
    const cartCount = document.getElementById('cart-count');
    cartCount.textContent = cart.length;
}

function updateCartItems() {
    const cartItems = document.getElementById('cart-items');
    const cartTotal = document.getElementById('cart-total');
    
    if (cart.length === 0) {
        cartItems.innerHTML = '<p>Your cart is empty</p>';
        cartTotal.textContent = '0.00';
        return;
    }
    
    let total = 0;
    cartItems.innerHTML = '';
    
    cart.forEach((item, index) => {
        total += item.price;
        const cartItem = document.createElement('div');
        cartItem.className = 'cart-item';
        cartItem.innerHTML = `
            <div style="display: flex; align-items: center; padding: 10px; border-bottom: 1px solid #eee;">
                <span style="font-size: 2rem; margin-right: 10px;">${item.image}</span>
                <div style="flex: 1;">
                    <h4>${item.name}</h4>
                    <p>$${item.price}</p>
                </div>
                <button onclick="removeFromCart(${index})" style="background: #e74c3c; color: white; border: none; padding: 5px 10px; border-radius: 4px; cursor: pointer;">Remove</button>
            </div>
        `;
        cartItems.appendChild(cartItem);
    });
    
    cartTotal.textContent = total.toFixed(2);
}

function removeFromCart(index) {
    cart.splice(index, 1);
    updateCartDisplay();
    updateCartItems();
}

function checkout() {
    if (cart.length === 0) {
        alert('Your cart is empty!');
        return;
    }
    
    const total = cart.reduce((sum, item) => sum + item.price, 0);
    alert(`Checkout successful!\n\nTotal: $${total.toFixed(2)}\n\nThank you for shopping with MANVUE!`);
    
    cart = [];
    updateCartDisplay();
    toggleCart();
}

// User Menu Functions
function toggleUserMenu() {
    const userMenu = document.getElementById('user-menu');
    const overlay = document.getElementById('overlay');
    
    userMenu.classList.toggle('active');
    overlay.classList.toggle('active');
}

function showLogin() {
    alert('Login feature coming soon!');
    toggleUserMenu();
}

function showRegister() {
    alert('Registration feature coming soon!');
    toggleUserMenu();
}

function showProfile() {
    alert('Profile feature coming soon!');
    toggleUserMenu();
}

function showOrders() {
    alert('Orders feature coming soon!');
    toggleUserMenu();
}

// Chatbot Functions
function toggleChatbot() {
    const chatbot = document.getElementById('chatbot');
    chatbot.classList.toggle('active');
}

function sendChatMessage() {
    const chatInput = document.getElementById('chat-input');
    const chatMessages = document.getElementById('chat-messages');
    const message = chatInput.value.trim();
    
    if (!message) return;
    
    // Add user message
    const userMessage = document.createElement('div');
    userMessage.className = 'user-message';
    userMessage.textContent = message;
    chatMessages.appendChild(userMessage);
    
    // Clear input
    chatInput.value = '';
    
    // Simulate bot response
    setTimeout(() => {
        const botMessage = document.createElement('div');
        botMessage.className = 'bot-message';
        botMessage.textContent = getBotResponse(message);
        chatMessages.appendChild(botMessage);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }, 1000);
    
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function getBotResponse(message) {
    const lowerMessage = message.toLowerCase();
    
    if (lowerMessage.includes('hello') || lowerMessage.includes('hi')) {
        return "Hello! I'm your style assistant. How can I help you find the perfect outfit today?";
    } else if (lowerMessage.includes('recommend') || lowerMessage.includes('suggest')) {
        return "I'd be happy to recommend some items! What type of clothing are you looking for? Casual, formal, or something specific?";
    } else if (lowerMessage.includes('size') || lowerMessage.includes('fit')) {
        return "For sizing, I recommend checking our size guide. Most items run true to size, but I can help you find the perfect fit!";
    } else if (lowerMessage.includes('color') || lowerMessage.includes('style')) {
        return "Great question! What colors do you usually prefer? I can suggest items that match your style preferences.";
    } else if (lowerMessage.includes('price') || lowerMessage.includes('cost')) {
        return "We have items for every budget! Our prices range from $24.99 to $299.99. What's your budget range?";
    } else {
        return "That's interesting! I'm here to help with any fashion questions. Feel free to ask about our products, styling tips, or anything else!";
    }
}

// Feature Demo Functions
function startStyleQuiz() {
    alert('Style Quiz coming soon! This will help us recommend the perfect items for your style.');
}

function show3DDemo() {
    alert('3D Try-On feature coming soon! You\'ll be able to see how clothes look on you using your camera.');
}

function showChatbot() {
    toggleChatbot();
}

// Utility Functions
function showMessage(message) {
    // Simple alert for now - can be enhanced with toast notifications
    alert(message);
}

function closeAllMenus() {
    const overlay = document.getElementById('overlay');
    const cartSidebar = document.getElementById('cart-sidebar');
    const userMenu = document.getElementById('user-menu');
    const searchBar = document.querySelector('.search-bar');
    const navMobile = document.querySelector('.nav-mobile');
    
    overlay.classList.remove('active');
    cartSidebar.classList.remove('active');
    userMenu.classList.remove('active');
    searchBar.classList.remove('active');
    navMobile.classList.remove('active');
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Escape key closes all menus
    if (e.key === 'Escape') {
        closeAllMenus();
    }
    
    // Ctrl/Cmd + K opens search
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        toggleSearch();
    }
});

// Chat input enter key
document.addEventListener('DOMContentLoaded', function() {
    const chatInput = document.getElementById('chat-input');
    if (chatInput) {
        chatInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendChatMessage();
            }
        });
    }
    
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                searchProducts();
            }
        });
    }
});

// Advanced Filtering Functions

function applyAllFilters() {
    let filteredProducts = products;
    
    // Category filter
    if (currentFilters.category !== 'all') {
        filteredProducts = filteredProducts.filter(product => 
            product.category === currentFilters.category
        );
    }
    
    // Type filter
    if (currentFilters.type) {
        filteredProducts = filteredProducts.filter(product => 
            product.type === currentFilters.type
        );
    }
    
    // Brand filter
    if (currentFilters.brand) {
        filteredProducts = filteredProducts.filter(product => 
            product.brand === currentFilters.brand
        );
    }
    
    // Price range filter
    filteredProducts = filteredProducts.filter(product => 
        product.price >= currentFilters.priceMin && 
        product.price <= currentFilters.priceMax
    );
    
    // Stock filter
    if (currentFilters.inStockOnly) {
        filteredProducts = filteredProducts.filter(product => product.inStock);
    }
    
    // Sort products
    filteredProducts = sortProductsArray(filteredProducts, currentFilters.sortBy);
    
    // Reset pagination
    currentPage = 1;
    
    displayProducts(filteredProducts);
}

function sortProductsArray(productsArray, sortBy) {
    const sorted = [...productsArray];
    
    switch (sortBy) {
        case 'name':
            return sorted.sort((a, b) => a.name.localeCompare(b.name));
        case 'price-low':
            return sorted.sort((a, b) => a.price - b.price);
        case 'price-high':
            return sorted.sort((a, b) => b.price - a.price);
        case 'rating':
            return sorted.sort((a, b) => b.rating - a.rating);
        case 'newest':
            return sorted.sort((a, b) => b.id - a.id);
        default:
            return sorted;
    }
}

function filterByType(type) {
    // Update button states
    const typeBtns = document.querySelectorAll('.filter-group:nth-child(2) .filter-btn');
    typeBtns.forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    
    currentFilters.type = type;
    applyAllFilters();
}

function filterByBrand() {
    const brandSelect = document.getElementById('brand-filter');
    currentFilters.brand = brandSelect.value;
    applyAllFilters();
}

function filterByStock() {
    const stockCheckbox = document.getElementById('in-stock-filter');
    currentFilters.inStockOnly = stockCheckbox.checked;
    applyAllFilters();
}

function updatePriceFilter() {
    const priceMin = document.getElementById('price-min');
    const priceMax = document.getElementById('price-max');
    const priceMinDisplay = document.getElementById('price-min-display');
    const priceMaxDisplay = document.getElementById('price-max-display');
    
    // Ensure min is not greater than max
    if (parseInt(priceMin.value) > parseInt(priceMax.value)) {
        priceMin.value = priceMax.value;
    }
    
    currentFilters.priceMin = parseInt(priceMin.value);
    currentFilters.priceMax = parseInt(priceMax.value);
    
    priceMinDisplay.textContent = currentFilters.priceMin;
    priceMaxDisplay.textContent = currentFilters.priceMax;
    
    applyAllFilters();
}

function sortProducts() {
    const sortSelect = document.getElementById('sort-select');
    currentFilters.sortBy = sortSelect.value;
    applyAllFilters();
}

function changeView(viewType) {
    // Update button states
    const viewBtns = document.querySelectorAll('.view-btn');
    viewBtns.forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    
    currentView = viewType;
    const productGrid = document.getElementById('product-grid');
    
    if (viewType === 'list') {
        productGrid.classList.add('list-view');
    } else {
        productGrid.classList.remove('list-view');
    }
}

function clearAllFilters() {
    // Reset all filters
    currentFilters = {
        category: 'all',
        type: '',
        brand: '',
        priceMin: 0,
        priceMax: 250,
        inStockOnly: true,
        sortBy: 'name'
    };
    
    // Reset UI elements
    document.getElementById('price-min').value = 0;
    document.getElementById('price-max').value = 250;
    document.getElementById('price-min-display').textContent = '0';
    document.getElementById('price-max-display').textContent = '250';
    document.getElementById('brand-filter').value = '';
    document.getElementById('in-stock-filter').checked = true;
    document.getElementById('sort-select').value = 'name';
    
    // Reset filter buttons
    const allFilterBtns = document.querySelectorAll('.filter-btn');
    allFilterBtns.forEach(btn => btn.classList.remove('active'));
    
    // Set "All" as active for category
    const categoryBtns = document.querySelectorAll('.filter-group:first-child .filter-btn');
    if (categoryBtns[0]) categoryBtns[0].classList.add('active');
    
    // Apply filters
    applyAllFilters();
}

function loadMoreProducts() {
    currentPage++;
    
    // Re-display products with new page
    const startIndex = (currentPage - 1) * productsPerPage;
    const endIndex = startIndex + productsPerPage;
    const paginatedProducts = displayedProducts.slice(startIndex, endIndex);
    
    const productGrid = document.getElementById('product-grid');
    
    paginatedProducts.forEach(product => {
        const productCard = document.createElement('div');
        productCard.className = 'product-card';
        
        const discount = product.originalPrice > product.price ? 
            Math.round(((product.originalPrice - product.price) / product.originalPrice) * 100) : 0;
        const stars = generateStars(product.rating);
        
        productCard.innerHTML = `
            <div class="product-image">${product.image}</div>
            <div class="product-info">
                <div class="product-brand">${product.brand}</div>
                <h3 class="product-title">${product.name}</h3>
                <div class="product-rating">
                    <span class="stars">${stars}</span>
                    <span class="review-count">(${product.reviews})</span>
                </div>
                <div class="product-price">
                    <span class="current-price">$${product.price}</span>
                    ${product.originalPrice > product.price ? 
                        `<span class="original-price">$${product.originalPrice}</span>
                         <span class="discount-badge">${discount}% OFF</span>` : ''}
                </div>
                <div class="stock-status ${product.inStock ? 'in-stock' : 'out-of-stock'}">
                    ${product.inStock ? '✓ In Stock' : '✗ Out of Stock'}
                </div>
                <div class="product-actions">
                    <button class="add-to-cart" onclick="addToCart(${product.id})" 
                            ${!product.inStock ? 'disabled style="opacity: 0.5; cursor: not-allowed;"' : ''}>
                        ${product.inStock ? 'Add to Cart' : 'Out of Stock'}
                    </button>
                    <button class="quick-view" onclick="quickView(${product.id})">
                        Quick View
                    </button>
                </div>
            </div>
        `;
        productGrid.appendChild(productCard);
    });
    
    updateLoadMoreButton();
}

// Enhanced search function
function searchProducts() {
    const searchTerm = document.getElementById('search-input').value.toLowerCase();
    
    if (!searchTerm) {
        applyAllFilters(); // Apply current filters instead of showing all
        return;
    }
    
    let filteredProducts = products.filter(product => 
        product.name.toLowerCase().includes(searchTerm) ||
        product.description.toLowerCase().includes(searchTerm) ||
        product.category.toLowerCase().includes(searchTerm) ||
        product.brand.toLowerCase().includes(searchTerm) ||
        product.tags.some(tag => tag.toLowerCase().includes(searchTerm))
    );
    
    // Apply other filters to search results
    if (currentFilters.category !== 'all') {
        filteredProducts = filteredProducts.filter(product => 
            product.category === currentFilters.category
        );
    }
    
    if (currentFilters.type) {
        filteredProducts = filteredProducts.filter(product => 
            product.type === currentFilters.type
        );
    }
    
    if (currentFilters.brand) {
        filteredProducts = filteredProducts.filter(product => 
            product.brand === currentFilters.brand
        );
    }
    
    filteredProducts = filteredProducts.filter(product => 
        product.price >= currentFilters.priceMin && 
        product.price <= currentFilters.priceMax
    );
    
    if (currentFilters.inStockOnly) {
        filteredProducts = filteredProducts.filter(product => product.inStock);
    }
    
    filteredProducts = sortProductsArray(filteredProducts, currentFilters.sortBy);
    
    currentPage = 1;
    displayProducts(filteredProducts);
    showSection('products');
    toggleSearch();
}


// Enhanced cart functions with GBP
function updateCartItems() {
    const cartItems = document.getElementById('cart-items');
    const cartTotal = document.getElementById('cart-total');
    
    if (cart.length === 0) {
        cartItems.innerHTML = '<p>Your cart is empty</p>';
        cartTotal.textContent = '0.00';
        return;
    }
    
    let total = 0;
    cartItems.innerHTML = '';
    
    cart.forEach((item, index) => {
        total += item.price;
        const cartItem = document.createElement('div');
        cartItem.className = 'cart-item';
        cartItem.innerHTML = `
            <div style="display: flex; align-items: center; padding: 10px; border-bottom: 1px solid #eee;">
                <img src="${item.image}" alt="${item.name}" style="width: 60px; height: 60px; object-fit: cover; border-radius: 6px; margin-right: 10px;">
                <div style="flex: 1;">
                    <h4>${item.name}</h4>
                    <p>£${item.price}</p>
                </div>
                <button onclick="removeFromCart(${index})" style="background: #e74c3c; color: white; border: none; padding: 5px 10px; border-radius: 4px; cursor: pointer;">Remove</button>
            </div>
        `;
        cartItems.appendChild(cartItem);
    });
    
    cartTotal.textContent = total.toFixed(2);
}

// Authentication System
let currentUser = null;
let userOrders = [];
let userAddresses = [];
let userPreferences = {
    favoriteCategories: [],
    sizePreferences: {},
    notifications: true,
    newsletter: true
};

// Initialize auth on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeAuth();
    loadProducts();
    showSection('home');
});

function initializeAuth() {
    // Check if user is logged in (from localStorage)
    const savedUser = localStorage.getItem('manvue_user');
    const savedOrders = localStorage.getItem('manvue_orders');
    const savedAddresses = localStorage.getItem('manvue_addresses');
    const savedPreferences = localStorage.getItem('manvue_preferences');
    
    if (savedUser) {
        currentUser = JSON.parse(savedUser);
        userOrders = savedOrders ? JSON.parse(savedOrders) : [];
        userAddresses = savedAddresses ? JSON.parse(savedAddresses) : [];
        userPreferences = savedPreferences ? JSON.parse(savedPreferences) : userPreferences;
        updateAuthUI();
    } else {
        updateAuthUI();
    }
}

function updateAuthUI() {
    const userMenuContent = document.getElementById('user-menu-content');
    const userMenuTitle = document.getElementById('user-menu-title');
    
    if (currentUser) {
        // User is logged in
        userMenuTitle.textContent = `Hello, ${currentUser.name.split(' ')[0]}`;
        userMenuContent.innerHTML = `
            <div class="user-info">
                <div class="user-avatar-small">
                    <span>${getInitials(currentUser.name)}</span>
                </div>
                <div class="user-details">
                    <h4>${currentUser.name}</h4>
                    <p>${currentUser.email}</p>
                </div>
            </div>
            <div class="user-menu-actions">
                <button onclick="showProfile()">My Profile</button>
                <button onclick="showOrders()">My Orders</button>
                <button onclick="showAddresses()">My Addresses</button>
                <button onclick="showPreferences()">Preferences</button>
                <button onclick="logout()" class="logout-btn">Sign Out</button>
            </div>
        `;
    } else {
        // User is not logged in
        userMenuTitle.textContent = 'Account';
        userMenuContent.innerHTML = `
            <div class="guest-menu">
                <p>Sign in for a personalized experience</p>
                <button onclick="showLogin()" class="btn-primary">Sign In</button>
                <button onclick="showRegister()" class="btn-outline">Create Account</button>
            </div>
        `;
    }
}

function getInitials(name) {
    return name.split(' ').map(n => n[0]).join('').toUpperCase();
}

// Modal Management
function showModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = 'auto';
    }
}

// Authentication Functions
function showLogin() {
    toggleUserMenu();
    showModal('login-modal');
}

function showRegister() {
    toggleUserMenu();
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
    const rememberMe = document.getElementById('remember-me').checked;
    
    // Simulate login validation
    if (email && password) {
        // Check if user exists in localStorage
        const existingUsers = JSON.parse(localStorage.getItem('manvue_users') || '[]');
        const user = existingUsers.find(u => u.email === email && u.password === password);
        
        if (user) {
            // Login successful
            currentUser = user;
            localStorage.setItem('manvue_user', JSON.stringify(currentUser));
            
            if (rememberMe) {
                localStorage.setItem('manvue_remember', 'true');
            }
            
            closeModal('login-modal');
            updateAuthUI();
            showMessage('Welcome back! Successfully signed in.');
            
            // Clear form
            document.getElementById('login-form').reset();
        } else {
            showMessage('Invalid email or password. Please try again.');
        }
    }
}

function handleRegister(event) {
    event.preventDefault();
    
    const name = document.getElementById('register-name').value;
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;
    const confirmPassword = document.getElementById('register-confirm-password').value;
    const phone = document.getElementById('register-phone').value;
    const agreeTerms = document.getElementById('terms-agree').checked;
    
    // Validation
    if (password !== confirmPassword) {
        showMessage('Passwords do not match.');
        return;
    }
    
    if (!agreeTerms) {
        showMessage('Please agree to the Terms & Conditions.');
        return;
    }
    
    // Check if email already exists
    const existingUsers = JSON.parse(localStorage.getItem('manvue_users') || '[]');
    if (existingUsers.find(u => u.email === email)) {
        showMessage('An account with this email already exists.');
        return;
    }
    
    // Create new user
    const newUser = {
        id: Date.now(),
        name,
        email,
        password, // In real app, this would be hashed
        phone,
        joinDate: new Date().toISOString(),
        avatar: null
    };
    
    // Save user
    existingUsers.push(newUser);
    localStorage.setItem('manvue_users', JSON.stringify(existingUsers));
    
    // Auto-login
    currentUser = newUser;
    localStorage.setItem('manvue_user', JSON.stringify(currentUser));
    
    closeModal('register-modal');
    updateAuthUI();
    showMessage('Account created successfully! Welcome to MANVUE.');
    
    // Clear form
    document.getElementById('register-form').reset();
}

function handleForgotPassword(event) {
    event.preventDefault();
    
    const email = document.getElementById('forgot-email').value;
    
    // Simulate sending reset email
    showMessage('Password reset link sent to your email!');
    closeModal('forgot-password-modal');
    
    // Clear form
    document.getElementById('forgot-password-form').reset();
}

function logout() {
    currentUser = null;
    localStorage.removeItem('manvue_user');
    localStorage.removeItem('manvue_remember');
    
    updateAuthUI();
    toggleUserMenu();
    showMessage('Successfully signed out. See you again soon!');
    
    // Clear cart and wishlist for security
    cart = [];
    wishlist = [];
    updateCartDisplay();
}

// New section management
function showSection(sectionName) {
    // For now, just scroll to products and apply filters
    if (sectionName === 'trending' || sectionName === 'new-arrivals') {
        const productsSection = document.getElementById('products');
        productsSection.scrollIntoView({ behavior: 'smooth' });
    }
}

// Wishlist functionality
let wishlist = [];

function toggleWishlist() {
    const wishlistSidebar = document.getElementById('wishlist-sidebar');
    const overlay = document.getElementById('overlay');
    
    wishlistSidebar.classList.toggle('active');
    overlay.classList.toggle('active');
    
    if (wishlistSidebar.classList.contains('active')) {
        updateWishlistItems();
    }
}

function updateWishlistItems() {
    const wishlistItems = document.getElementById('wishlist-items');
    
    if (wishlist.length === 0) {
        wishlistItems.innerHTML = '<p>Your wishlist is empty</p>';
        return;
    }
    
    wishlistItems.innerHTML = '';
    
    wishlist.forEach((item, index) => {
        const wishlistItem = document.createElement('div');
        wishlistItem.className = 'wishlist-item';
        wishlistItem.innerHTML = `
            <div style="display: flex; align-items: center; padding: 10px; border-bottom: 1px solid #eee;">
                <img src="${item.image}" alt="${item.name}" style="width: 60px; height: 60px; object-fit: cover; border-radius: 6px; margin-right: 10px;">
                <div style="flex: 1;">
                    <h4>${item.name}</h4>
                    <p>£${item.price}</p>
                </div>
                <button onclick="removeFromWishlist(${index})" style="background: #e74c3c; color: white; border: none; padding: 5px 10px; border-radius: 4px; cursor: pointer;">Remove</button>
            </div>
        `;
        wishlistItems.appendChild(wishlistItem);
    });
}

function addToWishlist(productId) {
    const product = products.find(p => p.id === productId);
    if (product && !wishlist.find(item => item.id === productId)) {
        wishlist.push(product);
        showMessage(`${product.name} added to wishlist!`);
    }
}

function removeFromWishlist(index) {
    wishlist.splice(index, 1);
    updateWishlistItems();
}

// Deal functions
function showDeals() {
    // Filter products to show only discounted items
    const discountedProducts = products.filter(product => product.originalPrice > product.price);
    displayProducts(discountedProducts);
    const productsSection = document.getElementById('products');
    productsSection.scrollIntoView({ behavior: 'smooth' });
}

function showAllProducts() {
    currentPage = 1;
    loadProducts();
    const productsSection = document.getElementById('products');
    productsSection.scrollIntoView({ behavior: 'smooth' });
}

// Enhanced search with specific terms
function searchProducts(searchTerm = null) {
    const searchInput = document.getElementById('search-input');
    const actualSearchTerm = searchTerm || searchInput.value.toLowerCase();
    
    if (!actualSearchTerm) {
        applyAllFilters();
        return;
    }
    
    // Set the search input value if searchTerm was provided
    if (searchTerm) {
        searchInput.value = searchTerm;
    }
    
    let filteredProducts = products.filter(product => 
        product.name.toLowerCase().includes(actualSearchTerm) ||
        product.description.toLowerCase().includes(actualSearchTerm) ||
        product.category.toLowerCase().includes(actualSearchTerm) ||
        product.brand.toLowerCase().includes(actualSearchTerm) ||
        product.tags.some(tag => tag.toLowerCase().includes(actualSearchTerm))
    );
    
    // Apply other filters to search results
    if (currentFilters.category !== 'all') {
        filteredProducts = filteredProducts.filter(product => 
            product.category === currentFilters.category
        );
    }
    
    if (currentFilters.type) {
        filteredProducts = filteredProducts.filter(product => 
            product.type === currentFilters.type
        );
    }
    
    if (currentFilters.brand) {
        filteredProducts = filteredProducts.filter(product => 
            product.brand === currentFilters.brand
        );
    }
    
    filteredProducts = filteredProducts.filter(product => 
        product.price >= currentFilters.priceMin && 
        product.price <= currentFilters.priceMax
    );
    
    if (currentFilters.inStockOnly) {
        filteredProducts = filteredProducts.filter(product => product.inStock);
    }
    
    filteredProducts = sortProductsArray(filteredProducts, currentFilters.sortBy);
    
    currentPage = 1;
    displayProducts(filteredProducts);
    
    // Scroll to products section
    const productsSection = document.getElementById('products');
    productsSection.scrollIntoView({ behavior: 'smooth' });
    
    // Close search if it was from dropdown
    if (searchTerm) {
        toggleSearch();
    }
}

// Profile Management Functions
function showProfile() {
    if (!currentUser) {
        showLogin();
        return;
    }
    
    toggleUserMenu();
    showModal('profile-modal');
    showProfileTab('personal');
    
    // Update user initials in profile
    document.getElementById('user-initials').textContent = getInitials(currentUser.name);
}

function showProfileTab(tabName) {
    // Remove active class from all nav items
    const navItems = document.querySelectorAll('.profile-nav-item');
    navItems.forEach(item => item.classList.remove('active'));
    
    // Add active class to clicked nav item
    event.target.classList.add('active');
    
    const tabContent = document.getElementById('profile-tab-content');
    
    switch(tabName) {
        case 'personal':
            showPersonalInfoTab(tabContent);
            break;
        case 'preferences':
            showPreferencesTab(tabContent);
            break;
        case 'orders':
            showOrdersTab(tabContent);
            break;
        case 'addresses':
            showAddressesTab(tabContent);
            break;
        case 'security':
            showSecurityTab(tabContent);
            break;
    }
}

function showPersonalInfoTab(container) {
    container.innerHTML = `
        <div class="profile-section">
            <h4>Personal Information</h4>
            <form class="profile-form" onsubmit="updatePersonalInfo(event)">
                <div class="form-group">
                    <label for="profile-name">Full Name</label>
                    <input type="text" id="profile-name" value="${currentUser.name}" required>
                </div>
                <div class="form-group">
                    <label for="profile-email">Email</label>
                    <input type="email" id="profile-email" value="${currentUser.email}" required>
                </div>
                <div class="form-group">
                    <label for="profile-phone">Phone Number</label>
                    <input type="tel" id="profile-phone" value="${currentUser.phone || ''}" placeholder="Enter phone number">
                </div>
                <div class="form-group">
                    <label for="profile-dob">Date of Birth</label>
                    <input type="date" id="profile-dob" value="${currentUser.dateOfBirth || ''}">
                </div>
                <div class="form-group full-width">
                    <label for="profile-bio">Bio</label>
                    <textarea id="profile-bio" rows="3" placeholder="Tell us about yourself">${currentUser.bio || ''}</textarea>
                </div>
                <div class="form-group full-width">
                    <button type="submit" class="btn-primary">Update Information</button>
                </div>
            </form>
        </div>
        
        <div class="profile-section">
            <h4>Account Statistics</h4>
            <div class="profile-stats">
                <div class="stat-card">
                    <div class="stat-number">${userOrders.length}</div>
                    <div class="stat-label">Total Orders</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${wishlist.length}</div>
                    <div class="stat-label">Wishlist Items</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${userAddresses.length}</div>
                    <div class="stat-label">Saved Addresses</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${Math.floor((new Date() - new Date(currentUser.joinDate)) / (1000 * 60 * 60 * 24))}</div>
                    <div class="stat-label">Days with us</div>
                </div>
            </div>
        </div>
    `;
}

function showPreferencesTab(container) {
    container.innerHTML = `
        <div class="profile-section">
            <h4>Shopping Preferences</h4>
            <form class="profile-form" onsubmit="updatePreferences(event)">
                <div class="form-group">
                    <label for="favorite-categories">Favorite Categories</label>
                    <select id="favorite-categories" multiple>
                        <option value="tops">Tops</option>
                        <option value="bottoms">Bottoms</option>
                        <option value="shoes">Shoes</option>
                        <option value="outerwear">Outerwear</option>
                        <option value="accessories">Accessories</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="preferred-size-tops">Preferred Size - Tops</label>
                    <select id="preferred-size-tops">
                        <option value="">Select Size</option>
                        <option value="S">Small (S)</option>
                        <option value="M">Medium (M)</option>
                        <option value="L">Large (L)</option>
                        <option value="XL">Extra Large (XL)</option>
                        <option value="XXL">XXL</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="preferred-size-bottoms">Preferred Size - Bottoms</label>
                    <select id="preferred-size-bottoms">
                        <option value="">Select Size</option>
                        <option value="30">30</option>
                        <option value="32">32</option>
                        <option value="34">34</option>
                        <option value="36">36</option>
                        <option value="38">38</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="preferred-size-shoes">Preferred Size - Shoes</label>
                    <select id="preferred-size-shoes">
                        <option value="">Select Size</option>
                        <option value="7">7</option>
                        <option value="8">8</option>
                        <option value="9">9</option>
                        <option value="10">10</option>
                        <option value="11">11</option>
                        <option value="12">12</option>
                    </select>
                </div>
                <div class="form-group full-width">
                    <label class="checkbox-label">
                        <input type="checkbox" id="notifications" ${userPreferences.notifications ? 'checked' : ''}>
                        <span>Receive push notifications</span>
                    </label>
                </div>
                <div class="form-group full-width">
                    <label class="checkbox-label">
                        <input type="checkbox" id="newsletter" ${userPreferences.newsletter ? 'checked' : ''}>
                        <span>Subscribe to newsletter</span>
                    </label>
                </div>
                <div class="form-group full-width">
                    <button type="submit" class="btn-primary">Save Preferences</button>
                </div>
            </form>
        </div>
    `;
}

function showOrdersTab(container) {
    container.innerHTML = `
        <div class="profile-section">
            <h4>Order History</h4>
            ${userOrders.length > 0 ? 
                userOrders.map(order => `
                    <div class="order-item">
                        <div class="order-info">
                            <h5>Order #${order.id}</h5>
                            <p>Date: ${new Date(order.date).toLocaleDateString()}</p>
                            <p>Total: £${order.total}</p>
                        </div>
                        <div class="order-status ${order.status}">
                            ${order.status.charAt(0).toUpperCase() + order.status.slice(1)}
                        </div>
                    </div>
                `).join('') : 
                '<p>No orders yet. <a href="#" onclick="closeModal(\'profile-modal\'); showAllProducts();">Start shopping!</a></p>'
            }
        </div>
    `;
}

function showAddressesTab(container) {
    container.innerHTML = `
        <div class="profile-section">
            <h4>Saved Addresses</h4>
            <button class="btn-outline" onclick="addNewAddress()">Add New Address</button>
            ${userAddresses.length > 0 ? 
                userAddresses.map((address, index) => `
                    <div class="address-card">
                        ${address.isDefault ? '<div class="default-badge">Default</div>' : ''}
                        <h5>${address.type}</h5>
                        <p>${address.street}</p>
                        <p>${address.city}, ${address.postcode}</p>
                        <p>${address.country}</p>
                        <div class="address-actions">
                            <button class="btn-outline btn-small" onclick="editAddress(${index})">Edit</button>
                            <button class="btn-outline btn-small" onclick="deleteAddress(${index})">Delete</button>
                            ${!address.isDefault ? `<button class="btn-outline btn-small" onclick="setDefaultAddress(${index})">Set Default</button>` : ''}
                        </div>
                    </div>
                `).join('') : 
                '<p>No saved addresses yet.</p>'
            }
        </div>
    `;
}

function showSecurityTab(container) {
    container.innerHTML = `
        <div class="profile-section">
            <h4>Change Password</h4>
            <form class="profile-form" onsubmit="changePassword(event)">
                <div class="form-group full-width">
                    <label for="current-password">Current Password</label>
                    <input type="password" id="current-password" required>
                </div>
                <div class="form-group">
                    <label for="new-password">New Password</label>
                    <input type="password" id="new-password" required minlength="6">
                </div>
                <div class="form-group">
                    <label for="confirm-new-password">Confirm New Password</label>
                    <input type="password" id="confirm-new-password" required>
                </div>
                <div class="form-group full-width">
                    <button type="submit" class="btn-primary">Change Password</button>
                </div>
            </form>
        </div>
        
        <div class="profile-section">
            <h4>Account Actions</h4>
            <button class="btn-outline" onclick="downloadData()">Download My Data</button>
            <button class="btn-outline" onclick="deleteAccount()" style="color: #e74c3c; border-color: #e74c3c;">Delete Account</button>
        </div>
    `;
}

// Profile update functions
function updatePersonalInfo(event) {
    event.preventDefault();
    
    const name = document.getElementById('profile-name').value;
    const email = document.getElementById('profile-email').value;
    const phone = document.getElementById('profile-phone').value;
    const dob = document.getElementById('profile-dob').value;
    const bio = document.getElementById('profile-bio').value;
    
    // Update current user
    currentUser.name = name;
    currentUser.email = email;
    currentUser.phone = phone;
    currentUser.dateOfBirth = dob;
    currentUser.bio = bio;
    
    // Update in localStorage
    localStorage.setItem('manvue_user', JSON.stringify(currentUser));
    
    // Update users array
    const existingUsers = JSON.parse(localStorage.getItem('manvue_users') || '[]');
    const userIndex = existingUsers.findIndex(u => u.id === currentUser.id);
    if (userIndex !== -1) {
        existingUsers[userIndex] = currentUser;
        localStorage.setItem('manvue_users', JSON.stringify(existingUsers));
    }
    
    updateAuthUI();
    showMessage('Personal information updated successfully!');
}

function updatePreferences(event) {
    event.preventDefault();
    
    const favoriteCategories = Array.from(document.getElementById('favorite-categories').selectedOptions).map(option => option.value);
    const notifications = document.getElementById('notifications').checked;
    const newsletter = document.getElementById('newsletter').checked;
    
    userPreferences = {
        favoriteCategories,
        sizePreferences: {
            tops: document.getElementById('preferred-size-tops').value,
            bottoms: document.getElementById('preferred-size-bottoms').value,
            shoes: document.getElementById('preferred-size-shoes').value
        },
        notifications,
        newsletter
    };
    
    localStorage.setItem('manvue_preferences', JSON.stringify(userPreferences));
    showMessage('Preferences saved successfully!');
}

function changePassword(event) {
    event.preventDefault();
    
    const currentPassword = document.getElementById('current-password').value;
    const newPassword = document.getElementById('new-password').value;
    const confirmPassword = document.getElementById('confirm-new-password').value;
    
    if (currentPassword !== currentUser.password) {
        showMessage('Current password is incorrect.');
        return;
    }
    
    if (newPassword !== confirmPassword) {
        showMessage('New passwords do not match.');
        return;
    }
    
    // Update password
    currentUser.password = newPassword;
    localStorage.setItem('manvue_user', JSON.stringify(currentUser));
    
    // Update users array
    const existingUsers = JSON.parse(localStorage.getItem('manvue_users') || '[]');
    const userIndex = existingUsers.findIndex(u => u.id === currentUser.id);
    if (userIndex !== -1) {
        existingUsers[userIndex] = currentUser;
        localStorage.setItem('manvue_users', JSON.stringify(existingUsers));
    }
    
    showMessage('Password changed successfully!');
    
    // Clear form
    document.getElementById('current-password').value = '';
    document.getElementById('new-password').value = '';
    document.getElementById('confirm-new-password').value = '';
}

function showOrders() {
    showProfile();
    // Wait for modal to open, then switch to orders tab
    setTimeout(() => {
        showProfileTab('orders');
        document.querySelector('.profile-nav-item[onclick="showProfileTab(\'orders\')"]').classList.add('active');
    }, 100);
}

function showAddresses() {
    showProfile();
    setTimeout(() => {
        showProfileTab('addresses');
        document.querySelector('.profile-nav-item[onclick="showProfileTab(\'addresses\')"]').classList.add('active');
    }, 100);
}

function showPreferences() {
    showProfile();
    setTimeout(() => {
        showProfileTab('preferences');
        document.querySelector('.profile-nav-item[onclick="showProfileTab(\'preferences\')"]').classList.add('active');
    }, 100);
}

// Style Recommendation System
let userStyleProfile = {
    styleType: '',
    bodyType: '',
    colorPreferences: [],
    occasions: [],
    budget: '',
    lifestyle: '',
    personalityTraits: [],
    fashionGoals: [],
    preferredBrands: [],
    avoidColors: []
};

let currentQuizQuestion = 0;
let quizAnswers = [];

const styleQuizQuestions = [
    {
        id: 1,
        question: "What's your primary style goal?",
        type: "single",
        options: [
            { value: "confidence", title: "Build Confidence", icon: "💪", desc: "Look and feel more confident" },
            { value: "professional", title: "Professional Image", icon: "👔", desc: "Elevate your work wardrobe" },
            { value: "trendy", title: "Stay Trendy", icon: "✨", desc: "Keep up with latest fashion" },
            { value: "comfort", title: "Comfort First", icon: "😌", desc: "Prioritize comfort and ease" }
        ]
    },
    {
        id: 2,
        question: "Which style personality resonates with you most?",
        type: "single",
        options: [
            { value: "classic", title: "Classic Gentleman", icon: "🎩", desc: "Timeless, refined, traditional" },
            { value: "modern", title: "Modern Minimalist", icon: "⚡", desc: "Clean lines, contemporary" },
            { value: "casual", title: "Casual Cool", icon: "😎", desc: "Relaxed, effortless style" },
            { value: "bold", title: "Bold & Creative", icon: "🎨", desc: "Statement pieces, unique looks" }
        ]
    },
    {
        id: 3,
        question: "What's your typical daily routine?",
        type: "single",
        options: [
            { value: "office", title: "Office Worker", icon: "💼", desc: "Business/smart casual required" },
            { value: "remote", title: "Remote Worker", icon: "🏠", desc: "Flexible, comfortable clothing" },
            { value: "active", title: "Active Lifestyle", icon: "🏃", desc: "Lots of movement, sporty needs" },
            { value: "social", title: "Social & Events", icon: "🎉", desc: "Frequent social gatherings" }
        ]
    },
    {
        id: 4,
        question: "What's your budget range for a complete outfit?",
        type: "single",
        options: [
            { value: "budget", title: "Budget-Friendly", icon: "💰", desc: "£50-100 per outfit" },
            { value: "moderate", title: "Moderate Spend", icon: "💳", desc: "£100-200 per outfit" },
            { value: "premium", title: "Premium Quality", icon: "💎", desc: "£200-400 per outfit" },
            { value: "luxury", title: "Luxury Investment", icon: "👑", desc: "£400+ per outfit" }
        ]
    },
    {
        id: 5,
        question: "Which colors make you feel most confident?",
        type: "multiple",
        options: [
            { value: "navy", title: "Navy Blue", icon: "🔵", desc: "Professional and versatile" },
            { value: "black", title: "Black", icon: "⚫", desc: "Sleek and sophisticated" },
            { value: "grey", title: "Grey", icon: "⚪", desc: "Neutral and adaptable" },
            { value: "white", title: "White", icon: "⚪", desc: "Clean and fresh" },
            { value: "earth", title: "Earth Tones", icon: "🟤", desc: "Warm and natural" },
            { value: "bold", title: "Bold Colors", icon: "🌈", desc: "Vibrant and expressive" }
        ]
    },
    {
        id: 6,
        question: "What occasions do you dress for most often?",
        type: "multiple",
        options: [
            { value: "work", title: "Work/Business", icon: "👔", desc: "Professional meetings" },
            { value: "casual", title: "Everyday Casual", icon: "👕", desc: "Daily activities" },
            { value: "social", title: "Social Events", icon: "🍷", desc: "Dinners, parties" },
            { value: "date", title: "Date Nights", icon: "💝", desc: "Romantic occasions" },
            { value: "travel", title: "Travel", icon: "✈️", desc: "Comfortable travel wear" },
            { value: "fitness", title: "Fitness/Sports", icon: "🏋️", desc: "Active wear needs" }
        ]
    },
    {
        id: 7,
        question: "How would you describe your body type?",
        type: "single",
        options: [
            { value: "athletic", title: "Athletic Build", icon: "💪", desc: "Broad shoulders, defined muscles" },
            { value: "slim", title: "Slim/Lean", icon: "📏", desc: "Narrow frame, tall appearance" },
            { value: "average", title: "Average Build", icon: "👤", desc: "Balanced proportions" },
            { value: "larger", title: "Larger Frame", icon: "🤗", desc: "Broader build, comfort focus" }
        ]
    },
    {
        id: 8,
        question: "Which personality traits best describe you?",
        type: "multiple",
        options: [
            { value: "confident", title: "Confident", icon: "🦁", desc: "Self-assured and bold" },
            { value: "creative", title: "Creative", icon: "🎨", desc: "Artistic and expressive" },
            { value: "practical", title: "Practical", icon: "🔧", desc: "Function over form" },
            { value: "adventurous", title: "Adventurous", icon: "🌍", desc: "Loves trying new things" },
            { value: "traditional", title: "Traditional", icon: "📚", desc: "Values classic approaches" },
            { value: "trendsetter", title: "Trendsetter", icon: "🚀", desc: "Likes to lead fashion" }
        ]
    },
    {
        id: 9,
        question: "What are your main fashion challenges?",
        type: "multiple",
        options: [
            { value: "matching", title: "Color Coordination", icon: "🎨", desc: "Struggle with color matching" },
            { value: "fit", title: "Finding Right Fit", icon: "📐", desc: "Clothes don't fit well" },
            { value: "occasions", title: "Occasion Dressing", icon: "🎭", desc: "Don't know what to wear when" },
            { value: "trends", title: "Keeping Up with Trends", icon: "📈", desc: "Fashion moves too fast" },
            { value: "budget", title: "Budget Constraints", icon: "💸", desc: "Want style within budget" },
            { value: "confidence", title: "Lack of Confidence", icon: "😰", desc: "Unsure about style choices" }
        ]
    },
    {
        id: 10,
        question: "What's your ultimate style aspiration?",
        type: "single",
        options: [
            { value: "effortless", title: "Effortless Elegance", icon: "✨", desc: "Look great without trying hard" },
            { value: "standout", title: "Stand Out", icon: "🌟", desc: "Be memorable and unique" },
            { value: "respected", title: "Professional Respect", icon: "🎯", desc: "Command respect through style" },
            { value: "authentic", title: "Authentic Self", icon: "🤝", desc: "Express true personality" }
        ]
    }
];

// Style Recommendation Engine
const styleProfiles = {
    classic: {
        name: "Classic Gentleman",
        description: "Timeless elegance with refined taste",
        tags: ["Sophisticated", "Traditional", "Refined", "Elegant"],
        colors: ["navy", "grey", "white", "black", "burgundy"],
        patterns: ["solid", "subtle stripes", "classic checks"],
        keyPieces: ["blazer", "dress shirt", "chinos", "leather shoes"],
        avoidance: ["loud patterns", "neon colors", "oversized fits"]
    },
    modern: {
        name: "Modern Minimalist",
        description: "Clean lines and contemporary sophistication",
        tags: ["Contemporary", "Minimalist", "Sleek", "Urban"],
        colors: ["black", "white", "grey", "navy", "olive"],
        patterns: ["solid", "geometric", "minimal stripes"],
        keyPieces: ["slim fit shirts", "tailored pants", "modern sneakers", "structured jackets"],
        avoidance: ["busy patterns", "vintage styles", "bulky accessories"]
    },
    casual: {
        name: "Casual Cool",
        description: "Relaxed confidence with effortless style",
        tags: ["Relaxed", "Comfortable", "Versatile", "Easy-going"],
        colors: ["denim", "earth tones", "pastels", "neutrals"],
        patterns: ["casual stripes", "simple graphics", "solid colors"],
        keyPieces: ["jeans", "polo shirts", "sneakers", "casual jackets"],
        avoidance: ["overly formal", "restrictive fits", "high maintenance"]
    },
    bold: {
        name: "Bold & Creative",
        description: "Statement-making with artistic flair",
        tags: ["Creative", "Expressive", "Unique", "Artistic"],
        colors: ["bold colors", "rich jewel tones", "contrasting combinations"],
        patterns: ["bold prints", "artistic designs", "mixed patterns"],
        keyPieces: ["statement jackets", "unique accessories", "designer pieces", "artistic prints"],
        avoidance: ["bland basics", "safe choices", "cookie-cutter looks"]
    }
};

// AI-Powered Outfit Generation
const outfitTemplates = {
    business: {
        warm: ["dress shirt", "chinos", "blazer", "leather shoes", "belt"],
        mild: ["dress shirt", "suit trousers", "blazer", "dress shoes", "tie"],
        cool: ["dress shirt", "wool trousers", "suit jacket", "leather shoes", "overcoat"],
        cold: ["thermal shirt", "wool suit", "heavy coat", "leather boots", "scarf"]
    },
    casual: {
        warm: ["t-shirt", "shorts", "sneakers", "cap"],
        mild: ["polo shirt", "jeans", "casual shoes", "light jacket"],
        cool: ["sweater", "jeans", "boots", "jacket"],
        cold: ["hoodie", "thermal layers", "winter coat", "warm boots"]
    },
    formal: {
        warm: ["dress shirt", "suit trousers", "vest", "dress shoes", "bow tie"],
        mild: ["dress shirt", "formal suit", "dress shoes", "cufflinks", "pocket square"],
        cool: ["dress shirt", "three-piece suit", "formal shoes", "overcoat", "gloves"],
        cold: ["thermal layers", "formal suit", "heavy coat", "formal boots", "wool scarf"]
    },
    date: {
        warm: ["button-down shirt", "dark jeans", "loafers", "watch"],
        mild: ["casual blazer", "chinos", "dress shoes", "nice belt"],
        cool: ["sweater", "dark jeans", "boots", "leather jacket"],
        cold: ["wool sweater", "dress pants", "coat", "dress boots"]
    }
};

// Style Quiz Functions
function startStyleQuiz() {
    currentQuizQuestion = 0;
    quizAnswers = [];
    showModal('style-quiz-modal');
    displayQuizQuestion();
}

function displayQuizQuestion() {
    const question = styleQuizQuestions[currentQuizQuestion];
    const questionsContainer = document.getElementById('quiz-questions');
    const progressFill = document.getElementById('quiz-progress-fill');
    const progressText = document.getElementById('quiz-progress-text');
    
    // Update progress
    const progress = ((currentQuizQuestion + 1) / styleQuizQuestions.length) * 100;
    progressFill.style.width = `${progress}%`;
    progressText.textContent = `Question ${currentQuizQuestion + 1} of ${styleQuizQuestions.length}`;
    
    // Create question HTML
    const optionsHTML = question.options.map(option => `
        <div class="quiz-option" onclick="selectQuizOption('${option.value}', ${question.type === 'multiple'})">
            <div class="quiz-option-icon">${option.icon}</div>
            <div class="quiz-option-title">${option.title}</div>
            <div class="quiz-option-desc">${option.desc}</div>
        </div>
    `).join('');
    
    questionsContainer.innerHTML = `
        <div class="quiz-question">
            <h4>${question.question}</h4>
            ${question.type === 'multiple' ? '<p style="color: #666; margin-bottom: 20px;">Select all that apply</p>' : ''}
            <div class="quiz-options">
                ${optionsHTML}
            </div>
        </div>
    `;
    
    // Update navigation buttons
    document.getElementById('quiz-prev').disabled = currentQuizQuestion === 0;
    document.getElementById('quiz-next').textContent = currentQuizQuestion === styleQuizQuestions.length - 1 ? 'Get My Style Profile' : 'Next';
}

function selectQuizOption(value, isMultiple) {
    const option = event.target.closest('.quiz-option');
    
    if (isMultiple) {
        // Multiple selection
        option.classList.toggle('selected');
        if (!quizAnswers[currentQuizQuestion]) {
            quizAnswers[currentQuizQuestion] = [];
        }
        const answers = quizAnswers[currentQuizQuestion];
        if (answers.includes(value)) {
            quizAnswers[currentQuizQuestion] = answers.filter(v => v !== value);
        } else {
            answers.push(value);
        }
    } else {
        // Single selection
        document.querySelectorAll('.quiz-option').forEach(opt => opt.classList.remove('selected'));
        option.classList.add('selected');
        quizAnswers[currentQuizQuestion] = value;
    }
}

function nextQuestion() {
    if (currentQuizQuestion === styleQuizQuestions.length - 1) {
        // Quiz complete - generate recommendations
        generateStyleProfile();
    } else {
        currentQuizQuestion++;
        displayQuizQuestion();
    }
}

function previousQuestion() {
    if (currentQuizQuestion > 0) {
        currentQuizQuestion--;
        displayQuizQuestion();
    }
}

function generateStyleProfile() {
    // Process quiz answers to determine style profile
    const answers = quizAnswers;
    
    // Determine primary style type based on answers
    let styleScores = { classic: 0, modern: 0, casual: 0, bold: 0 };
    
    // Question 2 directly influences style type
    if (answers[1] === 'classic') styleScores.classic += 3;
    if (answers[1] === 'modern') styleScores.modern += 3;
    if (answers[1] === 'casual') styleScores.casual += 3;
    if (answers[1] === 'bold') styleScores.bold += 3;
    
    // Budget influences style (Question 4)
    if (answers[3] === 'luxury') styleScores.classic += 2;
    if (answers[3] === 'premium') styleScores.modern += 2;
    if (answers[3] === 'budget') styleScores.casual += 2;
    
    // Personality traits influence style (Question 8)
    if (answers[7] && answers[7].includes('traditional')) styleScores.classic += 2;
    if (answers[7] && answers[7].includes('creative')) styleScores.bold += 2;
    if (answers[7] && answers[7].includes('practical')) styleScores.casual += 2;
    if (answers[7] && answers[7].includes('trendsetter')) styleScores.modern += 2;
    
    // Determine primary style
    const primaryStyle = Object.keys(styleScores).reduce((a, b) => styleScores[a] > styleScores[b] ? a : b);
    
    // Build user style profile
    userStyleProfile = {
        styleType: primaryStyle,
        goal: answers[0],
        lifestyle: answers[2],
        budget: answers[3],
        colorPreferences: answers[4] || [],
        occasions: answers[5] || [],
        bodyType: answers[6],
        personalityTraits: answers[7] || [],
        challenges: answers[8] || [],
        aspiration: answers[9]
    };
    
    // Save to localStorage
    localStorage.setItem('manvue_style_profile', JSON.stringify(userStyleProfile));
    
    // Close quiz and show recommendations
    closeModal('style-quiz-modal');
    showStyleRecommendations();
}

function showStyleRecommendations() {
    const profile = styleProfiles[userStyleProfile.styleType];
    const profileSummary = document.getElementById('style-profile-summary');
    const outfitsContainer = document.getElementById('recommended-outfits');
    const productsContainer = document.getElementById('recommended-products');
    
    // Display style profile
    profileSummary.innerHTML = `
        <div class="style-profile-card">
            <h4>${profile.name}</h4>
            <p>${profile.description}</p>
            <div class="style-tags">
                ${profile.tags.map(tag => `<span class="style-tag">${tag}</span>`).join('')}
            </div>
        </div>
    `;
    
    // Generate outfit recommendations
    const outfits = generateOutfitRecommendations();
    outfitsContainer.innerHTML = `
        <h3>Recommended Outfits</h3>
        <div class="outfit-grid">
            ${outfits.map(outfit => `
                <div class="outfit-card">
                    <div class="outfit-header">
                        <div class="outfit-occasion">${outfit.occasion}</div>
                        <div class="outfit-title">${outfit.title}</div>
                    </div>
                    <div class="outfit-items">
                        ${outfit.items.map(item => `
                            <div class="outfit-item">
                                <img src="${item.image}" alt="${item.name}" class="item-image">
                                <div class="item-details">
                                    <h5>${item.name}</h5>
                                    <p>£${item.price}</p>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `).join('')}
        </div>
    `;
    
    // Generate product recommendations
    const recommendedProducts = getRecommendedProducts();
    productsContainer.innerHTML = `
        <h3>Recommended Products</h3>
        <div class="product-grid">
            ${recommendedProducts.map(product => `
                <div class="product-card" onclick="quickView(${product.id})">
                    <div class="product-image">
                        <img src="${product.image}" alt="${product.name}">
                    </div>
                    <div class="product-info">
                        <div class="product-brand">${product.brand}</div>
                        <div class="product-title">${product.name}</div>
                        <div class="product-price">
                            <span class="current-price">£${product.price}</span>
                        </div>
                        <div class="product-actions">
                            <button class="add-to-cart" onclick="addToCart(${product.id}); event.stopPropagation();">Add to Cart</button>
                        </div>
                    </div>
                </div>
            `).join('')}
        </div>
    `;
    
    showModal('recommendations-modal');
}

function generateOutfitRecommendations() {
    const occasions = userStyleProfile.occasions;
    const outfits = [];
    
    // Generate outfits for user's preferred occasions
    occasions.forEach(occasion => {
        const template = outfitTemplates[occasion] || outfitTemplates.casual;
        const weather = 'mild'; // Default weather
        const items = template[weather];
        
        // Find matching products from our inventory
        const outfitItems = items.map(itemType => {
            const matchingProduct = products.find(p => 
                p.tags.some(tag => tag.includes(itemType.replace(' ', ''))) ||
                p.name.toLowerCase().includes(itemType)
            );
            return matchingProduct ? {
                name: matchingProduct.name,
                price: matchingProduct.price,
                image: matchingProduct.image
            } : {
                name: itemType.charAt(0).toUpperCase() + itemType.slice(1),
                price: 'TBD',
                image: 'https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=200&h=200&fit=crop'
            };
        });
        
        outfits.push({
            occasion: occasion.charAt(0).toUpperCase() + occasion.slice(1),
            title: `Perfect ${occasion} Look`,
            items: outfitItems.slice(0, 4) // Limit to 4 items per outfit
        });
    });
    
    return outfits.slice(0, 3); // Return top 3 outfits
}

function getRecommendedProducts() {
    const profile = styleProfiles[userStyleProfile.styleType];
    const userColors = userStyleProfile.colorPreferences;
    
    // Filter products based on style profile
    return products.filter(product => {
        // Check if product matches style preferences
        const matchesStyle = profile.keyPieces.some(piece => 
            product.name.toLowerCase().includes(piece) ||
            product.tags.some(tag => tag.includes(piece.replace(' ', '')))
        );
        
        // Check if product matches color preferences
        const matchesColor = userColors.length === 0 || userColors.some(color =>
            product.tags.some(tag => tag.includes(color)) ||
            product.name.toLowerCase().includes(color)
        );
        
        return matchesStyle || matchesColor;
    }).slice(0, 6); // Return top 6 recommendations
}

// Outfit Builder Functions
function showOutfitBuilder() {
    showModal('outfit-builder-modal');
    updateOutfitRecommendations();
}

function updateOutfitRecommendations() {
    const occasion = document.getElementById('occasion-select').value;
    const weather = document.getElementById('weather-select').value;
    const styleMood = document.getElementById('style-mood').value;
    
    const suggestions = generateAIOutfitSuggestions(occasion, weather, styleMood);
    const suggestionsContainer = document.getElementById('outfit-suggestions');
    
    suggestionsContainer.innerHTML = suggestions.map(suggestion => `
        <div class="suggestion-card">
            <div class="suggestion-header">
                <div class="suggestion-title">${suggestion.title}</div>
                <div class="confidence-score">${suggestion.confidence}% Match</div>
            </div>
            <div class="suggestion-description">${suggestion.description}</div>
            <div class="suggestion-products">
                ${suggestion.products.map(product => `
                    <div class="suggestion-product" onclick="quickView(${product.id})">
                        <img src="${product.image}" alt="${product.name}">
                        <h6>${product.name}</h6>
                        <p>£${product.price}</p>
                    </div>
                `).join('')}
            </div>
        </div>
    `).join('');
}

function generateAIOutfitSuggestions(occasion, weather, styleMood) {
    const suggestions = [];
    const template = outfitTemplates[occasion] || outfitTemplates.casual;
    const weatherItems = template[weather] || template.mild;
    
    // Generate 3 different outfit suggestions
    for (let i = 0; i < 3; i++) {
        const confidence = Math.floor(Math.random() * 20) + 80; // 80-100% confidence
        const outfitProducts = [];
        
        // Select products for this outfit
        weatherItems.forEach(itemType => {
            const matchingProducts = products.filter(p => 
                p.tags.some(tag => tag.includes(itemType.replace(' ', ''))) ||
                p.name.toLowerCase().includes(itemType)
            );
            
            if (matchingProducts.length > 0) {
                const randomProduct = matchingProducts[Math.floor(Math.random() * matchingProducts.length)];
                outfitProducts.push(randomProduct);
            }
        });
        
        suggestions.push({
            title: `${styleMood.charAt(0).toUpperCase() + styleMood.slice(1)} ${occasion.charAt(0).toUpperCase() + occasion.slice(1)} Look ${i + 1}`,
            confidence,
            description: generateOutfitDescription(occasion, weather, styleMood),
            products: outfitProducts.slice(0, 4)
        });
    }
    
    return suggestions;
}

function generateOutfitDescription(occasion, weather, styleMood) {
    const descriptions = {
        business: {
            classic: "A timeless professional look that commands respect in any boardroom.",
            trendy: "Modern business attire with contemporary touches for the style-conscious professional.",
            minimalist: "Clean, sophisticated lines that let your work speak for itself.",
            bold: "Professional with personality - stand out while staying appropriate."
        },
        casual: {
            classic: "Effortlessly refined casual wear that never goes out of style.",
            trendy: "Current casual trends that keep you looking fresh and modern.",
            minimalist: "Simple, comfortable pieces that create a cohesive, understated look.",
            bold: "Casual wear with creative flair that expresses your unique personality."
        },
        formal: {
            classic: "Traditional formal elegance perfect for special occasions.",
            trendy: "Contemporary formal wear with modern styling and current details.",
            minimalist: "Sleek, sophisticated formal attire with clean, uncluttered lines.",
            bold: "Formal wear that makes a statement while respecting the dress code."
        }
    };
    
    return descriptions[occasion]?.[styleMood] || "A carefully curated outfit that perfectly matches your style preferences and the occasion.";
}

// Enhanced Chat Functions
function sendChatMessage() {
    const chatInput = document.getElementById('chat-input');
    const message = chatInput.value.trim();
    
    if (!message) return;
    
    // Add user message
    addChatMessage(message, 'user');
    chatInput.value = '';
    
    // Generate AI response
    setTimeout(() => {
        const response = generateStyleAdvice(message);
        addChatMessage(response, 'bot');
    }, 1000);
}

function addChatMessage(message, sender) {
    const chatMessages = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `${sender}-message`;
    messageDiv.innerHTML = message;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function generateStyleAdvice(userMessage) {
    const message = userMessage.toLowerCase();
    
    // Style advice based on keywords
    if (message.includes('color') || message.includes('colour')) {
        return `🎨 <strong>Color Coordination Tips:</strong><br>
        • Navy and grey are versatile base colors that work with almost everything<br>
        • Follow the 60-30-10 rule: 60% neutral, 30% secondary color, 10% accent<br>
        • Earth tones (brown, beige, olive) work great together<br>
        • When in doubt, stick to monochrome or analogous colors<br>
        <span class="recommendation-chip" onclick="startStyleQuiz()">Take Style Quiz</span>`;
    }
    
    if (message.includes('occasion') || message.includes('event')) {
        return `🎭 <strong>Occasion Dressing Guide:</strong><br>
        • Business: Dark suit, crisp shirt, conservative tie<br>
        • Casual: Chinos/jeans with polo/button-down<br>
        • Date night: Smart casual with one standout piece<br>
        • Formal: Black/navy suit, white shirt, silk tie<br>
        <span class="recommendation-chip" onclick="showOutfitBuilder()">Build an Outfit</span>`;
    }
    
    if (message.includes('trend') || message.includes('fashion')) {
        return `🔥 <strong>Current Men's Fashion Trends:</strong><br>
        • Oversized blazers with tapered trousers<br>
        • Earth tone color palettes<br>
        • Textured fabrics and knits<br>
        • Minimalist accessories<br>
        • Sustainable and ethical fashion choices<br>
        <span class="recommendation-chip" onclick="getTrendingStyles()">See Trending Items</span>`;
    }
    
    if (message.includes('fit') || message.includes('size')) {
        return `📐 <strong>Perfect Fit Guidelines:</strong><br>
        • Shoulders should lie flat, not bunch or hang<br>
        • Sleeves should end at your wrist bone<br>
        • Pants should have minimal break at the ankle<br>
        • Shirts should allow for comfortable movement<br>
        • When in doubt, get it tailored!<br>
        <span class="recommendation-chip" onclick="showProfile()">Update Size Preferences</span>`;
    }
    
    if (message.includes('visual') || message.includes('image') || message.includes('photo')) {
        return `📸 <strong>Visual Search & Image Recognition:</strong><br>
        • Upload any fashion image to find similar products<br>
        • Use your camera to capture and analyze outfits<br>
        • AI-powered color and style detection<br>
        • Get instant product recommendations<br>
        <span class="recommendation-chip" onclick="startImageSearch()">📸 Start Visual Search</span>`;
    }
    
    // Default response with personalized touch
    return `Thanks for your question! 👔 Here are some general style tips:<br>
    • Invest in quality basics: white shirts, dark jeans, navy blazer<br>
    • Fit is more important than brand or price<br>
    • Build a capsule wardrobe with versatile pieces<br>
    • Confidence is your best accessory!<br><br>
    For personalized recommendations, try our features:<br>
    <span class="recommendation-chip" onclick="startStyleQuiz()">Discover Your Style</span>
    <span class="recommendation-chip" onclick="startImageSearch()">📸 Visual Search</span>`;
}

function getTrendingStyles() {
    const trendingMessage = `
        <div class="style-tip">
            <span class="style-tip-icon">🔥</span>
            <strong>Trending Now at MANVUE:</strong><br>
            • Earth tone casual wear<br>
            • Textured knitwear<br>
            • Minimalist accessories<br>
            • Sustainable fabrics<br>
        </div>
        Check out our trending products section!
        <span class="recommendation-chip" onclick="searchProducts('trending')">Shop Trends</span>
    `;
    addChatMessage(trendingMessage, 'bot');
}

// Image Recognition System
let currentImageData = null;
let cameraStream = null;
let analysisResults = null;

// AI-powered product categorization database
const productCategories = {
    'shirt': { category: 'tops', type: 'tops', confidence_boost: 0.15 },
    't-shirt': { category: 'tops', type: 'tops', confidence_boost: 0.15 },
    'polo': { category: 'tops', type: 'tops', confidence_boost: 0.12 },
    'sweater': { category: 'tops', type: 'tops', confidence_boost: 0.12 },
    'jacket': { category: 'outerwear', type: 'outerwear', confidence_boost: 0.18 },
    'blazer': { category: 'outerwear', type: 'outerwear', confidence_boost: 0.15 },
    'jeans': { category: 'bottoms', type: 'bottoms', confidence_boost: 0.16 },
    'pants': { category: 'bottoms', type: 'bottoms', confidence_boost: 0.14 },
    'shorts': { category: 'bottoms', type: 'bottoms', confidence_boost: 0.13 },
    'shoes': { category: 'shoes', type: 'shoes', confidence_boost: 0.20 },
    'sneakers': { category: 'shoes', type: 'shoes', confidence_boost: 0.18 },
    'boots': { category: 'shoes', type: 'shoes', confidence_boost: 0.17 },
    'watch': { category: 'accessories', type: 'accessories', confidence_boost: 0.12 },
    'belt': { category: 'accessories', type: 'accessories', confidence_boost: 0.10 }
};

// Color analysis database
const colorPalette = {
    '#000000': 'black',
    '#FFFFFF': 'white',
    '#808080': 'grey',
    '#000080': 'navy',
    '#0000FF': 'blue',
    '#FF0000': 'red',
    '#008000': 'green',
    '#FFFF00': 'yellow',
    '#FFA500': 'orange',
    '#800080': 'purple',
    '#FFC0CB': 'pink',
    '#A52A2A': 'brown',
    '#F5F5DC': 'beige'
};

// Visual Search Functions
function startImageSearch() {
    showModal('visual-search-modal');
    switchUploadMethod('camera');
}

function switchUploadMethod(method) {
    // Remove active class from all methods
    document.querySelectorAll('.upload-method').forEach(m => m.classList.remove('active'));
    document.querySelectorAll('.upload-content').forEach(c => c.classList.remove('active'));
    
    // Add active class to selected method
    document.querySelector(`.upload-method[onclick="switchUploadMethod('${method}')"]`).classList.add('active');
    document.getElementById(`${method}-section`).classList.add('active');
    
    // Clear previous content
    clearImagePreview();
}

function triggerFileInput() {
    document.getElementById('image-file-input').click();
}

function handleImageUpload(event) {
    const file = event.target.files[0];
    if (file && file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = function(e) {
            displayImagePreview(e.target.result);
        };
        reader.readAsDataURL(file);
    }
}

function loadImageFromURL() {
    const url = document.getElementById('image-url-input').value.trim();
    if (url) {
        displayImagePreview(url);
    } else {
        showMessage('Please enter a valid image URL');
    }
}

function displayImagePreview(imageSrc) {
    currentImageData = imageSrc;
    const previewSection = document.getElementById('image-preview-section');
    const previewImage = document.getElementById('preview-image');
    
    previewImage.src = imageSrc;
    previewSection.style.display = 'block';
    
    // Hide analysis results if showing
    document.getElementById('analysis-results').style.display = 'none';
}

function clearImagePreview() {
    currentImageData = null;
    document.getElementById('image-preview-section').style.display = 'none';
    document.getElementById('analysis-results').style.display = 'none';
    document.getElementById('image-url-input').value = '';
    document.getElementById('image-file-input').value = '';
}

// Camera Functions
function startCamera() {
    navigator.mediaDevices.getUserMedia({ 
        video: { facingMode: 'environment', width: 640, height: 480 } 
    })
    .then(stream => {
        cameraStream = stream;
        const video = document.getElementById('camera-video');
        video.srcObject = stream;
        video.play();
        
        document.getElementById('capture-btn').disabled = false;
        showMessage('Camera started! You can now capture photos.');
    })
    .catch(err => {
        console.error('Camera access error:', err);
        showMessage('Camera access denied. Please allow camera permissions or try uploading an image instead.');
    });
}

function capturePhoto() {
    const video = document.getElementById('camera-video');
    const canvas = document.getElementById('camera-canvas');
    const ctx = canvas.getContext('2d');
    
    // Set canvas size to match video
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    
    // Draw video frame to canvas
    ctx.drawImage(video, 0, 0);
    
    // Convert canvas to image data URL
    const imageDataURL = canvas.toDataURL('image/jpeg', 0.8);
    displayImagePreview(imageDataURL);
    
    showMessage('Photo captured! You can now analyze it.');
}

function stopCamera() {
    if (cameraStream) {
        cameraStream.getTracks().forEach(track => track.stop());
        cameraStream = null;
        
        const video = document.getElementById('camera-video');
        video.srcObject = null;
        
        document.getElementById('capture-btn').disabled = true;
        showMessage('Camera stopped.');
    }
}

// AI Image Analysis Functions
async function analyzeImage() {
    if (!currentImageData) {
        showMessage('Please select an image first.');
        return;
    }
    
    showMessage('🤖 Analyzing image with AI...');
    
    try {
        // Try ML API first, fallback to simulation
        const results = await analyzeImageWithML(currentImageData);
        displayAnalysisResults(results);
    } catch (error) {
        console.error('ML Analysis failed, using fallback:', error);
        // Fallback to simulation
        setTimeout(() => {
            const results = performImageAnalysis(currentImageData);
            displayAnalysisResults(results);
        }, 2000);
    }
}

// Enhanced ML-powered image analysis
async function analyzeImageWithML(imageData) {
    const ML_API_URL = 'http://localhost:5000';
    
    try {
        // Check if ML API is available
        const healthResponse = await fetch(`${ML_API_URL}/health`);
        if (!healthResponse.ok) {
            throw new Error('ML API not available');
        }
        
        // Call ML prediction API
        const response = await fetch(`${ML_API_URL}/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                image: imageData
            })
        });
        
        if (!response.ok) {
            throw new Error(`ML API error: ${response.status}`);
        }
        
        const mlResult = await response.json();
        
        if (!mlResult.success) {
            throw new Error(mlResult.error || 'ML prediction failed');
        }
        
        // Convert ML API response to our format
        analysisResults = {
            detectedItems: mlResult.detected_items.map(item => ({
                name: item.name,
                category: item.category,
                confidence: item.confidence
            })),
            colors: mlResult.colors || extractColors(),
            similarProducts: findSimilarProductsFromML(mlResult.detected_items),
            confidence: mlResult.overall_confidence,
            processingTime: mlResult.processing_time || '0.8s',
            source: 'ml_api'
        };
        
        showMessage(`✅ ML Analysis complete! Detected ${mlResult.detected_items.length} items with ${mlResult.overall_confidence}% confidence.`);
        return analysisResults;
        
    } catch (error) {
        console.warn('ML API unavailable, using fallback analysis:', error);
        throw error; // Let the calling function handle fallback
    }
}

function findSimilarProductsFromML(detectedItems) {
    const similarProducts = [];
    
    detectedItems.forEach(item => {
        // Enhanced matching using ML-detected categories
        const matchingProducts = products.filter(product => {
            // Direct category match
            if (product.type === item.type || product.category === item.category) {
                return true;
            }
            
            // Name/tag matching
            return product.name.toLowerCase().includes(item.name.toLowerCase()) ||
                   product.tags.some(tag => tag.toLowerCase().includes(item.name.toLowerCase()));
        });
        
        matchingProducts.slice(0, 2).forEach(product => {
            if (!similarProducts.find(p => p.id === product.id)) {
                const matchScore = Math.min(95, Math.floor(item.confidence + (item.confidence_boost * 100 || 0)));
                similarProducts.push({
                    ...product,
                    matchScore,
                    detectedAs: item.name
                });
            }
        });
    });
    
    return similarProducts.slice(0, 6);
}

function performImageAnalysis(imageData) {
    // Simulate AI image recognition with realistic results
    const detectedItems = generateDetectedItems();
    const colors = extractColors();
    const similarProducts = findSimilarProducts(detectedItems);
    
    analysisResults = {
        detectedItems,
        colors,
        similarProducts,
        confidence: Math.floor(Math.random() * 15) + 85, // 85-100%
        processingTime: (Math.random() * 1.5 + 0.3).toFixed(1) + 's'
    };
    
    return analysisResults;
}

function generateDetectedItems() {
    // Simulate AI detection with weighted randomness
    const possibleItems = [
        { name: 'Dress Shirt', category: 'tops', confidence: 0.92 },
        { name: 'Casual T-Shirt', category: 'tops', confidence: 0.88 },
        { name: 'Denim Jeans', category: 'bottoms', confidence: 0.95 },
        { name: 'Chino Pants', category: 'bottoms', confidence: 0.87 },
        { name: 'Sneakers', category: 'shoes', confidence: 0.91 },
        { name: 'Dress Shoes', category: 'shoes', confidence: 0.89 },
        { name: 'Blazer', category: 'outerwear', confidence: 0.93 },
        { name: 'Polo Shirt', category: 'tops', confidence: 0.86 },
        { name: 'Watch', category: 'accessories', confidence: 0.84 },
        { name: 'Leather Belt', category: 'accessories', confidence: 0.82 }
    ];
    
    // Randomly select 2-4 items
    const numItems = Math.floor(Math.random() * 3) + 2;
    const selectedItems = [];
    
    for (let i = 0; i < numItems; i++) {
        const randomItem = possibleItems[Math.floor(Math.random() * possibleItems.length)];
        if (!selectedItems.find(item => item.name === randomItem.name)) {
            selectedItems.push({
                ...randomItem,
                confidence: Math.floor(randomItem.confidence * 100)
            });
        }
    }
    
    return selectedItems.sort((a, b) => b.confidence - a.confidence);
}

function extractColors() {
    // Simulate color extraction
    const detectedColors = [
        { hex: '#1a1a1a', name: 'Charcoal', dominance: 0.35 },
        { hex: '#4169E1', name: 'Royal Blue', dominance: 0.25 },
        { hex: '#FFFFFF', name: 'White', dominance: 0.20 },
        { hex: '#2F4F4F', name: 'Dark Slate', dominance: 0.15 },
        { hex: '#C0C0C0', name: 'Silver', dominance: 0.05 }
    ];
    
    // Randomly select 3-5 colors
    const numColors = Math.floor(Math.random() * 3) + 3;
    return detectedColors.slice(0, numColors);
}

function findSimilarProducts(detectedItems) {
    const similarProducts = [];
    
    detectedItems.forEach(item => {
        // Find products that match the detected category
        const matchingProducts = products.filter(product => {
            const categoryMatch = productCategories[item.name.toLowerCase().replace(/\s+/g, '')];
            if (categoryMatch) {
                return product.type === categoryMatch.type || product.category === categoryMatch.category;
            }
            
            // Fallback: check if item name appears in product name or tags
            return product.name.toLowerCase().includes(item.name.toLowerCase()) ||
                   product.tags.some(tag => tag.toLowerCase().includes(item.name.toLowerCase()));
        });
        
        // Add top 2 matches for each detected item
        matchingProducts.slice(0, 2).forEach(product => {
            if (!similarProducts.find(p => p.id === product.id)) {
                similarProducts.push({
                    ...product,
                    matchScore: Math.floor(Math.random() * 20) + 80 // 80-100% match
                });
            }
        });
    });
    
    return similarProducts.slice(0, 6); // Limit to 6 similar products
}

function displayAnalysisResults(results) {
    const analysisSection = document.getElementById('analysis-results');
    const confidenceScore = document.getElementById('confidence-score');
    const detectedItemsList = document.getElementById('detected-items-list');
    const similarProductsGrid = document.getElementById('similar-products-grid');
    const colorPalette = document.getElementById('color-palette');
    
    // Update confidence score
    confidenceScore.textContent = `${results.confidence}%`;
    
    // Display detected items
    detectedItemsList.innerHTML = results.detectedItems.map(item => `
        <div class="detected-item">
            <div class="item-info">
                <strong>${item.name}</strong>
                <div style="font-size: 0.9em; color: #666;">${item.category}</div>
            </div>
            <div class="item-confidence">${item.confidence}%</div>
        </div>
    `).join('');
    
    // Display similar products
    similarProductsGrid.innerHTML = results.similarProducts.map(product => `
        <div class="similar-product-item" onclick="quickView(${product.id})">
            <img src="${product.image}" alt="${product.name}">
            <h6>${product.name}</h6>
            <p>£${product.price}</p>
            <div style="font-size: 0.8em; color: #27ae60; font-weight: 600;">${product.matchScore}% match</div>
        </div>
    `).join('');
    
    // Display color palette
    colorPalette.innerHTML = results.colors.map(color => `
        <div class="color-swatch" 
             style="background-color: ${color.hex}" 
             data-color="${color.name}"
             title="${color.name} (${Math.floor(color.dominance * 100)}%)"
             onclick="searchByColor('${color.name}')">
        </div>
    `).join('');
    
    analysisSection.style.display = 'block';
    showMessage(`✅ Analysis complete! Found ${results.detectedItems.length} items with ${results.confidence}% confidence.`);
}

function searchByColor(colorName) {
    closeModal('visual-search-modal');
    searchProducts(colorName);
    showMessage(`Searching for ${colorName} products...`);
}

// Visual Search Results Functions
function performVisualSearch() {
    if (!analysisResults) {
        showMessage('Please analyze an image first.');
        return;
    }
    
    const searchResults = generateVisualSearchResults();
    displayVisualSearchResults(searchResults);
    
    closeModal('visual-search-modal');
    showModal('recognition-results-modal');
}

function generateVisualSearchResults() {
    const allMatches = [];
    
    // Get products based on detected items
    analysisResults.detectedItems.forEach(item => {
        const categoryInfo = productCategories[item.name.toLowerCase().replace(/\s+/g, '')];
        
        const matchingProducts = products.filter(product => {
            if (categoryInfo) {
                return product.type === categoryInfo.type || 
                       product.category === categoryInfo.category;
            }
            return product.name.toLowerCase().includes(item.name.toLowerCase()) ||
                   product.tags.some(tag => tag.toLowerCase().includes(item.name.toLowerCase()));
        });
        
        matchingProducts.forEach(product => {
            if (!allMatches.find(m => m.id === product.id)) {
                const baseConfidence = item.confidence / 100;
                const categoryBoost = categoryInfo ? categoryInfo.confidence_boost : 0.05;
                const matchScore = Math.min(95, Math.floor((baseConfidence + categoryBoost) * 100));
                
                allMatches.push({
                    ...product,
                    matchScore,
                    detectedAs: item.name,
                    relevanceScore: matchScore + (product.rating * 2)
                });
            }
        });
    });
    
    // Sort by relevance score
    return allMatches.sort((a, b) => b.relevanceScore - a.relevanceScore).slice(0, 12);
}

function displayVisualSearchResults(results) {
    const analyzedImageDisplay = document.getElementById('analyzed-image-display');
    const detectionTags = document.getElementById('detection-tags');
    const totalMatches = document.getElementById('total-matches');
    const avgConfidence = document.getElementById('avg-confidence');
    const processingTime = document.getElementById('processing-time');
    const visualSearchResults = document.getElementById('visual-search-results');
    
    // Display analyzed image
    analyzedImageDisplay.src = currentImageData;
    
    // Display detection tags
    detectionTags.innerHTML = analysisResults.detectedItems.map(item => 
        `<span class="detection-tag">${item.name} (${item.confidence}%)</span>`
    ).join('');
    
    // Update statistics
    totalMatches.textContent = results.length;
    avgConfidence.textContent = `${Math.floor(results.reduce((sum, r) => sum + r.matchScore, 0) / results.length)}%`;
    processingTime.textContent = analysisResults.processingTime;
    
    // Display search results
    visualSearchResults.innerHTML = results.map(product => `
        <div class="visual-result-item" onclick="quickView(${product.id})">
            <img src="${product.image}" alt="${product.name}">
            <div class="visual-result-info">
                <div class="visual-result-match">
                    <span style="font-size: 0.8em; color: #666;">Detected as: ${product.detectedAs}</span>
                    <div class="match-score">${product.matchScore}%</div>
                </div>
                <div class="visual-result-title">${product.name}</div>
                <div class="visual-result-price">£${product.price}</div>
                <div class="visual-result-actions">
                    <button class="add-to-cart-visual" onclick="addToCart(${product.id}); event.stopPropagation();">Add to Cart</button>
                    <button class="view-details-visual" onclick="quickView(${product.id}); event.stopPropagation();">View Details</button>
                </div>
            </div>
        </div>
    `).join('');
}

function sortVisualResults() {
    // Implementation for sorting visual search results
    showMessage('Sorting results...');
}

function filterVisualResults() {
    // Implementation for filtering visual search results
    showMessage('Filtering results...');
}

// Enhanced chat integration
function startImageSearchFromChat() {
    const chatMessage = `
        <div class="style-tip">
            <span class="style-tip-icon">📸</span>
            <strong>Visual Search Ready!</strong><br>
            Upload an image or take a photo to find similar products in our store.
        </div>
        <span class="recommendation-chip" onclick="startImageSearch()">Start Visual Search</span>
    `;
    addChatMessage(chatMessage, 'bot');
}

// Add visual search to chat quick actions
function enhanceChat() {
    // This would be called to add visual search capabilities to the chat
    const visualSearchMessage = `
        📸 Try our new Visual Search feature! Upload any fashion image and I'll help you find similar products.
        <span class="recommendation-chip" onclick="startImageSearch()">📸 Visual Search</span>
    `;
    addChatMessage(visualSearchMessage, 'bot');
}

// Voice Recognition System
class MANVUEVoiceRecognition {
    constructor() {
        this.recognition = null;
        this.isListening = false;
        this.isContinuous = false;
        this.isVoiceFeedback = true;
        this.language = 'en-US';
        this.sensitivity = 0.8;
        this.wakeWord = 'hey manvue';
        this.currentTranscript = '';
        this.finalTranscript = '';
        this.voiceInterface = null;
        this.lastCommand = '';
        this.commandTimeout = null;
        this.wakingUp = false;
        
        this.initializeVoiceRecognition();
        this.loadVoiceSettings();
    }

    initializeVoiceRecognition() {
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            console.warn('Speech recognition not supported');
            this.showVoiceError('Speech recognition not supported in this browser');
            return;
        }

        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        this.recognition = new SpeechRecognition();
        
        this.recognition.continuous = true;
        this.recognition.interimResults = true;
        this.recognition.lang = this.language;
        this.recognition.maxAlternatives = 3;

        this.setupVoiceEvents();
        this.voiceInterface = document.getElementById('voice-interface');
    }

    setupVoiceEvents() {
        this.recognition.onstart = () => {
            this.isListening = true;
            this.updateVoiceUI('listening');
            this.updateVoiceCommand('Listening...');
        };

        this.recognition.onresult = (event) => {
            let interimTranscript = '';
            let finalTranscript = '';

            for (let i = event.resultIndex; i < event.results.length; i++) {
                const transcript = event.results[i][0].transcript;
                
                if (event.results[i].isFinal) {
                    finalTranscript += transcript;
                } else {
                    interimTranscript += transcript;
                }
            }

            this.currentTranscript = interimTranscript;
            this.finalTranscript = finalTranscript;
            
            this.updateTranscript(interimTranscript, finalTranscript);
            
            if (finalTranscript) {
                this.processVoiceCommand(finalTranscript.trim().toLowerCase());
            }
        };

        this.recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            this.handleVoiceError(event.error);
        };

        this.recognition.onend = () => {
            this.isListening = false;
            this.updateVoiceUI('idle');
            
            if (this.isContinuous && !this.wakingUp) {
                setTimeout(() => this.startListening(), 1000);
            }
        };
    }

    startListening() {
        if (!this.recognition) {
            this.showVoiceError('Voice recognition not available');
            return;
        }

        try {
            this.recognition.start();
            this.updateVoiceCommand(`Listening for "${this.wakeWord}"...`);
            this.provideFeedback('Voice recognition started');
        } catch (error) {
            console.error('Error starting voice recognition:', error);
            this.handleVoiceError('start_error');
        }
    }

    stopListening() {
        if (this.recognition && this.isListening) {
            this.recognition.stop();
            this.updateVoiceUI('idle');
            this.updateVoiceCommand('Voice recognition stopped');
            this.provideFeedback('Voice recognition stopped');
        }
    }

    processVoiceCommand(command) {
        // Check for wake word first
        if (!this.wakingUp && !command.includes(this.wakeWord)) {
            return;
        }

        // If wake word detected, enter wake mode
        if (command.includes(this.wakeWord)) {
            this.wakingUp = true;
            this.updateVoiceCommand('Ready! What would you like to do?');
            this.updateVoiceUI('processing');
            this.provideFeedback('Ready for your command');
            
            // Clear wake mode after 10 seconds
            clearTimeout(this.commandTimeout);
            this.commandTimeout = setTimeout(() => {
                this.wakingUp = false;
                this.updateVoiceCommand(`Say "${this.wakeWord}" to start`);
                this.updateVoiceUI('idle');
            }, 10000);
            
            return;
        }

        // Process commands only in wake mode
        if (!this.wakingUp) return;

        this.lastCommand = command;
        this.updateVoiceCommand(`Processing: "${command}"`);
        this.updateVoiceUI('processing');

        // Execute voice command
        const executed = this.executeVoiceCommand(command);
        
        if (executed) {
            this.wakingUp = false;
            this.updateVoiceCommand('Command executed successfully');
            this.provideFeedback('Command completed');
            setTimeout(() => {
                this.updateVoiceCommand(`Say "${this.wakeWord}" to start`);
                this.updateVoiceUI('idle');
            }, 2000);
        } else {
            this.updateVoiceCommand('Sorry, I didn\'t understand that command');
            this.provideFeedback('Command not recognized');
        }

        clearTimeout(this.commandTimeout);
    }

    executeVoiceCommand(command) {
        // Shopping Commands
        if (command.includes('add to cart')) {
            const currentProduct = this.getCurrentProduct();
            if (currentProduct) {
                addToCart(currentProduct.id);
                return true;
            }
            this.provideFeedback('No product selected');
            return false;
        }

        if (command.includes('remove from cart')) {
            // Implementation for cart removal
            this.provideFeedback('Item removed from cart');
            return true;
        }

        if (command.includes('show cart') || command.includes('view cart')) {
            toggleCart();
            return true;
        }

        if (command.includes('checkout')) {
            this.provideFeedback('Proceeding to checkout');
            // Implementation for checkout
            return true;
        }

        // Search Commands
        if (command.includes('search for')) {
            const searchTerm = command.replace('search for', '').trim();
            if (searchTerm) {
                searchProducts(searchTerm);
                return true;
            }
        }

        if (command.includes('show me') || command.includes('find')) {
            const category = this.extractCategory(command);
            if (category) {
                filterProducts(category);
                return true;
            }
        }

        if (command.includes('filter by price')) {
            this.showPriceFilter();
            return true;
        }

        if (command.includes('sort by')) {
            const sortType = this.extractSortType(command);
            if (sortType) {
                this.applySorting(sortType);
                return true;
            }
        }

        // Navigation Commands
        if (command.includes('go home') || command.includes('home page')) {
            this.scrollToSection('hero-banner');
            return true;
        }

        if (command.includes('show profile') || command.includes('my profile')) {
            showProfile();
            return true;
        }

        if (command.includes('open wishlist') || command.includes('show wishlist')) {
            toggleWishlist();
            return true;
        }

        if (command.includes('scroll down')) {
            window.scrollBy(0, 300);
            return true;
        }

        if (command.includes('scroll up')) {
            window.scrollBy(0, -300);
            return true;
        }

        // AI Commands
        if (command.includes('style quiz') || command.includes('take quiz')) {
            startStyleQuiz();
            return true;
        }

        if (command.includes('recommendations') || command.includes('suggest')) {
            showStyleRecommendations();
            return true;
        }

        if (command.includes('visual search') || command.includes('image search')) {
            startImageSearch();
            return true;
        }

        if (command.includes('chat') || command.includes('assistant')) {
            toggleChatbot();
            return true;
        }

        // General Commands
        if (command.includes('help') || command.includes('commands')) {
            showVoiceCommands();
            return true;
        }

        if (command.includes('settings')) {
            toggleVoiceSettings();
            return true;
        }

        return false;
    }

    getCurrentProduct() {
        // Try to find currently viewed product
        const productModal = document.querySelector('.modal[style*="display: block"]');
        if (productModal && productModal.id.includes('product')) {
            const productId = productModal.getAttribute('data-product-id');
            return products.find(p => p.id == productId);
        }
        return null;
    }

    extractCategory(command) {
        const categories = ['shirts', 'pants', 'shoes', 'jackets', 'accessories', 'tops', 'bottoms'];
        return categories.find(cat => command.includes(cat));
    }

    extractSortType(command) {
        if (command.includes('price')) return 'price';
        if (command.includes('rating')) return 'rating';
        if (command.includes('name')) return 'name';
        if (command.includes('popularity')) return 'popularity';
        return null;
    }

    applySorting(sortType) {
        const sortSelect = document.getElementById('sort-select');
        if (sortSelect) {
            sortSelect.value = sortType;
            sortSelect.dispatchEvent(new Event('change'));
        }
    }

    showPriceFilter() {
        const priceFilter = document.querySelector('.price-filter');
        if (priceFilter) {
            priceFilter.scrollIntoView({ behavior: 'smooth' });
        }
    }

    scrollToSection(sectionId) {
        const section = document.getElementById(sectionId);
        if (section) {
            section.scrollIntoView({ behavior: 'smooth' });
        }
    }

    updateVoiceUI(state) {
        const voiceInterface = document.getElementById('voice-interface');
        const voiceIndicator = document.getElementById('voice-indicator');
        const voiceToggle = document.querySelector('.voice-toggle');

        // Remove all state classes
        voiceInterface.classList.remove('listening', 'processing', 'error', 'speaking');
        voiceIndicator.classList.remove('listening', 'processing', 'error', 'speaking');
        voiceToggle.classList.remove('active');

        // Add current state class
        if (state !== 'idle') {
            voiceInterface.classList.add(state);
            voiceIndicator.classList.add(state);
            
            if (state === 'listening' || state === 'processing') {
                voiceToggle.classList.add('active');
            }
        }
    }

    updateVoiceCommand(text) {
        const commandElement = document.getElementById('voice-command');
        if (commandElement) {
            commandElement.textContent = text;
        }
    }

    updateTranscript(interim, final) {
        const transcriptElement = document.getElementById('voice-transcript');
        if (transcriptElement) {
            let displayText = '';
            if (final) {
                displayText = final;
                transcriptElement.className = 'voice-transcript final';
            } else if (interim) {
                displayText = interim;
                transcriptElement.className = 'voice-transcript interim';
            }
            transcriptElement.textContent = displayText;
        }
    }

    provideFeedback(message) {
        if (this.isVoiceFeedback && 'speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance(message);
            utterance.rate = 0.8;
            utterance.pitch = 1;
            utterance.volume = 0.7;
            speechSynthesis.speak(utterance);
            
            this.updateVoiceUI('speaking');
            utterance.onend = () => {
                if (!this.isListening) {
                    this.updateVoiceUI('idle');
                }
            };
        }
        
        showMessage(`🎤 ${message}`);
    }

    handleVoiceError(error) {
        let message = 'Voice recognition error occurred';
        
        switch (error) {
            case 'no-speech':
                message = 'No speech detected. Please try again.';
                break;
            case 'audio-capture':
                message = 'Microphone access denied or unavailable.';
                break;
            case 'not-allowed':
                message = 'Microphone permission denied.';
                break;
            case 'network':
                message = 'Network error occurred.';
                break;
            default:
                message = `Voice error: ${error}`;
        }

        this.updateVoiceUI('error');
        this.updateVoiceCommand(message);
        this.showVoiceError(message);
    }

    showVoiceError(message) {
        showMessage(`❌ ${message}`);
        setTimeout(() => {
            this.updateVoiceUI('idle');
            this.updateVoiceCommand(`Say "${this.wakeWord}" to start`);
        }, 3000);
    }

    // Settings Management
    loadVoiceSettings() {
        const settings = localStorage.getItem('manvue-voice-settings');
        if (settings) {
            const parsed = JSON.parse(settings);
            this.language = parsed.language || 'en-US';
            this.sensitivity = parsed.sensitivity || 0.8;
            this.isContinuous = parsed.continuous || false;
            this.isVoiceFeedback = parsed.feedback !== false;
            this.wakeWord = parsed.wakeWord || 'hey manvue';
            
            this.updateSettingsUI();
        }
    }

    saveVoiceSettings() {
        const settings = {
            language: this.language,
            sensitivity: this.sensitivity,
            continuous: this.isContinuous,
            feedback: this.isVoiceFeedback,
            wakeWord: this.wakeWord
        };
        localStorage.setItem('manvue-voice-settings', JSON.stringify(settings));
    }

    updateSettingsUI() {
        const langSelect = document.getElementById('voice-language');
        const sensitivitySlider = document.getElementById('voice-sensitivity');
        const continuousCheck = document.getElementById('continuous-listening');
        const feedbackCheck = document.getElementById('voice-feedback');
        const wakeWordSelect = document.getElementById('wake-word');
        const sensitivityValue = document.getElementById('sensitivity-value');

        if (langSelect) langSelect.value = this.language;
        if (sensitivitySlider) {
            sensitivitySlider.value = this.sensitivity;
            if (sensitivityValue) {
                sensitivityValue.textContent = `${Math.round(this.sensitivity * 100)}%`;
            }
        }
        if (continuousCheck) continuousCheck.checked = this.isContinuous;
        if (feedbackCheck) feedbackCheck.checked = this.isVoiceFeedback;
        if (wakeWordSelect) wakeWordSelect.value = this.wakeWord;
    }

    updateLanguage(language) {
        this.language = language;
        if (this.recognition) {
            this.recognition.lang = language;
        }
        this.saveVoiceSettings();
    }

    updateSensitivity(sensitivity) {
        this.sensitivity = sensitivity;
        this.saveVoiceSettings();
        
        const sensitivityValue = document.getElementById('sensitivity-value');
        if (sensitivityValue) {
            sensitivityValue.textContent = `${Math.round(sensitivity * 100)}%`;
        }
    }

    toggleContinuous(enabled) {
        this.isContinuous = enabled;
        this.saveVoiceSettings();
        
        if (enabled && !this.isListening) {
            this.startListening();
        } else if (!enabled && this.isListening) {
            this.stopListening();
        }
    }

    toggleFeedback(enabled) {
        this.isVoiceFeedback = enabled;
        this.saveVoiceSettings();
    }

    updateWakeWord(wakeWord) {
        this.wakeWord = wakeWord;
        this.saveVoiceSettings();
        this.updateVoiceCommand(`Say "${wakeWord}" to start`);
    }

    testRecognition() {
        this.provideFeedback('Voice recognition test. Please say something.');
        this.startListening();
        
        setTimeout(() => {
            this.stopListening();
            this.provideFeedback('Voice test completed');
        }, 5000);
    }

    calibrateVoice() {
        this.provideFeedback('Voice calibration started. Please speak normally for 10 seconds.');
        // Implementation for voice calibration
        setTimeout(() => {
            this.provideFeedback('Voice calibration completed');
        }, 10000);
    }
}

// Initialize voice recognition system
const manvueVoice = new MANVUEVoiceRecognition();

// Voice Interface Functions
function toggleVoiceInterface() {
    const voiceInterface = document.getElementById('voice-interface');
    voiceInterface.classList.toggle('active');
}

function toggleVoiceRecognition() {
    const toggleBtn = document.getElementById('voice-toggle');
    const btnText = document.getElementById('voice-btn-text');
    
    if (manvueVoice.isListening) {
        manvueVoice.stopListening();
        toggleBtn.classList.remove('active');
        btnText.textContent = '🎤 Start Voice';
    } else {
        manvueVoice.startListening();
        toggleBtn.classList.add('active');
        btnText.textContent = '🔴 Stop Voice';
    }
}

function showVoiceCommands() {
    showModal('voice-commands-modal');
}

function toggleVoiceSettings() {
    showModal('voice-settings-modal');
}

// Voice Settings Functions
function updateVoiceLanguage() {
    const language = document.getElementById('voice-language').value;
    manvueVoice.updateLanguage(language);
}

function updateVoiceSensitivity() {
    const sensitivity = parseFloat(document.getElementById('voice-sensitivity').value);
    manvueVoice.updateSensitivity(sensitivity);
}

function toggleContinuousListening() {
    const enabled = document.getElementById('continuous-listening').checked;
    manvueVoice.toggleContinuous(enabled);
}

function toggleVoiceFeedback() {
    const enabled = document.getElementById('voice-feedback').checked;
    manvueVoice.toggleFeedback(enabled);
}

function updateWakeWord() {
    const wakeWord = document.getElementById('wake-word').value;
    manvueVoice.updateWakeWord(wakeWord);
}

function testVoiceRecognition() {
    manvueVoice.testRecognition();
}

function calibrateVoice() {
    manvueVoice.calibrateVoice();
}

// 3D Virtual Try-On System
class MANVUE3DTryOn {
    constructor() {
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.controls = null;
        this.avatar = null;
        this.clothing = {};
        this.environment = 'studio';
        this.lighting = 1.0;
        this.bodyMeasurements = {
            height: 175,
            chest: 95,
            waist: 85,
            shoulders: 45
        };
        this.currentOutfit = [];
        this.cameraStream = null;
        this.bodyTracking = false;
        this.isInitialized = false;
        
        this.init3DEngine();
        this.loadBodyMeasurements();
    }

    init3DEngine() {
        // Initialize Three.js scene
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0x222222);

        // Setup camera
        this.camera = new THREE.PerspectiveCamera(
            75,
            window.innerWidth / window.innerHeight,
            0.1,
            1000
        );
        this.camera.position.set(0, 1.6, 3);

        // Setup renderer
        const container = document.getElementById('threejs-container');
        if (container) {
            this.renderer = new THREE.WebGLRenderer({
                canvas: document.getElementById('threejs-canvas'),
                antialias: true,
                alpha: true
            });
            this.renderer.setSize(container.clientWidth, container.clientHeight);
            this.renderer.setPixelRatio(window.devicePixelRatio);
            this.renderer.shadowMap.enabled = true;
            this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
            this.renderer.outputEncoding = THREE.sRGBEncoding;
            this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
            this.renderer.toneMappingExposure = 1.0;
        }

        // Setup controls
        if (this.renderer && typeof THREE.OrbitControls !== 'undefined') {
            this.controls = new THREE.OrbitControls(this.camera, this.renderer.domElement);
            this.controls.enableDamping = true;
            this.controls.dampingFactor = 0.05;
            this.controls.maxPolarAngle = Math.PI / 2;
            this.controls.minDistance = 1;
            this.controls.maxDistance = 10;
        }

        // Setup lighting
        this.setupLighting();
        
        // Create basic avatar
        this.createAvatar();
        
        // Start render loop
        this.animate();
        
        this.isInitialized = true;
        this.hideLoading();
    }

    setupLighting() {
        // Ambient light
        const ambientLight = new THREE.AmbientLight(0x404040, 0.4);
        this.scene.add(ambientLight);

        // Main directional light
        const directionalLight = new THREE.DirectionalLight(0xffffff, this.lighting);
        directionalLight.position.set(5, 5, 5);
        directionalLight.castShadow = true;
        directionalLight.shadow.mapSize.width = 2048;
        directionalLight.shadow.mapSize.height = 2048;
        directionalLight.shadow.camera.near = 0.5;
        directionalLight.shadow.camera.far = 500;
        this.scene.add(directionalLight);

        // Fill light
        const fillLight = new THREE.DirectionalLight(0xffffff, 0.3);
        fillLight.position.set(-5, 0, -5);
        this.scene.add(fillLight);

        // Rim light
        const rimLight = new THREE.DirectionalLight(0xffffff, 0.5);
        rimLight.position.set(0, 5, -5);
        this.scene.add(rimLight);
    }

    createAvatar() {
        // Create a basic humanoid avatar using primitive shapes
        const avatarGroup = new THREE.Group();

        // Body parts materials
        const skinMaterial = new THREE.MeshLambertMaterial({ color: 0xfdbcb4 });
        const hairMaterial = new THREE.MeshLambertMaterial({ color: 0x4a4a4a });

        // Head
        const headGeometry = new THREE.SphereGeometry(0.12, 16, 16);
        const head = new THREE.Mesh(headGeometry, skinMaterial);
        head.position.y = 1.65;
        head.castShadow = true;
        avatarGroup.add(head);

        // Body (torso)
        const torsoGeometry = new THREE.BoxGeometry(0.35, 0.6, 0.2);
        const torso = new THREE.Mesh(torsoGeometry, skinMaterial);
        torso.position.y = 1.2;
        torso.castShadow = true;
        avatarGroup.add(torso);

        // Arms
        const armGeometry = new THREE.CapsuleGeometry(0.06, 0.5, 8, 16);
        
        const leftArm = new THREE.Mesh(armGeometry, skinMaterial);
        leftArm.position.set(-0.25, 1.2, 0);
        leftArm.castShadow = true;
        avatarGroup.add(leftArm);

        const rightArm = new THREE.Mesh(armGeometry, skinMaterial);
        rightArm.position.set(0.25, 1.2, 0);
        rightArm.castShadow = true;
        avatarGroup.add(rightArm);

        // Legs
        const legGeometry = new THREE.CapsuleGeometry(0.08, 0.8, 8, 16);
        
        const leftLeg = new THREE.Mesh(legGeometry, skinMaterial);
        leftLeg.position.set(-0.1, 0.5, 0);
        leftLeg.castShadow = true;
        avatarGroup.add(leftLeg);

        const rightLeg = new THREE.Mesh(legGeometry, skinMaterial);
        rightLeg.position.set(0.1, 0.5, 0);
        rightLeg.castShadow = true;
        avatarGroup.add(rightLeg);

        // Ground plane
        const groundGeometry = new THREE.PlaneGeometry(10, 10);
        const groundMaterial = new THREE.MeshLambertMaterial({ color: 0x999999 });
        const ground = new THREE.Mesh(groundGeometry, groundMaterial);
        ground.rotation.x = -Math.PI / 2;
        ground.receiveShadow = true;
        this.scene.add(ground);

        this.avatar = avatarGroup;
        this.scene.add(avatarGroup);
        
        // Apply measurements to avatar
        this.updateAvatarMeasurements();
    }

    updateAvatarMeasurements() {
        if (!this.avatar) return;

        const { height, chest, waist, shoulders } = this.bodyMeasurements;
        
        // Scale avatar based on measurements
        const heightScale = height / 175; // Base height 175cm
        const chestScale = chest / 95; // Base chest 95cm
        const waistScale = waist / 85; // Base waist 85cm
        const shoulderScale = shoulders / 45; // Base shoulders 45cm

        this.avatar.scale.y = heightScale;
        this.avatar.scale.x = (chestScale + shoulderScale) / 2;
        this.avatar.scale.z = (chestScale + waistScale) / 2;

        // Update size recommendation
        this.calculateSizeRecommendation();
    }

    calculateSizeRecommendation() {
        const { chest, waist } = this.bodyMeasurements;
        let recommendedSize = 'M';
        let confidence = 95;

        if (chest < 90 && waist < 80) {
            recommendedSize = 'S';
            confidence = 92;
        } else if (chest > 105 || waist > 95) {
            recommendedSize = 'L';
            confidence = 88;
        } else if (chest > 115 || waist > 105) {
            recommendedSize = 'XL';
            confidence = 85;
        }

        // Update UI
        const sizeElement = document.querySelector('.size-badge');
        const confidenceElement = document.querySelector('.confidence');
        const detailsElement = document.getElementById('size-details');

        if (sizeElement) sizeElement.textContent = recommendedSize;
        if (confidenceElement) confidenceElement.textContent = `${confidence}% Match`;
        if (detailsElement) {
            detailsElement.textContent = `Based on your measurements (${chest}cm chest, ${this.bodyMeasurements.waist}cm waist), we recommend size ${recommendedSize} for optimal fit.`;
        }
    }

    addClothingItem(productId, type) {
        // Create clothing geometry based on type
        let clothingMesh;
        const clothingMaterial = new THREE.MeshLambertMaterial({ 
            color: Math.random() * 0xffffff 
        });

        switch (type) {
            case 'tops':
                clothingMesh = this.createShirtGeometry(clothingMaterial);
                break;
            case 'bottoms':
                clothingMesh = this.createPantsGeometry(clothingMaterial);
                break;
            case 'shoes':
                clothingMesh = this.createShoesGeometry(clothingMaterial);
                break;
            default:
                return;
        }

        // Remove existing clothing of same type
        if (this.clothing[type]) {
            this.avatar.remove(this.clothing[type]);
        }

        // Add new clothing
        this.clothing[type] = clothingMesh;
        this.avatar.add(clothingMesh);

        // Update current outfit
        const existingIndex = this.currentOutfit.findIndex(item => item.type === type);
        if (existingIndex !== -1) {
            this.currentOutfit[existingIndex] = { productId, type };
        } else {
            this.currentOutfit.push({ productId, type });
        }

        showMessage(`Added ${type} to virtual outfit`);
    }

    createShirtGeometry(material) {
        const shirtGroup = new THREE.Group();
        
        // Shirt body
        const bodyGeometry = new THREE.BoxGeometry(0.37, 0.55, 0.22);
        const body = new THREE.Mesh(bodyGeometry, material);
        body.position.y = 1.2;
        shirtGroup.add(body);

        // Sleeves
        const sleeveGeometry = new THREE.CapsuleGeometry(0.07, 0.3, 8, 16);
        
        const leftSleeve = new THREE.Mesh(sleeveGeometry, material);
        leftSleeve.position.set(-0.25, 1.3, 0);
        leftSleeve.rotation.z = Math.PI / 6;
        shirtGroup.add(leftSleeve);

        const rightSleeve = new THREE.Mesh(sleeveGeometry, material);
        rightSleeve.position.set(0.25, 1.3, 0);
        rightSleeve.rotation.z = -Math.PI / 6;
        shirtGroup.add(rightSleeve);

        return shirtGroup;
    }

    createPantsGeometry(material) {
        const pantsGroup = new THREE.Group();
        
        // Waist
        const waistGeometry = new THREE.BoxGeometry(0.36, 0.15, 0.22);
        const waist = new THREE.Mesh(waistGeometry, material);
        waist.position.y = 0.85;
        pantsGroup.add(waist);

        // Legs
        const legGeometry = new THREE.CapsuleGeometry(0.09, 0.7, 8, 16);
        
        const leftLeg = new THREE.Mesh(legGeometry, material);
        leftLeg.position.set(-0.1, 0.45, 0);
        pantsGroup.add(leftLeg);

        const rightLeg = new THREE.Mesh(legGeometry, material);
        rightLeg.position.set(0.1, 0.45, 0);
        pantsGroup.add(rightLeg);

        return pantsGroup;
    }

    createShoesGeometry(material) {
        const shoesGroup = new THREE.Group();
        
        const shoeGeometry = new THREE.BoxGeometry(0.1, 0.08, 0.25);
        
        const leftShoe = new THREE.Mesh(shoeGeometry, material);
        leftShoe.position.set(-0.1, 0.04, 0.05);
        shoesGroup.add(leftShoe);

        const rightShoe = new THREE.Mesh(shoeGeometry, material);
        rightShoe.position.set(0.1, 0.04, 0.05);
        shoesGroup.add(rightShoe);

        return shoesGroup;
    }

    animate() {
        requestAnimationFrame(() => this.animate());

        if (this.controls) {
            this.controls.update();
        }

        if (this.renderer && this.scene && this.camera) {
            this.renderer.render(this.scene, this.camera);
        }
    }

    hideLoading() {
        const loadingElement = document.getElementById('3d-loading');
        if (loadingElement) {
            loadingElement.parentElement.classList.add('hidden');
        }
    }

    adjustLighting(intensity) {
        this.lighting = intensity;
        const lights = this.scene.children.filter(child => child.type === 'DirectionalLight');
        lights.forEach(light => {
            if (light.intensity > 0.5) { // Main light
                light.intensity = intensity;
            }
        });
    }

    changeEnvironment(preset) {
        this.environment = preset;
        let backgroundColor;
        
        switch (preset) {
            case 'studio':
                backgroundColor = 0x222222;
                break;
            case 'outdoor':
                backgroundColor = 0x87CEEB;
                break;
            case 'indoor':
                backgroundColor = 0xF5F5DC;
                break;
            case 'sunset':
                backgroundColor = 0xFF6347;
                break;
            default:
                backgroundColor = 0x222222;
        }
        
        this.scene.background = new THREE.Color(backgroundColor);
    }

    // Camera and body tracking
    async startCamera() {
        try {
            this.cameraStream = await navigator.mediaDevices.getUserMedia({ 
                video: { 
                    facingMode: 'user',
                    width: { ideal: 1280 },
                    height: { ideal: 720 }
                } 
            });
            
            const video = document.getElementById('tryon-camera');
            if (video) {
                video.srcObject = this.cameraStream;
                video.play();
                
                // Start body tracking
                this.startBodyTracking();
                showMessage('Camera started - body tracking active');
            }
        } catch (error) {
            console.error('Camera access error:', error);
            showMessage('Camera access denied or unavailable');
        }
    }

    stopCamera() {
        if (this.cameraStream) {
            this.cameraStream.getTracks().forEach(track => track.stop());
            this.cameraStream = null;
            
            const video = document.getElementById('tryon-camera');
            if (video) {
                video.srcObject = null;
            }
            
            this.stopBodyTracking();
            showMessage('Camera stopped');
        }
    }

    startBodyTracking() {
        this.bodyTracking = true;
        // Simulate body tracking points
        this.simulateBodyTracking();
    }

    stopBodyTracking() {
        this.bodyTracking = false;
        const trackingContainer = document.getElementById('body-tracking');
        if (trackingContainer) {
            trackingContainer.innerHTML = '';
        }
    }

    simulateBodyTracking() {
        if (!this.bodyTracking) return;

        const trackingContainer = document.getElementById('body-tracking');
        if (!trackingContainer) return;

        // Clear existing points
        trackingContainer.innerHTML = '';

        // Simulate key body points
        const bodyPoints = [
            { x: 50, y: 15, label: 'head' },
            { x: 45, y: 25, label: 'left-shoulder' },
            { x: 55, y: 25, label: 'right-shoulder' },
            { x: 50, y: 35, label: 'chest' },
            { x: 50, y: 45, label: 'waist' },
            { x: 47, y: 65, label: 'left-hip' },
            { x: 53, y: 65, label: 'right-hip' },
            { x: 47, y: 85, label: 'left-knee' },
            { x: 53, y: 85, label: 'right-knee' }
        ];

        bodyPoints.forEach(point => {
            const trackingPoint = document.createElement('div');
            trackingPoint.className = 'tracking-point';
            trackingPoint.style.left = `${point.x}%`;
            trackingPoint.style.top = `${point.y}%`;
            trackingPoint.title = point.label;
            trackingContainer.appendChild(trackingPoint);
        });

        // Auto-detect measurements from tracking
        setTimeout(() => this.autoDetectMeasurements(), 2000);
    }

    autoDetectMeasurements() {
        // Simulate auto-detection
        const detectedMeasurements = {
            height: 170 + Math.random() * 20,
            chest: 90 + Math.random() * 20,
            waist: 80 + Math.random() * 15,
            shoulders: 42 + Math.random() * 8
        };

        this.updateMeasurements(detectedMeasurements);
        showMessage('Body measurements auto-detected from camera');
    }

    updateMeasurements(measurements) {
        this.bodyMeasurements = { ...this.bodyMeasurements, ...measurements };
        
        // Update UI
        Object.keys(measurements).forEach(key => {
            const valueElement = document.getElementById(`${key}-measurement`);
            const sliderElement = document.getElementById(`${key}-adjust`);
            
            if (valueElement) {
                valueElement.textContent = `${Math.round(measurements[key])}cm`;
            }
            if (sliderElement) {
                sliderElement.value = measurements[key];
            }
        });

        // Update 3D avatar
        this.updateAvatarMeasurements();
        
        // Save measurements
        this.saveBodyMeasurements();
    }

    saveBodyMeasurements() {
        localStorage.setItem('manvue-body-measurements', JSON.stringify(this.bodyMeasurements));
    }

    loadBodyMeasurements() {
        const saved = localStorage.getItem('manvue-body-measurements');
        if (saved) {
            this.bodyMeasurements = JSON.parse(saved);
            this.updateMeasurements(this.bodyMeasurements);
        }
    }

    exportMeasurements() {
        const data = {
            measurements: this.bodyMeasurements,
            recommendedSize: document.querySelector('.size-badge')?.textContent || 'M',
            outfit: this.currentOutfit,
            timestamp: new Date().toISOString()
        };

        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'manvue-measurements.json';
        a.click();
        URL.revokeObjectURL(url);

        showMessage('Measurements exported successfully');
    }

    saveOutfit() {
        if (this.currentOutfit.length === 0) {
            showMessage('No outfit to save');
            return;
        }

        const outfits = JSON.parse(localStorage.getItem('manvue-saved-outfits') || '[]');
        const newOutfit = {
            id: Date.now(),
            name: `Outfit ${outfits.length + 1}`,
            items: this.currentOutfit,
            measurements: this.bodyMeasurements,
            timestamp: new Date().toISOString()
        };

        outfits.push(newOutfit);
        localStorage.setItem('manvue-saved-outfits', JSON.stringify(outfits));

        showMessage('Outfit saved successfully');
    }

    shareOutfit() {
        if (this.currentOutfit.length === 0) {
            showMessage('No outfit to share');
            return;
        }

        // Generate shareable link (simulate)
        const shareData = {
            outfit: this.currentOutfit,
            measurements: this.bodyMeasurements
        };

        const shareUrl = `${window.location.origin}/outfit/${btoa(JSON.stringify(shareData))}`;
        
        if (navigator.share) {
            navigator.share({
                title: 'My MANVUE Outfit',
                text: 'Check out my virtual outfit!',
                url: shareUrl
            });
        } else {
            navigator.clipboard.writeText(shareUrl);
            showMessage('Outfit link copied to clipboard');
        }
    }

    resize() {
        if (!this.renderer || !this.camera) return;

        const container = document.getElementById('threejs-container');
        if (container) {
            const width = container.clientWidth;
            const height = container.clientHeight;

            this.camera.aspect = width / height;
            this.camera.updateProjectionMatrix();
            this.renderer.setSize(width, height);
        }
    }
}

// Initialize 3D Try-On System
let manvue3D = null;

// 3D Interface Functions
function toggle3DTryOn() {
    showModal('tryon-3d-modal');
    if (!manvue3D) {
        manvue3D = new MANVUE3DTryOn();
    }
}

function start3DCamera() {
    if (manvue3D) {
        manvue3D.startCamera();
    }
}

function stop3DCamera() {
    if (manvue3D) {
        manvue3D.stopCamera();
    }
}

function capture3DPhoto() {
    const video = document.getElementById('tryon-camera');
    const canvas = document.getElementById('tryon-canvas');
    
    if (video && canvas) {
        const ctx = canvas.getContext('2d');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        ctx.drawImage(video, 0, 0);
        
        showMessage('Photo captured for fitting analysis');
    }
}

function toggle3DView() {
    // Toggle between camera and 3D view
    const cameraSection = document.querySelector('.camera-section');
    const visualizationSection = document.querySelector('.visualization-section');
    
    if (cameraSection && visualizationSection) {
        const isHidden = cameraSection.style.display === 'none';
        cameraSection.style.display = isHidden ? 'flex' : 'none';
        visualizationSection.style.display = isHidden ? 'none' : 'flex';
    }
}

function change3DViewMode() {
    const mode = document.getElementById('view-mode').value;
    showMessage(`Switched to ${mode} view mode`);
    // Implementation for different view modes
}

function adjust3DLighting() {
    const intensity = parseFloat(document.getElementById('lighting-intensity').value);
    if (manvue3D) {
        manvue3D.adjustLighting(intensity);
    }
}

function change3DEnvironment() {
    const environment = document.getElementById('environment-preset').value;
    if (manvue3D) {
        manvue3D.changeEnvironment(environment);
    }
}

function showTryOnCategory(category) {
    // Update tab appearance
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    
    // Filter and display products
    const grid = document.getElementById('tryon-products-grid');
    if (grid) {
        const filteredProducts = category === 'all' ? products : 
            products.filter(p => p.type === category || p.category === category);
        
        grid.innerHTML = filteredProducts.map(product => `
            <div class="tryon-product-item" onclick="addTo3DOutfit(${product.id}, '${product.type}')">
                <img src="${product.image}" alt="${product.name}">
                <div class="tryon-product-info">
                    <div class="tryon-product-name">${product.name}</div>
                    <div class="tryon-product-price">£${product.price}</div>
                </div>
            </div>
        `).join('');
    }
}

function addTo3DOutfit(productId, type) {
    if (manvue3D) {
        manvue3D.addClothingItem(productId, type);
    }
}

function adjustBodyMeasurement(type, value) {
    const valueElement = document.getElementById(`${type}-measurement`);
    if (valueElement) {
        valueElement.textContent = `${value}cm`;
    }
    
    if (manvue3D) {
        manvue3D.updateMeasurements({ [type]: parseFloat(value) });
    }
}

function save3DMeasurements() {
    if (manvue3D) {
        manvue3D.saveBodyMeasurements();
        showMessage('Measurements saved to your profile');
    }
}

function autoDetectMeasurements() {
    if (manvue3D) {
        manvue3D.autoDetectMeasurements();
    } else {
        showMessage('Please start the camera first');
    }
}

function reset3DMeasurements() {
    const defaultMeasurements = {
        height: 175,
        chest: 95,
        waist: 85,
        shoulders: 45
    };
    
    if (manvue3D) {
        manvue3D.updateMeasurements(defaultMeasurements);
    }
    
    showMessage('Measurements reset to default values');
}

function startVirtualFitting() {
    if (!manvue3D) {
        showMessage('Please initialize 3D system first');
        return;
    }
    
    showMessage('Virtual fitting session started');
    // Load default products for fitting
    showTryOnCategory('all');
}

function save3DOutfit() {
    if (manvue3D) {
        manvue3D.saveOutfit();
    }
}

function share3DOutfit() {
    if (manvue3D) {
        manvue3D.shareOutfit();
    }
}

function exportMeasurements() {
    if (manvue3D) {
        manvue3D.exportMeasurements();
    }
}

// 3D Product Viewer Functions
function show3DProduct(productId) {
    showModal('product-3d-modal');
    
    const product = products.find(p => p.id === productId);
    if (product) {
        document.getElementById('product-3d-name').textContent = product.name;
        document.getElementById('product-3d-description').textContent = product.description || 'High-quality product with excellent craftsmanship.';
        document.getElementById('product-material').textContent = product.material || 'Cotton Blend';
        document.getElementById('product-fit').textContent = product.fit || 'Regular Fit';
        document.getElementById('product-care').textContent = product.care || 'Machine Wash';
    }
    
    // Initialize 3D product viewer
    init3DProductViewer(product);
}

function init3DProductViewer(product) {
    const container = document.getElementById('product-threejs-viewer');
    const canvas = document.getElementById('product-threejs-canvas');
    
    if (!container || !canvas) return;
    
    // Create simple 3D product representation
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xf0f0f0);
    
    const camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
    camera.position.z = 2;
    
    const renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    
    // Create product geometry based on type
    let geometry, material;
    
    switch (product.type) {
        case 'tops':
            geometry = new THREE.BoxGeometry(1, 1.2, 0.2);
            material = new THREE.MeshLambertMaterial({ color: 0x4169E1 });
            break;
        case 'bottoms':
            geometry = new THREE.CylinderGeometry(0.3, 0.5, 1.5, 8);
            material = new THREE.MeshLambertMaterial({ color: 0x2F4F4F });
            break;
        case 'shoes':
            geometry = new THREE.BoxGeometry(0.8, 0.3, 1.2);
            material = new THREE.MeshLambertMaterial({ color: 0x8B4513 });
            break;
        default:
            geometry = new THREE.BoxGeometry(1, 1, 1);
            material = new THREE.MeshLambertMaterial({ color: 0x888888 });
    }
    
    const productMesh = new THREE.Mesh(geometry, material);
    scene.add(productMesh);
    
    // Add lighting
    const ambientLight = new THREE.AmbientLight(0x404040);
    const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
    directionalLight.position.set(1, 1, 1);
    scene.add(ambientLight);
    scene.add(directionalLight);
    
    // Animation loop
    function animate() {
        requestAnimationFrame(animate);
        productMesh.rotation.y += 0.01;
        renderer.render(scene, camera);
    }
    animate();
    
    // Store references for controls
    window.current3DProduct = { scene, camera, renderer, mesh: productMesh };
}

function rotate3DProduct(direction) {
    if (window.current3DProduct) {
        const rotation = direction === 'left' ? -0.2 : 0.2;
        window.current3DProduct.mesh.rotation.y += rotation;
    }
}

function zoom3DProduct(direction) {
    if (window.current3DProduct) {
        const zoom = direction === 'in' ? -0.5 : 0.5;
        window.current3DProduct.camera.position.z += zoom;
        window.current3DProduct.camera.position.z = Math.max(0.5, Math.min(5, window.current3DProduct.camera.position.z));
    }
}

function reset3DProduct() {
    if (window.current3DProduct) {
        window.current3DProduct.camera.position.set(0, 0, 2);
        window.current3DProduct.mesh.rotation.set(0, 0, 0);
    }
}

function tryOn3DProduct() {
    if (window.current3DProduct) {
        showMessage('Adding product to virtual try-on');
        closeModal('product-3d-modal');
        toggle3DTryOn();
    }
}

function view3DDetails() {
    // Show detailed product information
    showMessage('Opening detailed product view');
}

// Window resize handler for 3D scenes
window.addEventListener('resize', () => {
    if (manvue3D) {
        manvue3D.resize();
    }
});

// Initialize try-on products when modal opens
document.addEventListener('DOMContentLoaded', () => {
    // Load try-on products when the modal is first opened
    showTryOnCategory('all');
});

// Enhanced AI Chatbot System
class MANVUEAIChatbot {
    constructor() {
        this.isActive = false;
        this.messageCount = 0;
        this.sessionStartTime = Date.now();
        this.currentLanguage = 'en';
        this.responseStyle = 'friendly';
        this.typingSpeed = 50;
        this.conversationHistory = [];
        this.userProfile = null;
        this.knowledgeBase = this.initializeKnowledgeBase();
        this.aiEngine = this.initializeAIEngine();
        this.isVoiceInputActive = false;
        this.currentConversationContext = {};
        
        this.loadChatSettings();
        this.initializeWelcomeMessage();
        this.startSessionTracking();
    }

    initializeKnowledgeBase() {
        return {
            fashion: {
                styles: ['classic', 'modern', 'casual', 'bold', 'minimalist', 'street', 'formal', 'bohemian'],
                occasions: ['work', 'casual', 'formal', 'party', 'date', 'travel', 'gym', 'sleep'],
                seasons: ['spring', 'summer', 'autumn', 'winter'],
                bodyTypes: ['slim', 'athletic', 'regular', 'plus-size'],
                colorTheory: {
                    warm: ['red', 'orange', 'yellow', 'coral', 'gold'],
                    cool: ['blue', 'green', 'purple', 'silver', 'navy'],
                    neutral: ['black', 'white', 'gray', 'beige', 'brown']
                }
            },
            products: {
                categories: ['tops', 'bottoms', 'shoes', 'accessories', 'outerwear'],
                brands: products.map(p => p.brand),
                priceRanges: ['budget', 'mid-range', 'premium', 'luxury']
            },
            customer_service: {
                shipping: 'We offer free shipping on orders over £50. Standard delivery takes 3-5 business days.',
                returns: 'You can return items within 30 days for a full refund. Items must be unworn with tags.',
                sizing: 'Use our size guide or try our 3D fitting tool for accurate sizing recommendations.',
                care: 'Care instructions are provided with each item. Generally, machine wash cold and hang dry.'
            }
        };
    }

    initializeAIEngine() {
        return {
            nlp: {
                intentClassification: this.classifyIntent.bind(this),
                entityExtraction: this.extractEntities.bind(this),
                sentimentAnalysis: this.analyzeSentiment.bind(this),
                contextUnderstanding: this.understandContext.bind(this)
            },
            ml: {
                styleRecommendation: this.generateStyleRecommendations.bind(this),
                productMatching: this.findProductMatches.bind(this),
                trendAnalysis: this.analyzeTrends.bind(this),
                personalizedResponse: this.generatePersonalizedResponse.bind(this)
            }
        };
    }

    initializeWelcomeMessage() {
        const welcomeTime = document.getElementById('welcome-time');
        if (welcomeTime) {
            welcomeTime.textContent = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        }
    }

    startSessionTracking() {
        setInterval(() => {
            const duration = Math.floor((Date.now() - this.sessionStartTime) / 60000);
            const durationElement = document.getElementById('session-duration');
            if (durationElement) {
                durationElement.textContent = `${duration}m`;
            }
        }, 60000);
    }

    async processMessage(message) {
        this.messageCount++;
        this.updateMessageCount();
        
        // Add user message to history
        this.conversationHistory.push({
            role: 'user',
            content: message,
            timestamp: Date.now(),
            context: { ...this.currentConversationContext }
        });

        // Show typing indicator
        this.showTypingIndicator();

        try {
            // AI processing pipeline
            const intent = this.aiEngine.nlp.intentClassification(message);
            const entities = this.aiEngine.nlp.entityExtraction(message);
            const sentiment = this.aiEngine.nlp.sentimentAnalysis(message);
            const context = this.aiEngine.nlp.contextUnderstanding(message);

            // Generate response based on intent and context
            const response = await this.generateResponse(message, intent, entities, sentiment, context);
            
            // Add AI response to history
            this.conversationHistory.push({
                role: 'assistant',
                content: response,
                timestamp: Date.now(),
                intent: intent,
                entities: entities,
                sentiment: sentiment
            });

            // Hide typing indicator and show response
            this.hideTypingIndicator();
            await this.displayResponse(response);

        } catch (error) {
            console.error('Chat processing error:', error);
            this.hideTypingIndicator();
            this.displayErrorMessage();
        }
    }

    classifyIntent(message) {
        const lowerMessage = message.toLowerCase();
        
        // Product search intents
        if (lowerMessage.includes('search') || lowerMessage.includes('find') || lowerMessage.includes('looking for')) {
            return 'product_search';
        }
        
        // Style advice intents
        if (lowerMessage.includes('style') || lowerMessage.includes('outfit') || lowerMessage.includes('wear')) {
            return 'style_advice';
        }
        
        // Recommendation intents
        if (lowerMessage.includes('recommend') || lowerMessage.includes('suggest') || lowerMessage.includes('advice')) {
            return 'recommendation';
        }
        
        // Customer service intents
        if (lowerMessage.includes('return') || lowerMessage.includes('shipping') || lowerMessage.includes('size')) {
            return 'customer_service';
        }
        
        // Trend and fashion intents
        if (lowerMessage.includes('trend') || lowerMessage.includes('fashion') || lowerMessage.includes('popular')) {
            return 'trend_inquiry';
        }
        
        // Product information intents
        if (lowerMessage.includes('price') || lowerMessage.includes('material') || lowerMessage.includes('details')) {
            return 'product_info';
        }
        
        // Greeting intents
        if (lowerMessage.includes('hello') || lowerMessage.includes('hi') || lowerMessage.includes('hey')) {
            return 'greeting';
        }
        
        return 'general_inquiry';
    }

    extractEntities(message) {
        const entities = {
            products: [],
            colors: [],
            styles: [],
            occasions: [],
            brands: [],
            sizes: [],
            priceRange: null
        };

        const lowerMessage = message.toLowerCase();

        // Extract product categories
        this.knowledgeBase.products.categories.forEach(category => {
            if (lowerMessage.includes(category)) {
                entities.products.push(category);
            }
        });

        // Extract colors
        const colors = ['black', 'white', 'red', 'blue', 'green', 'yellow', 'orange', 'purple', 'pink', 'brown', 'gray', 'navy', 'beige'];
        colors.forEach(color => {
            if (lowerMessage.includes(color)) {
                entities.colors.push(color);
            }
        });

        // Extract styles
        this.knowledgeBase.fashion.styles.forEach(style => {
            if (lowerMessage.includes(style)) {
                entities.styles.push(style);
            }
        });

        // Extract occasions
        this.knowledgeBase.fashion.occasions.forEach(occasion => {
            if (lowerMessage.includes(occasion)) {
                entities.occasions.push(occasion);
            }
        });

        // Extract price range
        if (lowerMessage.includes('cheap') || lowerMessage.includes('budget')) {
            entities.priceRange = 'budget';
        } else if (lowerMessage.includes('expensive') || lowerMessage.includes('premium')) {
            entities.priceRange = 'premium';
        }

        return entities;
    }

    analyzeSentiment(message) {
        const positiveWords = ['love', 'like', 'great', 'awesome', 'amazing', 'perfect', 'good', 'nice', 'beautiful'];
        const negativeWords = ['hate', 'dislike', 'bad', 'awful', 'terrible', 'ugly', 'poor', 'worst'];
        
        const lowerMessage = message.toLowerCase();
        let sentiment = 'neutral';
        let score = 0;

        positiveWords.forEach(word => {
            if (lowerMessage.includes(word)) score += 1;
        });

        negativeWords.forEach(word => {
            if (lowerMessage.includes(word)) score -= 1;
        });

        if (score > 0) sentiment = 'positive';
        else if (score < 0) sentiment = 'negative';

        return { sentiment, score };
    }

    understandContext(message) {
        // Update conversation context based on current message
        const entities = this.extractEntities(message);
        
        // Merge with existing context
        Object.keys(entities).forEach(key => {
            if (entities[key] && entities[key].length > 0) {
                this.currentConversationContext[key] = entities[key];
            }
        });

        return this.currentConversationContext;
    }

    async generateResponse(message, intent, entities, sentiment, context) {
        let response = '';

        switch (intent) {
            case 'product_search':
                response = await this.handleProductSearch(message, entities);
                break;
            case 'style_advice':
                response = await this.handleStyleAdvice(message, entities, context);
                break;
            case 'recommendation':
                response = await this.handleRecommendation(message, entities, sentiment);
                break;
            case 'customer_service':
                response = this.handleCustomerService(message, entities);
                break;
            case 'trend_inquiry':
                response = this.handleTrendInquiry(message, entities);
                break;
            case 'product_info':
                response = this.handleProductInfo(message, entities);
                break;
            case 'greeting':
                response = this.handleGreeting(message, sentiment);
                break;
            default:
                response = this.handleGeneralInquiry(message, context);
        }

        return this.personalizeResponse(response, sentiment);
    }

    async handleProductSearch(message, entities) {
        let searchResults = products;

        // Filter by categories
        if (entities.products.length > 0) {
            searchResults = searchResults.filter(p => 
                entities.products.some(category => p.type === category || p.category === category)
            );
        }

        // Filter by colors
        if (entities.colors.length > 0) {
            searchResults = searchResults.filter(p => 
                entities.colors.some(color => p.name.toLowerCase().includes(color))
            );
        }

        if (searchResults.length === 0) {
            return "I couldn't find any products matching your criteria. Would you like me to suggest some alternatives or help you browse our popular items?";
        }

        const count = searchResults.length;
        const topResults = searchResults.slice(0, 3);
        
        let response = `I found ${count} products matching your search! Here are the top results:\n\n`;
        
        topResults.forEach((product, index) => {
            response += `${index + 1}. **${product.name}** - £${product.price}\n`;
            response += `   ${product.description || 'Stylish and comfortable design'}\n`;
            
            // Add matching suggestions using the matching system
            const matches = manvueProductMatcher.findMatchingProducts(product, {
                max_results: 2,
                occasion: entities.occasions.length > 0 ? entities.occasions[0] : 'casual'
            });
            
            if (matches.length > 0) {
                response += `   💡 Perfect with: ${matches[0].product.name}\n`;
            }
            response += '\n';
        });

        if (count > 3) {
            response += `And ${count - 3} more items available. Would you like me to show more or help you narrow down your search?`;
        }

        // Add interactive options
        response += `\n🔗 Want to see complete outfits? I can suggest matching items for any product!`;

        return response;
    }

    async handleStyleAdvice(message, entities, context) {
        const userStyle = this.getUserStyleProfile();
        let advice = '';

        if (entities.occasions.length > 0) {
            const occasion = entities.occasions[0];
            advice = this.getOccasionAdvice(occasion, userStyle);
        } else if (entities.styles.length > 0) {
            const style = entities.styles[0];
            advice = this.getStyleAdvice(style);
        } else {
            advice = this.getGeneralStyleAdvice(userStyle);
        }

        return advice;
    }

    getOccasionAdvice(occasion, userStyle) {
        const occasionAdvice = {
            work: "For work, I recommend a smart-casual approach. Try a well-fitted blazer with chinos or dress pants, paired with a quality button-down shirt. Add leather shoes and a minimalist watch to complete the professional look.",
            casual: "For casual outings, comfort meets style! Consider well-fitted jeans or chinos with a quality t-shirt or polo. Layer with a light jacket or cardigan, and finish with clean sneakers or casual loafers.",
            formal: "For formal events, go classic with a tailored suit in navy or charcoal gray. Pair with a crisp white dress shirt, silk tie, leather dress shoes, and minimal accessories. Quality and fit are key!",
            party: "Party time calls for statement pieces! Try a bold printed shirt or textured blazer with dark jeans. Add interesting accessories like a unique watch or stylish boots to stand out from the crowd.",
            date: "For dates, aim for smart-casual with personality. A well-fitted henley or button-down with dark jeans or chinos works great. Add a leather jacket or blazer and quality shoes to show you made an effort!"
        };

        return occasionAdvice[occasion] || "Tell me more about the specific occasion, and I'll give you targeted style advice!";
    }

    getStyleAdvice(style) {
        const styleAdvice = {
            classic: "Classic style is timeless! Focus on well-tailored pieces in neutral colors. Think white shirts, navy blazers, quality denim, and leather accessories. Invest in quality basics that never go out of style.",
            modern: "Modern style embraces clean lines and contemporary cuts. Try slim-fit pieces with interesting textures or subtle patterns. Experiment with monochromatic looks and geometric accessories.",
            casual: "Casual style is all about comfort and ease. Invest in quality basics like soft cotton tees, comfortable jeans, cozy sweaters, and versatile sneakers. Layer for dimension and interest.",
            bold: "Bold style means making statements! Don't be afraid of vibrant colors, striking patterns, or unique silhouettes. Mix textures and experiment with unexpected combinations to express your personality."
        };

        return styleAdvice[style] || "That's an interesting style choice! Tell me more about what specific elements you'd like to explore.";
    }

    handleRecommendation(message, entities, sentiment) {
        if (entities.products.length > 0) {
            return this.getProductRecommendations(entities.products[0]);
        }
        
        return "I'd love to give you personalized recommendations! What type of items are you looking for? You can also take our style quiz for customized suggestions based on your preferences.";
    }

    getProductRecommendations(category) {
        const categoryProducts = products.filter(p => p.type === category || p.category === category);
        const recommendations = categoryProducts.slice(0, 3);

        if (recommendations.length === 0) {
            return `I don't have specific ${category} recommendations right now, but I can help you explore our other categories!`;
        }

        let response = `Here are my top ${category} recommendations for you:\n\n`;
        
        recommendations.forEach((product, index) => {
            response += `${index + 1}. **${product.name}** - £${product.price}\n`;
            response += `   Rating: ${product.rating}/5 ⭐\n`;
            response += `   ${this.getProductRecommendationReason(product)}\n\n`;
        });

        response += "Would you like to see more options or get specific styling advice for any of these items?";
        
        return response;
    }

    getProductRecommendationReason(product) {
        const reasons = [
            "Highly rated by customers for quality and comfort",
            "Perfect for versatile styling and multiple occasions",
            "Great value for money with excellent craftsmanship",
            "Trending style that's perfect for the current season",
            "Classic design that works well with many outfits"
        ];
        
        return reasons[Math.floor(Math.random() * reasons.length)];
    }

    handleCustomerService(message, entities) {
        const lowerMessage = message.toLowerCase();
        
        if (lowerMessage.includes('shipping')) {
            return this.knowledgeBase.customer_service.shipping + "\n\nIs there anything specific about shipping you'd like to know more about?";
        }
        
        if (lowerMessage.includes('return')) {
            return this.knowledgeBase.customer_service.returns + "\n\nDo you need help with a specific return?";
        }
        
        if (lowerMessage.includes('size') || lowerMessage.includes('sizing')) {
            return this.knowledgeBase.customer_service.sizing + "\n\nWould you like help with sizing for a specific item?";
        }
        
        if (lowerMessage.includes('care') || lowerMessage.includes('wash')) {
            return this.knowledgeBase.customer_service.care + "\n\nDo you have questions about caring for a specific item?";
        }
        
        return "I'm here to help with any questions about orders, shipping, returns, sizing, or product care. What specific information can I provide for you?";
    }

    handleTrendInquiry(message, entities) {
        const currentTrends = [
            "Sustainable fashion and eco-friendly materials",
            "Oversized blazers and structured outerwear",
            "Earth tones and neutral color palettes",
            "Vintage-inspired denim and retro styles",
            "Minimalist accessories and clean lines",
            "Comfort-focused athleisure wear",
            "Bold patterns mixed with solid basics"
        ];

        const selectedTrends = currentTrends.slice(0, 4);
        
        let response = "Here are the hottest fashion trends right now:\n\n";
        selectedTrends.forEach((trend, index) => {
            response += `${index + 1}. ${trend}\n`;
        });
        
        response += "\nWould you like specific product recommendations for any of these trends, or styling advice on how to incorporate them into your wardrobe?";
        
        return response;
    }

    handleProductInfo(message, entities) {
        if (entities.products.length > 0) {
            const category = entities.products[0];
            const categoryProducts = products.filter(p => p.type === category);
            
            if (categoryProducts.length > 0) {
                const product = categoryProducts[0];
                return `Here's information about our ${category}:\n\n**${product.name}** - £${product.price}\n\nMaterial: High-quality cotton blend\nFit: Regular fit, true to size\nCare: Machine wash cold, hang dry\nRating: ${product.rating}/5 ⭐\n\nWould you like to know more about sizing, styling options, or see similar products?`;
            }
        }
        
        return "I'd be happy to provide product information! Which specific item or category are you interested in learning more about?";
    }

    handleGreeting(message, sentiment) {
        const greetings = [
            "Hello! I'm your MANVUE AI style assistant. How can I help you look amazing today?",
            "Hi there! Ready to discover your perfect style? I'm here to help with all things fashion!",
            "Hey! Welcome to MANVUE. Whether you need outfit advice, product recommendations, or style tips, I've got you covered!",
            "Hello! I'm excited to help you elevate your style. What fashion adventure shall we embark on today?"
        ];

        return greetings[Math.floor(Math.random() * greetings.length)];
    }

    handleGeneralInquiry(message, context) {
        return "I'm here to help with all your fashion and style needs! I can assist with:\n\n• Finding specific products\n• Style and outfit advice\n• Fashion trend insights\n• Sizing and fit guidance\n• Customer service questions\n\nWhat would you like to explore today?";
    }

    personalizeResponse(response, sentiment) {
        const style = this.responseStyle;
        
        if (style === 'friendly') {
            response = this.addFriendlyTone(response);
        } else if (style === 'professional') {
            response = this.addProfessionalTone(response);
        } else if (style === 'casual') {
            response = this.addCasualTone(response);
        }

        return response;
    }

    addFriendlyTone(response) {
        const friendlyPrefixes = ['😊 ', '✨ ', '👍 '];
        const friendlySuffixes = [' Hope this helps! 😊', ' Let me know if you need anything else! ✨', ' Happy to help! 👍'];
        
        if (Math.random() > 0.7) {
            response = friendlyPrefixes[Math.floor(Math.random() * friendlyPrefixes.length)] + response;
        }
        
        if (Math.random() > 0.7) {
            response += friendlySuffixes[Math.floor(Math.random() * friendlySuffixes.length)];
        }
        
        return response;
    }

    addProfessionalTone(response) {
        return response.replace(/I'm/g, 'I am').replace(/can't/g, 'cannot').replace(/won't/g, 'will not');
    }

    addCasualTone(response) {
        return response.replace(/I would/g, "I'd").replace(/you would/g, "you'd").replace(/cannot/g, "can't");
    }

    async displayResponse(response) {
        const typingDelay = this.calculateTypingDelay(response);
        
        setTimeout(() => {
            this.addMessage(response, 'bot');
            this.showInputSuggestions(response);
        }, typingDelay);
    }

    calculateTypingDelay(text) {
        const wordsPerMinute = this.typingSpeed;
        const words = text.split(' ').length;
        const delay = (words / wordsPerMinute) * 60 * 1000;
        return Math.min(Math.max(delay, 1000), 4000); // Between 1-4 seconds
    }

    showTypingIndicator() {
        const indicator = document.getElementById('typing-indicator');
        if (indicator) {
            indicator.classList.remove('hidden');
            this.scrollToBottom();
        }
    }

    hideTypingIndicator() {
        const indicator = document.getElementById('typing-indicator');
        if (indicator) {
            indicator.classList.add('hidden');
        }
    }

    addMessage(content, sender) {
        const messagesContainer = document.getElementById('chat-messages');
        if (!messagesContainer) return;

        const messageElement = document.createElement('div');
        messageElement.className = `chat-message ${sender}`;
        
        const currentTime = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        const senderName = sender === 'bot' ? 'MANVUE AI' : 'You';
        const avatar = sender === 'bot' ? '🤖' : '👤';

        messageElement.innerHTML = `
            <div class="message-avatar">${avatar}</div>
            <div class="message-content">
                <div class="message-header">
                    <span class="sender-name">${senderName}</span>
                    <span class="message-time">${currentTime}</span>
                </div>
                <div class="message-text">
                    ${this.formatMessageContent(content)}
                </div>
            </div>
        `;

        messagesContainer.appendChild(messageElement);
        this.scrollToBottom();
    }

    formatMessageContent(content) {
        // Convert markdown-like formatting to HTML
        content = content.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        content = content.replace(/\*(.*?)\*/g, '<em>$1</em>');
        content = content.replace(/\n\n/g, '</p><p>');
        content = content.replace(/\n/g, '<br>');
        
        if (!content.includes('<p>')) {
            content = `<p>${content}</p>`;
        }
        
        return content;
    }

    showInputSuggestions(response) {
        const suggestionsContainer = document.getElementById('input-suggestions');
        if (!suggestionsContainer) return;

        // Generate contextual suggestions based on response
        const suggestions = this.generateContextualSuggestions(response);
        
        suggestionsContainer.innerHTML = '';
        suggestions.forEach(suggestion => {
            const chip = document.createElement('div');
            chip.className = 'suggestion-chip';
            chip.textContent = suggestion;
            chip.onclick = () => this.selectSuggestion(suggestion);
            suggestionsContainer.appendChild(chip);
        });
    }

    generateContextualSuggestions(response) {
        const suggestions = [];
        
        if (response.includes('recommend') || response.includes('suggestion')) {
            suggestions.push('Show me more', 'Different style', 'Price range');
        }
        
        if (response.includes('trend')) {
            suggestions.push('How to wear this', 'Similar items', 'Color options');
        }
        
        if (response.includes('size') || response.includes('fit')) {
            suggestions.push('Size guide', '3D try-on', 'Fit advice');
        }

        // Default suggestions if none generated
        if (suggestions.length === 0) {
            suggestions.push('Style quiz', 'Trending now', 'Help me choose');
        }
        
        return suggestions.slice(0, 3);
    }

    selectSuggestion(suggestion) {
        const input = document.getElementById('chat-input');
        if (input) {
            input.value = suggestion;
            this.sendMessage();
        }
    }

    scrollToBottom() {
        const messagesContainer = document.getElementById('chat-messages');
        if (messagesContainer) {
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
    }

    updateMessageCount() {
        const countElement = document.getElementById('message-count');
        if (countElement) {
            countElement.textContent = this.messageCount;
        }
    }

    displayErrorMessage() {
        this.addMessage("I apologize, but I'm experiencing some technical difficulties. Please try again in a moment, or feel free to browse our products while I get back online! 🔧", 'bot');
    }

    getUserStyleProfile() {
        // Get user style profile from localStorage or return default
        const profile = localStorage.getItem('manvue-style-profile');
        return profile ? JSON.parse(profile) : { style: 'modern', preferences: [] };
    }

    // Settings management
    loadChatSettings() {
        const settings = localStorage.getItem('manvue-chat-settings');
        if (settings) {
            const parsed = JSON.parse(settings);
            this.currentLanguage = parsed.language || 'en';
            this.responseStyle = parsed.responseStyle || 'friendly';
            this.typingSpeed = parsed.typingSpeed || 50;
            
            this.updateSettingsUI();
        }
    }

    saveChatSettings() {
        const settings = {
            language: this.currentLanguage,
            responseStyle: this.responseStyle,
            typingSpeed: this.typingSpeed
        };
        localStorage.setItem('manvue-chat-settings', JSON.stringify(settings));
    }

    updateSettingsUI() {
        const langSelect = document.getElementById('chat-language');
        const styleSelect = document.getElementById('response-style');
        const speedSlider = document.getElementById('typing-speed');

        if (langSelect) langSelect.value = this.currentLanguage;
        if (styleSelect) styleSelect.value = this.responseStyle;
        if (speedSlider) speedSlider.value = this.typingSpeed;
    }
}

// Cross-Category Product Matching System
class MANVUEProductMatcher {
    constructor() {
        this.compatibilityMatrix = this.initializeCompatibilityMatrix();
        this.colorHarmonyRules = this.initializeColorHarmony();
        this.styleCoherenceRules = this.initializeStyleCoherence();
        this.seasonalRules = this.initializeSeasonalRules();
        this.occasionRules = this.initializeOccasionRules();
        this.matchingHistory = [];
        this.userPreferences = this.loadUserPreferences();
        
        this.initializeMatchingEngine();
    }

    initializeCompatibilityMatrix() {
        return {
            // Category compatibility scores (0-1, where 1 is perfect match)
            categories: {
                'casual-shirt': {
                    'jeans': 0.95,
                    'chinos': 0.90,
                    'shorts': 0.85,
                    'sneakers': 0.90,
                    'casual-shoes': 0.85,
                    'watch': 0.80,
                    'jacket': 0.75,
                    'hoodie': 0.70
                },
                'dress-shirt': {
                    'dress-pants': 0.95,
                    'chinos': 0.85,
                    'suit-jacket': 0.98,
                    'blazer': 0.90,
                    'dress-shoes': 0.95,
                    'tie': 0.90,
                    'watch': 0.85,
                    'belt': 0.90
                },
                'polo': {
                    'chinos': 0.95,
                    'jeans': 0.80,
                    'shorts': 0.90,
                    'sneakers': 0.85,
                    'casual-shoes': 0.90,
                    'watch': 0.75
                },
                't-shirt': {
                    'jeans': 0.95,
                    'shorts': 0.90,
                    'chinos': 0.80,
                    'sneakers': 0.95,
                    'casual-shoes': 0.75,
                    'hoodie': 0.85,
                    'jacket': 0.70
                },
                'blazer': {
                    'dress-shirt': 0.90,
                    'polo': 0.75,
                    'chinos': 0.90,
                    'dress-pants': 0.95,
                    'dress-shoes': 0.90,
                    'casual-shoes': 0.70
                },
                'jeans': {
                    'casual-shirt': 0.95,
                    't-shirt': 0.95,
                    'polo': 0.80,
                    'sneakers': 0.90,
                    'casual-shoes': 0.85,
                    'boots': 0.80
                },
                'chinos': {
                    'dress-shirt': 0.85,
                    'casual-shirt': 0.90,
                    'polo': 0.95,
                    'blazer': 0.90,
                    'dress-shoes': 0.85,
                    'casual-shoes': 0.90,
                    'sneakers': 0.80
                }
            },
            // Style compatibility
            styles: {
                'casual': ['t-shirt', 'jeans', 'sneakers', 'hoodie', 'casual-shirt'],
                'business-casual': ['polo', 'chinos', 'blazer', 'dress-shirt', 'casual-shoes'],
                'formal': ['dress-shirt', 'suit-jacket', 'dress-pants', 'dress-shoes', 'tie'],
                'smart-casual': ['casual-shirt', 'chinos', 'blazer', 'casual-shoes', 'watch'],
                'athletic': ['t-shirt', 'shorts', 'sneakers', 'hoodie', 'trackpants']
            }
        };
    }

    initializeColorHarmony() {
        return {
            // Color harmony rules based on color theory
            complementary: {
                'navy': ['white', 'cream', 'light-blue', 'gray', 'tan'],
                'black': ['white', 'gray', 'red', 'blue', 'silver'],
                'white': ['navy', 'black', 'gray', 'blue', 'brown'],
                'gray': ['white', 'black', 'navy', 'burgundy', 'blue'],
                'brown': ['cream', 'white', 'tan', 'orange', 'gold'],
                'blue': ['white', 'cream', 'gray', 'brown', 'navy'],
                'red': ['white', 'black', 'gray', 'navy', 'cream'],
                'green': ['white', 'cream', 'brown', 'tan', 'navy']
            },
            // Seasonal color preferences
            seasonal: {
                'spring': ['light-blue', 'cream', 'light-gray', 'soft-green', 'white'],
                'summer': ['white', 'light-blue', 'cream', 'tan', 'light-gray'],
                'autumn': ['brown', 'burgundy', 'orange', 'dark-green', 'tan'],
                'winter': ['navy', 'black', 'gray', 'burgundy', 'dark-blue']
            },
            // Neutral colors that work with everything
            neutrals: ['white', 'black', 'gray', 'navy', 'cream', 'tan', 'brown'],
            // Colors to avoid together
            clashing: [
                ['red', 'pink'],
                ['orange', 'red'],
                ['purple', 'green'],
                ['brown', 'black']
            ]
        };
    }

    initializeStyleCoherence() {
        return {
            // Style coherence rules
            coherent_combinations: {
                'minimalist': {
                    colors: ['white', 'black', 'gray', 'navy'],
                    patterns: ['solid', 'subtle'],
                    fit: ['slim', 'tailored'],
                    materials: ['cotton', 'wool', 'linen']
                },
                'classic': {
                    colors: ['navy', 'white', 'gray', 'brown'],
                    patterns: ['solid', 'stripes', 'checks'],
                    fit: ['regular', 'tailored'],
                    materials: ['cotton', 'wool', 'leather']
                },
                'modern': {
                    colors: ['black', 'white', 'gray', 'blue'],
                    patterns: ['solid', 'geometric'],
                    fit: ['slim', 'modern'],
                    materials: ['cotton', 'synthetic', 'tech-fabric']
                },
                'casual': {
                    colors: ['blue', 'gray', 'green', 'brown'],
                    patterns: ['solid', 'casual-stripes', 'prints'],
                    fit: ['regular', 'relaxed'],
                    materials: ['cotton', 'denim', 'jersey']
                }
            },
            // Pattern mixing rules
            pattern_mixing: {
                'solid': ['stripes', 'checks', 'dots', 'prints'],
                'stripes': ['solid', 'small-checks'],
                'checks': ['solid', 'small-stripes'],
                'dots': ['solid', 'stripes'],
                'prints': ['solid']
            }
        };
    }

    initializeSeasonalRules() {
        return {
            spring: {
                preferred_materials: ['cotton', 'linen', 'light-wool'],
                colors: ['light-blue', 'cream', 'soft-green', 'white', 'light-gray'],
                categories: ['light-jacket', 'chinos', 'polo', 'casual-shirt'],
                avoid: ['heavy-coat', 'thick-sweater', 'dark-colors']
            },
            summer: {
                preferred_materials: ['cotton', 'linen', 'breathable-synthetic'],
                colors: ['white', 'light-blue', 'cream', 'tan', 'pastels'],
                categories: ['t-shirt', 'shorts', 'polo', 'light-shirt', 'sandals'],
                avoid: ['heavy-materials', 'dark-colors', 'long-pants']
            },
            autumn: {
                preferred_materials: ['wool', 'cotton', 'cashmere', 'leather'],
                colors: ['brown', 'burgundy', 'orange', 'dark-green', 'navy'],
                categories: ['sweater', 'jacket', 'boots', 'scarf', 'long-pants'],
                avoid: ['light-materials', 'pastels', 'shorts']
            },
            winter: {
                preferred_materials: ['wool', 'cashmere', 'heavy-cotton', 'synthetic-insulation'],
                colors: ['navy', 'black', 'gray', 'burgundy', 'dark-colors'],
                categories: ['coat', 'sweater', 'boots', 'scarf', 'gloves'],
                avoid: ['light-materials', 'light-colors', 'open-shoes']
            }
        };
    }

    initializeOccasionRules() {
        return {
            work: {
                required: ['dress-shirt', 'dress-pants', 'dress-shoes'],
                optional: ['blazer', 'tie', 'watch', 'belt'],
                avoid: ['shorts', 'sandals', 't-shirt', 'sneakers'],
                style_preference: 'formal'
            },
            casual: {
                preferred: ['t-shirt', 'jeans', 'sneakers', 'casual-shirt'],
                optional: ['hoodie', 'jacket', 'watch'],
                avoid: ['tie', 'dress-shoes', 'formal-suit'],
                style_preference: 'casual'
            },
            date: {
                preferred: ['casual-shirt', 'chinos', 'casual-shoes', 'blazer'],
                optional: ['watch', 'cologne', 'nice-belt'],
                avoid: ['gym-wear', 'overly-formal', 'wrinkled-clothes'],
                style_preference: 'smart-casual'
            },
            party: {
                preferred: ['dress-shirt', 'dark-jeans', 'nice-shoes', 'blazer'],
                optional: ['watch', 'cologne', 'unique-accessory'],
                avoid: ['overly-casual', 'gym-wear', 'work-clothes'],
                style_preference: 'smart-casual'
            },
            gym: {
                required: ['athletic-shirt', 'shorts', 'athletic-shoes'],
                optional: ['hoodie', 'water-bottle', 'headphones'],
                avoid: ['dress-clothes', 'jeans', 'dress-shoes'],
                style_preference: 'athletic'
            }
        };
    }

    initializeMatchingEngine() {
        console.log('🔗 Product Matching Engine Initialized');
        this.preprocessProducts();
    }

    preprocessProducts() {
        // Add matching metadata to products
        products.forEach(product => {
            product.matchingData = {
                primaryColor: this.extractPrimaryColor(product),
                secondaryColors: this.extractSecondaryColors(product),
                style: this.categorizeStyle(product),
                season: this.determineSeason(product),
                formality: this.assessFormality(product),
                versatility: this.calculateVersatility(product),
                categories: this.extractCategories(product)
            };
        });
    }

    extractPrimaryColor(product) {
        const name = product.name.toLowerCase();
        const colorMap = {
            'white': ['white', 'cream', 'ivory'],
            'black': ['black', 'charcoal'],
            'navy': ['navy', 'dark blue'],
            'blue': ['blue', 'light blue'],
            'gray': ['gray', 'grey', 'silver'],
            'brown': ['brown', 'tan', 'beige'],
            'red': ['red', 'burgundy', 'maroon'],
            'green': ['green', 'olive', 'forest']
        };

        for (const [color, variants] of Object.entries(colorMap)) {
            if (variants.some(variant => name.includes(variant))) {
                return color;
            }
        }
        return 'neutral';
    }

    extractSecondaryColors(product) {
        // Extract any secondary colors mentioned in the product name or description
        const colors = [];
        const colorKeywords = ['stripe', 'check', 'pattern', 'trim', 'accent'];
        
        colorKeywords.forEach(keyword => {
            if (product.name.toLowerCase().includes(keyword)) {
                colors.push('accent');
            }
        });
        
        return colors;
    }

    categorizeStyle(product) {
        const name = product.name.toLowerCase();
        const type = product.type.toLowerCase();
        
        // Style categorization based on product name and type
        if (name.includes('dress') || name.includes('formal') || type.includes('dress')) {
            return 'formal';
        } else if (name.includes('casual') || type.includes('casual')) {
            return 'casual';
        } else if (name.includes('business') || name.includes('professional')) {
            return 'business-casual';
        } else if (name.includes('sport') || name.includes('athletic')) {
            return 'athletic';
        } else {
            return 'smart-casual';
        }
    }

    determineSeason(product) {
        const name = product.name.toLowerCase();
        const seasonKeywords = {
            'summer': ['shorts', 'tank', 'linen', 'light', 'breathable'],
            'winter': ['coat', 'sweater', 'wool', 'heavy', 'thermal'],
            'spring': ['light jacket', 'cardigan', 'transition'],
            'autumn': ['jacket', 'boots', 'layers']
        };

        for (const [season, keywords] of Object.entries(seasonKeywords)) {
            if (keywords.some(keyword => name.includes(keyword))) {
                return season;
            }
        }
        return 'all-season';
    }

    assessFormality(product) {
        const formalKeywords = ['dress', 'suit', 'formal', 'business', 'professional'];
        const casualKeywords = ['casual', 'relaxed', 'everyday', 'comfort'];
        
        const name = product.name.toLowerCase();
        
        if (formalKeywords.some(keyword => name.includes(keyword))) {
            return 0.8; // High formality
        } else if (casualKeywords.some(keyword => name.includes(keyword))) {
            return 0.2; // Low formality
        } else {
            return 0.5; // Medium formality
        }
    }

    calculateVersatility(product) {
        const type = product.type.toLowerCase();
        const name = product.name.toLowerCase();
        
        // Versatile items score higher
        const versatileTypes = ['shirt', 'jeans', 'chinos', 'blazer', 'watch'];
        const versatileColors = ['white', 'navy', 'gray', 'black'];
        
        let score = 0.5; // Base score
        
        if (versatileTypes.some(type_keyword => type.includes(type_keyword))) {
            score += 0.2;
        }
        
        if (versatileColors.some(color => name.includes(color))) {
            score += 0.2;
        }
        
        if (name.includes('classic') || name.includes('basic')) {
            score += 0.1;
        }
        
        return Math.min(score, 1.0);
    }

    extractCategories(product) {
        // Extract all relevant categories for matching
        const categories = [product.type, product.category];
        
        // Add sub-categories based on product name
        const name = product.name.toLowerCase();
        if (name.includes('dress')) categories.push('dress-item');
        if (name.includes('casual')) categories.push('casual-item');
        if (name.includes('formal')) categories.push('formal-item');
        
        return categories.filter(cat => cat && cat.length > 0);
    }

    // Main matching algorithm
    findMatchingProducts(baseProduct, options = {}) {
        const {
            occasion = 'casual',
            season = 'all-season',
            style_preference = null,
            max_results = 10,
            exclude_categories = [],
            color_harmony = true,
            budget_range = null
        } = options;

        let matches = [];
        
        products.forEach(candidate => {
            if (candidate.id === baseProduct.id) return; // Skip same product
            
            const matchScore = this.calculateMatchScore(baseProduct, candidate, {
                occasion,
                season,
                style_preference,
                color_harmony
            });
            
            if (matchScore > 0.3) { // Minimum threshold
                matches.push({
                    product: candidate,
                    score: matchScore,
                    reasons: this.getMatchingReasons(baseProduct, candidate),
                    compatibility_type: this.getCompatibilityType(baseProduct, candidate)
                });
            }
        });

        // Sort by score and apply filters
        matches.sort((a, b) => b.score - a.score);
        
        // Apply filters
        if (exclude_categories.length > 0) {
            matches = matches.filter(match => 
                !exclude_categories.some(cat => 
                    match.product.type.includes(cat) || 
                    match.product.category.includes(cat)
                )
            );
        }
        
        if (budget_range) {
            matches = matches.filter(match => 
                match.product.price >= budget_range.min && 
                match.product.price <= budget_range.max
            );
        }
        
        return matches.slice(0, max_results);
    }

    calculateMatchScore(baseProduct, candidate, options) {
        let score = 0;
        const weights = {
            category_compatibility: 0.25,
            color_harmony: 0.20,
            style_coherence: 0.20,
            seasonal_appropriateness: 0.15,
            occasion_suitability: 0.10,
            versatility: 0.10
        };

        // Category compatibility
        const categoryScore = this.getCategoryCompatibility(baseProduct, candidate);
        score += categoryScore * weights.category_compatibility;

        // Color harmony
        if (options.color_harmony) {
            const colorScore = this.getColorHarmonyScore(baseProduct, candidate);
            score += colorScore * weights.color_harmony;
        }

        // Style coherence
        const styleScore = this.getStyleCoherenceScore(baseProduct, candidate, options.style_preference);
        score += styleScore * weights.style_coherence;

        // Seasonal appropriateness
        const seasonScore = this.getSeasonalScore(candidate, options.season);
        score += seasonScore * weights.seasonal_appropriateness;

        // Occasion suitability
        const occasionScore = this.getOccasionScore(candidate, options.occasion);
        score += occasionScore * weights.occasion_suitability;

        // Versatility bonus
        const versatilityScore = candidate.matchingData?.versatility || 0.5;
        score += versatilityScore * weights.versatility;

        return Math.min(score, 1.0);
    }

    getCategoryCompatibility(baseProduct, candidate) {
        const baseType = baseProduct.type.toLowerCase();
        const candidateType = candidate.type.toLowerCase();
        
        // Check direct compatibility from matrix
        if (this.compatibilityMatrix.categories[baseType]?.[candidateType]) {
            return this.compatibilityMatrix.categories[baseType][candidateType];
        }
        
        // Check reverse compatibility
        if (this.compatibilityMatrix.categories[candidateType]?.[baseType]) {
            return this.compatibilityMatrix.categories[candidateType][baseType];
        }
        
        // Default compatibility for same style family
        const baseStyle = baseProduct.matchingData?.style;
        const candidateStyle = candidate.matchingData?.style;
        
        if (baseStyle === candidateStyle) {
            return 0.6;
        }
        
        return 0.3; // Low but not zero compatibility
    }

    getColorHarmonyScore(baseProduct, candidate) {
        const baseColor = baseProduct.matchingData?.primaryColor || 'neutral';
        const candidateColor = candidate.matchingData?.primaryColor || 'neutral';
        
        // Perfect match for same color
        if (baseColor === candidateColor) {
            return 0.8;
        }
        
        // Check complementary colors
        if (this.colorHarmonyRules.complementary[baseColor]?.includes(candidateColor)) {
            return 0.9;
        }
        
        // Check if both are neutrals
        if (this.colorHarmonyRules.neutrals.includes(baseColor) && 
            this.colorHarmonyRules.neutrals.includes(candidateColor)) {
            return 0.85;
        }
        
        // Check for clashing colors
        const isClashing = this.colorHarmonyRules.clashing.some(clash => 
            (clash.includes(baseColor) && clash.includes(candidateColor))
        );
        
        if (isClashing) {
            return 0.1;
        }
        
        return 0.5; // Neutral compatibility
    }

    getStyleCoherenceScore(baseProduct, candidate, stylePreference) {
        const baseStyle = baseProduct.matchingData?.style;
        const candidateStyle = candidate.matchingData?.style;
        
        // Perfect match for same style
        if (baseStyle === candidateStyle) {
            return 0.9;
        }
        
        // Check style preference override
        if (stylePreference && candidateStyle === stylePreference) {
            return 0.8;
        }
        
        // Compatible style combinations
        const compatibleStyles = {
            'formal': ['business-casual'],
            'business-casual': ['formal', 'smart-casual'],
            'smart-casual': ['business-casual', 'casual'],
            'casual': ['smart-casual']
        };
        
        if (compatibleStyles[baseStyle]?.includes(candidateStyle)) {
            return 0.7;
        }
        
        return 0.4; // Low but acceptable compatibility
    }

    getSeasonalScore(product, season) {
        if (season === 'all-season') return 0.8;
        
        const productSeason = product.matchingData?.season;
        
        if (productSeason === season) {
            return 1.0;
        }
        
        if (productSeason === 'all-season') {
            return 0.8;
        }
        
        // Adjacent seasons get partial credit
        const seasonAdjacency = {
            'spring': ['summer'],
            'summer': ['spring', 'autumn'],
            'autumn': ['summer', 'winter'],
            'winter': ['autumn']
        };
        
        if (seasonAdjacency[season]?.includes(productSeason)) {
            return 0.6;
        }
        
        return 0.3;
    }

    getOccasionScore(product, occasion) {
        const rules = this.occasionRules[occasion];
        if (!rules) return 0.5;
        
        const productType = product.type.toLowerCase();
        
        // Check if required item
        if (rules.required && rules.required.includes(productType)) {
            return 1.0;
        }
        
        // Check if preferred item
        if (rules.preferred && rules.preferred.includes(productType)) {
            return 0.9;
        }
        
        // Check if optional item
        if (rules.optional && rules.optional.includes(productType)) {
            return 0.7;
        }
        
        // Check if should be avoided
        if (rules.avoid && rules.avoid.includes(productType)) {
            return 0.1;
        }
        
        return 0.5; // Neutral
    }

    getMatchingReasons(baseProduct, candidate) {
        const reasons = [];
        
        // Category compatibility
        const categoryScore = this.getCategoryCompatibility(baseProduct, candidate);
        if (categoryScore > 0.7) {
            reasons.push('Excellent category compatibility');
        } else if (categoryScore > 0.5) {
            reasons.push('Good category match');
        }
        
        // Color harmony
        const colorScore = this.getColorHarmonyScore(baseProduct, candidate);
        if (colorScore > 0.8) {
            reasons.push('Perfect color harmony');
        } else if (colorScore > 0.6) {
            reasons.push('Complementary colors');
        }
        
        // Style coherence
        const baseStyle = baseProduct.matchingData?.style;
        const candidateStyle = candidate.matchingData?.style;
        if (baseStyle === candidateStyle) {
            reasons.push('Same style family');
        }
        
        // Versatility
        const versatility = candidate.matchingData?.versatility || 0;
        if (versatility > 0.7) {
            reasons.push('Highly versatile piece');
        }
        
        return reasons;
    }

    getCompatibilityType(baseProduct, candidate) {
        const baseType = baseProduct.type.toLowerCase();
        const candidateType = candidate.type.toLowerCase();
        
        const topBottomTypes = ['shirt', 'polo', 't-shirt', 'sweater', 'blazer'];
        const bottomTypes = ['jeans', 'chinos', 'pants', 'shorts'];
        const shoeTypes = ['shoes', 'sneakers', 'boots'];
        const accessoryTypes = ['watch', 'belt', 'tie', 'bag'];
        
        if (topBottomTypes.some(type => baseType.includes(type)) && 
            bottomTypes.some(type => candidateType.includes(type))) {
            return 'top-bottom';
        }
        
        if (bottomTypes.some(type => baseType.includes(type)) && 
            shoeTypes.some(type => candidateType.includes(type))) {
            return 'bottom-shoes';
        }
        
        if (accessoryTypes.some(type => candidateType.includes(type))) {
            return 'accessory';
        }
        
        return 'general';
    }

    // Generate complete outfits
    generateCompleteOutfit(baseProduct, options = {}) {
        const {
            occasion = 'casual',
            season = 'all-season',
            budget_limit = null,
            style_preference = null
        } = options;

        const outfit = {
            base: baseProduct,
            matches: {},
            total_price: baseProduct.price,
            style_score: 0,
            completeness: 0
        };

        const requiredCategories = this.getRequiredCategories(occasion);
        const optionalCategories = this.getOptionalCategories(occasion);
        
        // Find matches for each required category
        requiredCategories.forEach(category => {
            if (baseProduct.type.toLowerCase() === category) return; // Skip if base product
            
            const matches = this.findMatchingProducts(baseProduct, {
                occasion,
                season,
                style_preference,
                max_results: 3,
                exclude_categories: Object.keys(outfit.matches)
            }).filter(match => match.product.type.toLowerCase() === category);
            
            if (matches.length > 0) {
                const bestMatch = matches[0];
                outfit.matches[category] = bestMatch;
                outfit.total_price += bestMatch.product.price;
            }
        });

        // Add optional items if budget allows
        if (!budget_limit || outfit.total_price < budget_limit) {
            optionalCategories.forEach(category => {
                if (outfit.matches[category] || baseProduct.type.toLowerCase() === category) return;
                
                const remainingBudget = budget_limit ? budget_limit - outfit.total_price : null;
                
                const matches = this.findMatchingProducts(baseProduct, {
                    occasion,
                    season,
                    style_preference,
                    max_results: 3,
                    exclude_categories: Object.keys(outfit.matches),
                    budget_range: remainingBudget ? { min: 0, max: remainingBudget } : null
                }).filter(match => match.product.type.toLowerCase() === category);
                
                if (matches.length > 0) {
                    const bestMatch = matches[0];
                    outfit.matches[category] = bestMatch;
                    outfit.total_price += bestMatch.product.price;
                }
            });
        }

        // Calculate outfit metrics
        outfit.style_score = this.calculateOutfitStyleScore(outfit);
        outfit.completeness = this.calculateOutfitCompleteness(outfit, requiredCategories);
        
        return outfit;
    }

    getRequiredCategories(occasion) {
        const rules = this.occasionRules[occasion];
        return rules?.required || [];
    }

    getOptionalCategories(occasion) {
        const rules = this.occasionRules[occasion];
        return rules?.optional || [];
    }

    calculateOutfitStyleScore(outfit) {
        let totalScore = 0;
        let itemCount = 1; // Base product
        
        Object.values(outfit.matches).forEach(match => {
            totalScore += match.score;
            itemCount++;
        });
        
        return totalScore / itemCount;
    }

    calculateOutfitCompleteness(outfit, requiredCategories) {
        const presentCategories = [outfit.base.type.toLowerCase()];
        Object.keys(outfit.matches).forEach(category => {
            presentCategories.push(category);
        });
        
        const requiredPresent = requiredCategories.filter(cat => 
            presentCategories.includes(cat)
        ).length;
        
        return requiredCategories.length > 0 ? requiredPresent / requiredCategories.length : 1.0;
    }

    // User preference learning
    saveUserPreference(interaction) {
        this.matchingHistory.push({
            ...interaction,
            timestamp: Date.now()
        });
        
        // Save to localStorage
        localStorage.setItem('manvue-matching-history', JSON.stringify(this.matchingHistory));
        
        // Update user preferences
        this.updateUserPreferences();
    }

    loadUserPreferences() {
        const saved = localStorage.getItem('manvue-matching-history');
        if (saved) {
            this.matchingHistory = JSON.parse(saved);
        }
        
        return this.extractUserPreferences();
    }

    extractUserPreferences() {
        const preferences = {
            preferred_styles: {},
            preferred_colors: {},
            preferred_occasions: {},
            budget_patterns: [],
            category_preferences: {}
        };
        
        this.matchingHistory.forEach(interaction => {
            // Extract patterns from user interactions
            if (interaction.style) {
                preferences.preferred_styles[interaction.style] = 
                    (preferences.preferred_styles[interaction.style] || 0) + 1;
            }
            
            if (interaction.colors) {
                interaction.colors.forEach(color => {
                    preferences.preferred_colors[color] = 
                        (preferences.preferred_colors[color] || 0) + 1;
                });
            }
        });
        
        return preferences;
    }

    updateUserPreferences() {
        this.userPreferences = this.extractUserPreferences();
    }
}

// Initialize product matcher
const manvueProductMatcher = new MANVUEProductMatcher();

// Initialize enhanced chatbot
const manvueAI = new MANVUEAIChatbot();

// Enhanced chatbot interface functions
function toggleChatSettings() {
    const settings = document.getElementById('chat-settings');
    if (settings) {
        settings.classList.toggle('hidden');
    }
}

function clearChatHistory() {
    const messagesContainer = document.getElementById('chat-messages');
    if (messagesContainer) {
        // Keep welcome message, clear the rest
        const welcomeMessage = messagesContainer.querySelector('.chat-message.bot');
        messagesContainer.innerHTML = '';
        if (welcomeMessage) {
            messagesContainer.appendChild(welcomeMessage);
        }
    }
    
    manvueAI.conversationHistory = [];
    manvueAI.messageCount = 0;
    manvueAI.updateMessageCount();
    
    showMessage('Chat history cleared');
}

function updateChatLanguage() {
    const language = document.getElementById('chat-language').value;
    manvueAI.currentLanguage = language;
    manvueAI.saveChatSettings();
    showMessage(`Language changed to ${language}`);
}

function updateResponseStyle() {
    const style = document.getElementById('response-style').value;
    manvueAI.responseStyle = style;
    manvueAI.saveChatSettings();
    showMessage(`Response style changed to ${style}`);
}

function updateTypingSpeed() {
    const speed = document.getElementById('typing-speed').value;
    manvueAI.typingSpeed = parseInt(speed);
    manvueAI.saveChatSettings();
}

function toggleVoiceInput() {
    if (manvueAI.isVoiceInputActive) {
        // Stop voice input
        manvueAI.isVoiceInputActive = false;
        showMessage('Voice input disabled');
    } else {
        // Start voice input
        if (manvueVoice && manvueVoice.recognition) {
            manvueAI.isVoiceInputActive = true;
            manvueVoice.startListening();
            showMessage('Voice input enabled - speak your message');
        } else {
            showMessage('Voice recognition not available');
        }
    }
}

function attachFile() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*';
    input.onchange = function(e) {
        const file = e.target.files[0];
        if (file) {
            // Simulate image analysis
            showMessage('Image uploaded! Analyzing your style preferences...');
            setTimeout(() => {
                manvueAI.addMessage('I can see you have great taste! Based on your image, I recommend checking out our modern casual collection. Would you like me to show you some specific items?', 'bot');
            }, 2000);
        }
    };
    input.click();
}

function sendMessage() {
    const input = document.getElementById('chat-input');
    if (!input) return;

    const message = input.value.trim();
    if (!message) return;

    // Add user message immediately
    manvueAI.addMessage(message, 'user');
    input.value = '';

    // Clear suggestions
    const suggestionsContainer = document.getElementById('input-suggestions');
    if (suggestionsContainer) {
        suggestionsContainer.innerHTML = '';
    }

    // Process message with AI
    manvueAI.processMessage(message);
}

function toggleQuickActions() {
    const grid = document.getElementById('quick-actions-grid');
    const toggle = document.getElementById('quick-actions-toggle');
    
    if (grid && toggle) {
        grid.classList.toggle('collapsed');
        toggle.textContent = grid.classList.contains('collapsed') ? '▲' : '▼';
        toggle.style.transform = grid.classList.contains('collapsed') ? 'rotate(180deg)' : 'rotate(0deg)';
    }
}

function showSuggestions() {
    const suggestions = [
        "What's trending now?",
        "Help me build an outfit",
        "Show me casual wear",
        "I need work clothes",
        "What suits my body type?",
        "Seasonal recommendations"
    ];
    
    let response = "Here are some popular topics I can help you with:\n\n";
    suggestions.forEach((suggestion, index) => {
        response += `${index + 1}. ${suggestion}\n`;
    });
    response += "\nJust click on any suggestion or type your own question!";
    
    manvueAI.addMessage(response, 'bot');
}

function startTour() {
    const tourSteps = [
        "Welcome to MANVUE! Let me show you around. 🎯",
        "You can ask me anything about fashion, style, or our products using natural language. 💬",
        "Use the quick action buttons below for common tasks like style quizzes and recommendations. ⚡",
        "Try our 3D virtual try-on system for a realistic fitting experience. 🎮",
        "I can understand voice commands too - just click the microphone button! 🎤",
        "Ready to start your style journey? Ask me anything! ✨"
    ];
    
    tourSteps.forEach((step, index) => {
        setTimeout(() => {
            manvueAI.addMessage(step, 'bot');
        }, index * 2000);
    });
}

// New quick action functions
function getPersonalShopper() {
    manvueAI.addMessage("I'm your personal AI shopper! Tell me about your style preferences, budget, and what you're looking for, and I'll curate the perfect selection just for you. What's your ideal outfit vision?", 'bot');
}

function getStyleTips() {
    const tips = [
        "🎯 **Fit is everything** - Well-fitted clothes instantly elevate your look",
        "🎨 **Master color coordination** - Start with neutrals and add one accent color",
        "👔 **Invest in basics** - Quality white shirts, dark jeans, and blazers are versatile",
        "👞 **Good shoes matter** - They can make or break an outfit",
        "🧥 **Layer thoughtfully** - Layers add depth and sophistication to any look",
        "⌚ **Accessorize wisely** - A watch, belt, or bag can complete your style"
    ];
    
    let response = "Here are my top style tips for modern men:\n\n";
    tips.forEach(tip => {
        response += tip + "\n\n";
    });
    response += "Would you like specific advice on any of these areas?";
    
    manvueAI.addMessage(response, 'bot');
}

function askAboutProduct() {
    manvueAI.addMessage("I'm here to help with any product questions! You can ask me about:\n\n• Sizing and fit\n• Materials and care instructions\n• Styling suggestions\n• Price comparisons\n• Availability and shipping\n\nWhat would you like to know about a specific item?", 'bot');
}

function getCustomerSupport() {
    manvueAI.addMessage("I'm here to provide comprehensive customer support! I can help you with:\n\n🚚 **Shipping & Delivery** - Tracking, timing, and options\n🔄 **Returns & Exchanges** - Easy return process\n📏 **Sizing Help** - Size guides and fit advice\n💳 **Payment & Orders** - Order status and payment options\n🛡️ **Product Care** - Care instructions and maintenance\n\nWhat can I assist you with today?", 'bot');
}

// Enhanced sendChatMessage to work with new system
function sendChatMessage() {
    sendMessage();
}

// Cross-Category Product Matching Interface Functions
function showProductMatches(productId) {
    const product = products.find(p => p.id === productId);
    if (!product) return;

    const matches = manvueProductMatcher.findMatchingProducts(product, {
        occasion: 'casual',
        season: getCurrentSeason(),
        max_results: 6
    });

    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.id = 'product-matches-modal';
    
    modal.innerHTML = `
        <div class="modal-content large">
            <div class="modal-header">
                <h3>🔗 Perfect Matches for ${product.name}</h3>
                <button onclick="closeModal('product-matches-modal')">✕</button>
            </div>
            
            <div class="matches-content">
                <div class="base-product">
                    <h4>Base Item</h4>
                    <div class="product-card mini">
                        <img src="${product.image}" alt="${product.name}">
                        <h5>${product.name}</h5>
                        <p class="price">£${product.price}</p>
                    </div>
                </div>
                
                <div class="matching-options">
                    <div class="match-controls">
                        <div class="control-group">
                            <label>Occasion</label>
                            <select id="match-occasion" onchange="updateMatches('${product.id}')">
                                <option value="casual">Casual</option>
                                <option value="work">Work</option>
                                <option value="date">Date</option>
                                <option value="party">Party</option>
                                <option value="gym">Gym</option>
                            </select>
                        </div>
                        <div class="control-group">
                            <label>Season</label>
                            <select id="match-season" onchange="updateMatches('${product.id}')">
                                <option value="all-season">All Season</option>
                                <option value="spring">Spring</option>
                                <option value="summer">Summer</option>
                                <option value="autumn">Autumn</option>
                                <option value="winter">Winter</option>
                            </select>
                        </div>
                        <div class="control-group">
                            <label>Style</label>
                            <select id="match-style" onchange="updateMatches('${product.id}')">
                                <option value="">Auto</option>
                                <option value="casual">Casual</option>
                                <option value="formal">Formal</option>
                                <option value="smart-casual">Smart Casual</option>
                                <option value="business-casual">Business Casual</option>
                            </select>
                        </div>
                    </div>
                    
                    <div class="matches-grid" id="matches-grid">
                        ${renderMatches(matches)}
                    </div>
                </div>
                
                <div class="outfit-actions">
                    <button class="btn-primary" onclick="generateCompleteOutfit('${product.id}')">
                        👔 Generate Complete Outfit
                    </button>
                    <button class="btn-secondary" onclick="saveMatchingPreferences('${product.id}')">
                        💾 Save Preferences
                    </button>
                </div>
            </div>
        </div>
    `;

    document.body.appendChild(modal);
    modal.style.display = 'flex';
}

function renderMatches(matches) {
    if (matches.length === 0) {
        return '<div class="no-matches">No suitable matches found. Try adjusting your preferences.</div>';
    }

    return matches.map(match => `
        <div class="match-card" data-score="${(match.score * 100).toFixed(0)}">
            <div class="match-header">
                <span class="match-score">${(match.score * 100).toFixed(0)}% Match</span>
                <span class="compatibility-type">${match.compatibility_type}</span>
            </div>
            <div class="product-info">
                <img src="${match.product.image}" alt="${match.product.name}">
                <h5>${match.product.name}</h5>
                <p class="price">£${match.product.price}</p>
                <div class="match-reasons">
                    ${match.reasons.map(reason => `<span class="reason-tag">${reason}</span>`).join('')}
                </div>
            </div>
            <div class="match-actions">
                <button class="btn-outline" onclick="addToCart(${match.product.id})">Add to Cart</button>
                <button class="btn-secondary" onclick="viewProduct(${match.product.id})">View Details</button>
            </div>
        </div>
    `).join('');
}

function updateMatches(productId) {
    const product = products.find(p => p.id === productId);
    if (!product) return;

    const occasion = document.getElementById('match-occasion').value;
    const season = document.getElementById('match-season').value;
    const style = document.getElementById('match-style').value;

    const matches = manvueProductMatcher.findMatchingProducts(product, {
        occasion,
        season,
        style_preference: style || null,
        max_results: 6
    });

    const grid = document.getElementById('matches-grid');
    if (grid) {
        grid.innerHTML = renderMatches(matches);
    }
}

function generateCompleteOutfit(productId) {
    const product = products.find(p => p.id === productId);
    if (!product) return;

    const occasion = document.getElementById('match-occasion')?.value || 'casual';
    const season = document.getElementById('match-season')?.value || 'all-season';
    const style = document.getElementById('match-style')?.value || null;

    const outfit = manvueProductMatcher.generateCompleteOutfit(product, {
        occasion,
        season,
        style_preference: style
    });

    showCompleteOutfit(outfit);
}

function showCompleteOutfit(outfit) {
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.id = 'complete-outfit-modal';
    
    const outfitItems = [outfit.base, ...Object.values(outfit.matches).map(m => m.product)];
    
    modal.innerHTML = `
        <div class="modal-content large">
            <div class="modal-header">
                <h3>👔 Complete Outfit</h3>
                <button onclick="closeModal('complete-outfit-modal')">✕</button>
            </div>
            
            <div class="outfit-content">
                <div class="outfit-metrics">
                    <div class="metric">
                        <span class="metric-label">Style Score</span>
                        <span class="metric-value">${(outfit.style_score * 100).toFixed(0)}%</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Completeness</span>
                        <span class="metric-value">${(outfit.completeness * 100).toFixed(0)}%</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Total Price</span>
                        <span class="metric-value">£${outfit.total_price}</span>
                    </div>
                </div>
                
                <div class="outfit-visualization">
                    <div class="outfit-grid">
                        ${outfitItems.map(item => `
                            <div class="outfit-item">
                                <img src="${item.image}" alt="${item.name}">
                                <h5>${item.name}</h5>
                                <p class="price">£${item.price}</p>
                                <span class="item-type">${item.type}</span>
                            </div>
                        `).join('')}
                    </div>
                </div>
                
                <div class="outfit-actions">
                    <button class="btn-primary large" onclick="addOutfitToCart(${JSON.stringify(outfitItems.map(i => i.id))})">
                        🛒 Add Entire Outfit to Cart
                    </button>
                    <button class="btn-secondary" onclick="saveOutfitAsTemplate(${JSON.stringify(outfit)})">
                        💾 Save as Template
                    </button>
                    <button class="btn-secondary" onclick="shareOutfit(${JSON.stringify(outfit)})">
                        📤 Share Outfit
                    </button>
                    <button class="btn-outline" onclick="try3DOutfit(${JSON.stringify(outfitItems.map(i => i.id))})">
                        🎮 Try in 3D
                    </button>
                </div>
            </div>
        </div>
    `;

    document.body.appendChild(modal);
    modal.style.display = 'flex';
}

function addOutfitToCart(itemIds) {
    itemIds.forEach(id => {
        const product = products.find(p => p.id === id);
        if (product) {
            addToCart(id);
        }
    });
    
    showMessage(`Added ${itemIds.length} items to cart!`);
    closeModal('complete-outfit-modal');
}

function saveOutfitAsTemplate(outfit) {
    const templates = JSON.parse(localStorage.getItem('manvue-outfit-templates') || '[]');
    
    const template = {
        id: Date.now(),
        name: `Outfit ${templates.length + 1}`,
        outfit: outfit,
        created: new Date().toLocaleDateString(),
        occasion: document.getElementById('match-occasion')?.value || 'casual'
    };
    
    templates.push(template);
    localStorage.setItem('manvue-outfit-templates', JSON.stringify(templates));
    
    showMessage('Outfit saved as template!');
}

function shareOutfit(outfit) {
    const shareData = {
        title: 'Check out this MANVUE outfit!',
        text: `I created this amazing outfit with ${Object.keys(outfit.matches).length + 1} pieces for £${outfit.total_price}`,
        url: window.location.href
    };
    
    if (navigator.share) {
        navigator.share(shareData);
    } else {
        // Fallback for browsers without Web Share API
        const shareText = `${shareData.title}\n${shareData.text}\n${shareData.url}`;
        navigator.clipboard.writeText(shareText).then(() => {
            showMessage('Outfit details copied to clipboard!');
        });
    }
}

function try3DOutfit(itemIds) {
    // Integration with 3D try-on system
    if (typeof toggle3DTryOn === 'function') {
        toggle3DTryOn();
        
        // Pre-select outfit items in 3D system
        setTimeout(() => {
            itemIds.forEach(id => {
                const product = products.find(p => p.id === id);
                if (product && typeof addTo3DOutfit === 'function') {
                    // This would integrate with the 3D system to pre-load items
                    console.log('Adding to 3D outfit:', product.name);
                }
            });
        }, 1000);
        
        showMessage('Opening 3D try-on with your outfit...');
    } else {
        showMessage('3D try-on feature not available');
    }
}

function saveMatchingPreferences(productId) {
    const product = products.find(p => p.id === productId);
    if (!product) return;

    const occasion = document.getElementById('match-occasion')?.value;
    const season = document.getElementById('match-season')?.value;
    const style = document.getElementById('match-style')?.value;

    const interaction = {
        productId: product.id,
        occasion,
        season,
        style,
        action: 'preference_saved'
    };

    manvueProductMatcher.saveUserPreference(interaction);
    showMessage('Preferences saved and will improve future recommendations!');
}

function getCurrentSeason() {
    const month = new Date().getMonth();
    if (month >= 2 && month <= 4) return 'spring';
    if (month >= 5 && month <= 7) return 'summer';
    if (month >= 8 && month <= 10) return 'autumn';
    return 'winter';
}

function showOutfitTemplates() {
    const templates = JSON.parse(localStorage.getItem('manvue-outfit-templates') || '[]');
    
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.id = 'outfit-templates-modal';
    
    modal.innerHTML = `
        <div class="modal-content large">
            <div class="modal-header">
                <h3>👔 Saved Outfit Templates</h3>
                <button onclick="closeModal('outfit-templates-modal')">✕</button>
            </div>
            
            <div class="templates-content">
                ${templates.length === 0 ? 
                    '<div class="no-templates">No saved outfit templates yet. Create your first outfit!</div>' :
                    `<div class="templates-grid">
                        ${templates.map(template => `
                            <div class="template-card">
                                <div class="template-header">
                                    <h4>${template.name}</h4>
                                    <span class="template-date">${template.created}</span>
                                </div>
                                <div class="template-preview">
                                    <div class="template-items">
                                        ${[template.outfit.base, ...Object.values(template.outfit.matches).map(m => m.product)].slice(0, 3).map(item => `
                                            <img src="${item.image}" alt="${item.name}" class="template-item-image">
                                        `).join('')}
                                    </div>
                                    <div class="template-info">
                                        <span class="template-occasion">${template.occasion}</span>
                                        <span class="template-price">£${template.outfit.total_price}</span>
                                    </div>
                                </div>
                                <div class="template-actions">
                                    <button class="btn-primary" onclick="loadOutfitTemplate(${template.id})">Load Outfit</button>
                                    <button class="btn-outline" onclick="deleteOutfitTemplate(${template.id})">Delete</button>
                                </div>
                            </div>
                        `).join('')}
                    </div>`
                }
                
                <div class="templates-actions">
                    <button class="btn-secondary" onclick="exportOutfitTemplates()">
                        📤 Export Templates
                    </button>
                    <button class="btn-outline" onclick="clearAllTemplates()">
                        🗑️ Clear All
                    </button>
                </div>
            </div>
        </div>
    `;

    document.body.appendChild(modal);
    modal.style.display = 'flex';
}

function loadOutfitTemplate(templateId) {
    const templates = JSON.parse(localStorage.getItem('manvue-outfit-templates') || '[]');
    const template = templates.find(t => t.id === templateId);
    
    if (template) {
        showCompleteOutfit(template.outfit);
        closeModal('outfit-templates-modal');
    }
}

function deleteOutfitTemplate(templateId) {
    const templates = JSON.parse(localStorage.getItem('manvue-outfit-templates') || '[]');
    const filtered = templates.filter(t => t.id !== templateId);
    localStorage.setItem('manvue-outfit-templates', JSON.stringify(filtered));
    
    showMessage('Template deleted');
    closeModal('outfit-templates-modal');
    showOutfitTemplates(); // Refresh the modal
}

function exportOutfitTemplates() {
    const templates = JSON.parse(localStorage.getItem('manvue-outfit-templates') || '[]');
    const dataStr = JSON.stringify(templates, null, 2);
    const dataBlob = new Blob([dataStr], {type: 'application/json'});
    
    const link = document.createElement('a');
    link.href = URL.createObjectURL(dataBlob);
    link.download = 'manvue-outfit-templates.json';
    link.click();
    
    showMessage('Templates exported successfully!');
}

function clearAllTemplates() {
    if (confirm('Are you sure you want to delete all outfit templates?')) {
        localStorage.removeItem('manvue-outfit-templates');
        showMessage('All templates cleared');
        closeModal('outfit-templates-modal');
    }
}

// Integrate matching system with existing product display
function addMatchingButtonToProducts() {
    // Add matching buttons to existing product cards
    const productCards = document.querySelectorAll('.product-card');
    productCards.forEach(card => {
        const productId = card.dataset.productId;
        if (productId && !card.querySelector('.match-button')) {
            const matchButton = document.createElement('button');
            matchButton.className = 'btn-outline match-button';
            matchButton.innerHTML = '🔗 Find Matches';
            matchButton.onclick = () => showProductMatches(parseInt(productId));
            
            const actions = card.querySelector('.product-actions') || card;
            actions.appendChild(matchButton);
        }
    });
}

// Enhanced buildOutfit function to use matching system
function buildOutfit() {
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.id = 'outfit-builder-modal';
    
    modal.innerHTML = `
        <div class="modal-content fullscreen">
            <div class="modal-header">
                <h3>👔 AI Outfit Builder</h3>
                <button onclick="closeModal('outfit-builder-modal')">✕</button>
            </div>
            
            <div class="outfit-builder-content">
                <div class="builder-sidebar">
                    <div class="builder-controls">
                        <h4>Outfit Settings</h4>
                        <div class="control-group">
                            <label>Occasion</label>
                            <select id="builder-occasion">
                                <option value="casual">Casual</option>
                                <option value="work">Work</option>
                                <option value="date">Date</option>
                                <option value="party">Party</option>
                                <option value="gym">Gym</option>
                            </select>
                        </div>
                        <div class="control-group">
                            <label>Season</label>
                            <select id="builder-season">
                                <option value="all-season">All Season</option>
                                <option value="spring">Spring</option>
                                <option value="summer">Summer</option>
                                <option value="autumn">Autumn</option>
                                <option value="winter">Winter</option>
                            </select>
                        </div>
                        <div class="control-group">
                            <label>Budget Limit (£)</label>
                            <input type="number" id="builder-budget" placeholder="No limit" min="0">
                        </div>
                        <div class="control-group">
                            <label>Style Preference</label>
                            <select id="builder-style">
                                <option value="">Auto</option>
                                <option value="casual">Casual</option>
                                <option value="formal">Formal</option>
                                <option value="smart-casual">Smart Casual</option>
                                <option value="business-casual">Business Casual</option>
                            </select>
                        </div>
                    </div>
                    
                    <div class="builder-actions">
                        <button class="btn-primary" onclick="generateRandomOutfit()">
                            🎲 Generate Random Outfit
                        </button>
                        <button class="btn-secondary" onclick="showOutfitTemplates()">
                            📁 Load Template
                        </button>
                        <button class="btn-outline" onclick="clearCurrentOutfit()">
                            🗑️ Clear Outfit
                        </button>
                    </div>
                </div>
                
                <div class="builder-main">
                    <div class="current-outfit" id="current-outfit">
                        <h4>Current Outfit</h4>
                        <div class="outfit-slots">
                            <div class="outfit-slot" data-category="top">
                                <span class="slot-label">Top</span>
                                <div class="slot-content" id="slot-top">Click to select</div>
                            </div>
                            <div class="outfit-slot" data-category="bottom">
                                <span class="slot-label">Bottom</span>
                                <div class="slot-content" id="slot-bottom">Click to select</div>
                            </div>
                            <div class="outfit-slot" data-category="shoes">
                                <span class="slot-label">Shoes</span>
                                <div class="slot-content" id="slot-shoes">Click to select</div>
                            </div>
                            <div class="outfit-slot" data-category="accessories">
                                <span class="slot-label">Accessories</span>
                                <div class="slot-content" id="slot-accessories">Click to select</div>
                            </div>
                        </div>
                        
                        <div class="outfit-summary" id="outfit-summary">
                            <div class="summary-item">Total: £0</div>
                            <div class="summary-item">Items: 0</div>
                            <div class="summary-item">Style Score: -</div>
                        </div>
                    </div>
                    
                    <div class="product-selector" id="product-selector">
                        <h4>Select Products</h4>
                        <div class="category-filters">
                            <button class="filter-btn active" onclick="filterBuilderProducts('all')">All</button>
                            <button class="filter-btn" onclick="filterBuilderProducts('top')">Tops</button>
                            <button class="filter-btn" onclick="filterBuilderProducts('bottom')">Bottoms</button>
                            <button class="filter-btn" onclick="filterBuilderProducts('shoes')">Shoes</button>
                            <button class="filter-btn" onclick="filterBuilderProducts('accessories')">Accessories</button>
                        </div>
                        <div class="products-grid" id="builder-products-grid">
                            <!-- Products will be loaded here -->
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;

    document.body.appendChild(modal);
    modal.style.display = 'flex';
    
    // Initialize the builder
    filterBuilderProducts('all');
}

// Helper functions
function changeAvatar() {
    showMessage('Avatar upload feature coming soon!');
}

function addNewAddress() {
    showMessage('Add address feature coming soon!');
}

function editAddress(index) {
    showMessage('Edit address feature coming soon!');
}

function deleteAddress(index) {
    userAddresses.splice(index, 1);
    localStorage.setItem('manvue_addresses', JSON.stringify(userAddresses));
    showAddressesTab(document.getElementById('profile-tab-content'));
    showMessage('Address deleted successfully!');
}

function setDefaultAddress(index) {
    userAddresses.forEach((addr, i) => addr.isDefault = i === index);
    localStorage.setItem('manvue_addresses', JSON.stringify(userAddresses));
    showAddressesTab(document.getElementById('profile-tab-content'));
    showMessage('Default address updated!');
}

function downloadData() {
    const userData = {
        user: currentUser,
        orders: userOrders,
        addresses: userAddresses,
        preferences: userPreferences,
        cart: cart,
        wishlist: wishlist
    };
    
    const dataStr = JSON.stringify(userData, null, 2);
    const dataBlob = new Blob([dataStr], {type: 'application/json'});
    const url = URL.createObjectURL(dataBlob);
    
    const link = document.createElement('a');
    link.href = url;
    link.download = 'manvue-user-data.json';
    link.click();
    
    showMessage('Your data has been downloaded!');
}

function deleteAccount() {
    if (confirm('Are you sure you want to delete your account? This action cannot be undone.')) {
        // Remove user from users array
        const existingUsers = JSON.parse(localStorage.getItem('manvue_users') || '[]');
        const updatedUsers = existingUsers.filter(u => u.id !== currentUser.id);
        localStorage.setItem('manvue_users', JSON.stringify(updatedUsers));
        
        // Clear all user data
        localStorage.removeItem('manvue_user');
        localStorage.removeItem('manvue_orders');
        localStorage.removeItem('manvue_addresses');
        localStorage.removeItem('manvue_preferences');
        
        // Logout
        logout();
        closeModal('profile-modal');
        showMessage('Account deleted successfully. We\'re sorry to see you go!');
    }
}

// Export functions to global scope for HTML onclick handlers
window.showSection = showSection;
window.toggleMobileMenu = toggleMobileMenu;
window.toggleSearch = toggleSearch;
window.searchProducts = searchProducts;
window.startVoiceSearch = startVoiceSearch;
window.filterProducts = filterProducts;
window.filterByType = filterByType;
window.filterByBrand = filterByBrand;
window.filterByStock = filterByStock;
window.updatePriceFilter = updatePriceFilter;
window.sortProducts = sortProducts;
window.changeView = changeView;
window.clearAllFilters = clearAllFilters;
window.loadMoreProducts = loadMoreProducts;
window.addToCart = addToCart;
window.addToWishlist = addToWishlist;
window.removeFromWishlist = removeFromWishlist;
window.toggleWishlist = toggleWishlist;
window.showDeals = showDeals;
window.showAllProducts = showAllProducts;
window.quickView = quickView;
window.toggleCart = toggleCart;
window.removeFromCart = removeFromCart;
window.checkout = checkout;
window.toggleUserMenu = toggleUserMenu;
window.showLogin = showLogin;
window.showRegister = showRegister;
window.showProfile = showProfile;
window.showOrders = showOrders;
window.showAddresses = showAddresses;
window.showPreferences = showPreferences;
window.showModal = showModal;
window.closeModal = closeModal;
window.handleLogin = handleLogin;
window.handleRegister = handleRegister;
window.handleForgotPassword = handleForgotPassword;
window.switchToLogin = switchToLogin;
window.switchToRegister = switchToRegister;
window.showForgotPassword = showForgotPassword;
window.logout = logout;
window.showProfileTab = showProfileTab;
window.updatePersonalInfo = updatePersonalInfo;
window.updatePreferences = updatePreferences;
window.changePassword = changePassword;
window.changeAvatar = changeAvatar;
window.addNewAddress = addNewAddress;
window.editAddress = editAddress;
window.deleteAddress = deleteAddress;
window.setDefaultAddress = setDefaultAddress;
window.downloadData = downloadData;
window.deleteAccount = deleteAccount;
window.toggleChatbot = toggleChatbot;
window.sendChatMessage = sendChatMessage;
window.startStyleQuiz = startStyleQuiz;
window.displayQuizQuestion = displayQuizQuestion;
window.selectQuizOption = selectQuizOption;
window.nextQuestion = nextQuestion;
window.previousQuestion = previousQuestion;
window.generateStyleProfile = generateStyleProfile;
window.showStyleRecommendations = showStyleRecommendations;
window.showOutfitBuilder = showOutfitBuilder;
window.updateOutfitRecommendations = updateOutfitRecommendations;
window.sendChatMessage = sendChatMessage;
window.getTrendingStyles = getTrendingStyles;
window.startImageSearch = startImageSearch;
window.switchUploadMethod = switchUploadMethod;
window.triggerFileInput = triggerFileInput;
window.handleImageUpload = handleImageUpload;
window.loadImageFromURL = loadImageFromURL;
window.clearImagePreview = clearImagePreview;
window.startCamera = startCamera;
window.capturePhoto = capturePhoto;
window.stopCamera = stopCamera;
window.analyzeImage = analyzeImage;
window.searchByColor = searchByColor;
window.performVisualSearch = performVisualSearch;
window.sortVisualResults = sortVisualResults;
window.filterVisualResults = filterVisualResults;
window.toggleVoiceInterface = toggleVoiceInterface;
window.toggleVoiceRecognition = toggleVoiceRecognition;
window.showVoiceCommands = showVoiceCommands;
window.toggleVoiceSettings = toggleVoiceSettings;
window.updateVoiceLanguage = updateVoiceLanguage;
window.updateVoiceSensitivity = updateVoiceSensitivity;
window.toggleContinuousListening = toggleContinuousListening;
window.toggleVoiceFeedback = toggleVoiceFeedback;
window.updateWakeWord = updateWakeWord;
window.testVoiceRecognition = testVoiceRecognition;
window.calibrateVoice = calibrateVoice;
window.toggle3DTryOn = toggle3DTryOn;
window.start3DCamera = start3DCamera;
window.stop3DCamera = stop3DCamera;
window.capture3DPhoto = capture3DPhoto;
window.toggle3DView = toggle3DView;
window.change3DViewMode = change3DViewMode;
window.adjust3DLighting = adjust3DLighting;
window.change3DEnvironment = change3DEnvironment;
window.showTryOnCategory = showTryOnCategory;
window.addTo3DOutfit = addTo3DOutfit;
window.adjustBodyMeasurement = adjustBodyMeasurement;
window.save3DMeasurements = save3DMeasurements;
window.autoDetectMeasurements = autoDetectMeasurements;
window.reset3DMeasurements = reset3DMeasurements;
window.startVirtualFitting = startVirtualFitting;
window.save3DOutfit = save3DOutfit;
window.share3DOutfit = share3DOutfit;
window.exportMeasurements = exportMeasurements;
window.show3DProduct = show3DProduct;
window.rotate3DProduct = rotate3DProduct;
window.zoom3DProduct = zoom3DProduct;
window.reset3DProduct = reset3DProduct;
window.tryOn3DProduct = tryOn3DProduct;
window.view3DDetails = view3DDetails;
window.toggleChatSettings = toggleChatSettings;
window.clearChatHistory = clearChatHistory;
window.updateChatLanguage = updateChatLanguage;
window.updateResponseStyle = updateResponseStyle;
window.updateTypingSpeed = updateTypingSpeed;
window.toggleVoiceInput = toggleVoiceInput;
window.attachFile = attachFile;
window.sendMessage = sendMessage;
window.toggleQuickActions = toggleQuickActions;
window.showSuggestions = showSuggestions;
window.startTour = startTour;
window.getPersonalShopper = getPersonalShopper;
window.getStyleTips = getStyleTips;
window.askAboutProduct = askAboutProduct;
window.getCustomerSupport = getCustomerSupport;
window.sendChatMessage = sendChatMessage;
window.showProductMatches = showProductMatches;
window.updateMatches = updateMatches;
window.generateCompleteOutfit = generateCompleteOutfit;
window.addOutfitToCart = addOutfitToCart;
window.saveOutfitAsTemplate = saveOutfitAsTemplate;
window.shareOutfit = shareOutfit;
window.try3DOutfit = try3DOutfit;
window.saveMatchingPreferences = saveMatchingPreferences;
window.showOutfitTemplates = showOutfitTemplates;
window.loadOutfitTemplate = loadOutfitTemplate;
window.deleteOutfitTemplate = deleteOutfitTemplate;
window.exportOutfitTemplates = exportOutfitTemplates;
window.clearAllTemplates = clearAllTemplates;
window.addMatchingButtonToProducts = addMatchingButtonToProducts;
window.show3DDemo = show3DDemo;
window.showChatbot = showChatbot;
window.closeAllMenus = closeAllMenus;