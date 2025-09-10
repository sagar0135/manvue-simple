// Product Page JavaScript
const API_BASE_URL = "http://localhost:5001"; // Updated to use enhanced backend

// Global variables
let currentProduct = null;
let selectedSize = null;
let selectedColor = null;
let quantity = 1;
let cart = JSON.parse(localStorage.getItem('cart')) || [];

// Initialize page when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
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
    if (element.classList.contains('unavailable')) return;
    
    // Update selected size
    document.querySelectorAll('.size-option').forEach(option => {
        option.classList.remove('selected');
    });
    element.classList.add('selected');
    
    selectedSize = size;
    updateTotalPrice();
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
    // Update selected color
    document.querySelectorAll('.color-option').forEach(option => {
        option.classList.remove('selected');
    });
    element.classList.add('selected');
    
    selectedColor = color;
    updateTotalPrice();
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
    const quantityInput = document.getElementById('quantity');
    const currentValue = parseInt(quantityInput.value);
    if (currentValue < 10) {
        quantityInput.value = currentValue + 1;
        quantity = currentValue + 1;
        updateTotalPrice();
    }
}

function decreaseQuantity() {
    const quantityInput = document.getElementById('quantity');
    const currentValue = parseInt(quantityInput.value);
    if (currentValue > 1) {
        quantityInput.value = currentValue - 1;
        quantity = currentValue - 1;
        updateTotalPrice();
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
    if (!currentProduct) return;
    
    if (!selectedSize) {
        alert('Please select a size');
        return;
    }
    
    if (!selectedColor) {
        alert('Please select a color');
        return;
    }
    
    const cartItem = {
        id: currentProduct.id,
        title: currentProduct.title || currentProduct.name,
        price: currentProduct.price,
        image_url: currentProduct.image_url || currentProduct.image,
        size: selectedSize,
        color: selectedColor,
        quantity: quantity
    };
    
    // Check if item already exists in cart
    const existingItemIndex = cart.findIndex(item => 
        item.id === cartItem.id && 
        item.size === cartItem.size && 
        item.color === cartItem.color
    );
    
    if (existingItemIndex > -1) {
        cart[existingItemIndex].quantity += quantity;
    } else {
        cart.push(cartItem);
    }
    
    localStorage.setItem('cart', JSON.stringify(cart));
    
    // Show success message
    showMessage('✅ Product added to cart!', 'success');
    
    // Update cart count if it exists
    updateCartCount();
}

// Add to wishlist
function addToWishlist() {
    if (!currentProduct) return;
    
    let wishlist = JSON.parse(localStorage.getItem('wishlist')) || [];
    
    const wishlistItem = {
        id: currentProduct.id,
        title: currentProduct.title || currentProduct.name,
        price: currentProduct.price,
        image_url: currentProduct.image_url || currentProduct.image
    };
    
    // Check if already in wishlist
    const exists = wishlist.some(item => item.id === wishlistItem.id);
    
    if (!exists) {
        wishlist.push(wishlistItem);
        localStorage.setItem('wishlist', JSON.stringify(wishlist));
        showMessage('❤️ Added to wishlist!', 'success');
    } else {
        showMessage('Already in wishlist!', 'info');
    }
}

// Image zoom functionality
function toggleImageZoom() {
    const modal = document.getElementById('image-zoom-modal');
    const zoomedImage = document.getElementById('zoomed-image');
    const mainImage = document.getElementById('main-product-image');
    
    zoomedImage.src = mainImage.src;
    modal.style.display = 'block';
}

function closeImageZoom() {
    const modal = document.getElementById('image-zoom-modal');
    modal.style.display = 'none';
}

// Navigate to product
function goToProduct(productId) {
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
    const messageDiv = document.createElement('div');
    messageDiv.className = `message message-${type}`;
    messageDiv.textContent = message;
    messageDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 2rem;
        border-radius: 4px;
        color: white;
        font-weight: 500;
        z-index: 1001;
        animation: slideIn 0.3s ease;
    `;
    
    // Set background color based on type
    switch (type) {
        case 'success':
            messageDiv.style.background = '#28a745';
            break;
        case 'error':
            messageDiv.style.background = '#dc3545';
            break;
        case 'info':
            messageDiv.style.background = '#17a2b8';
            break;
        default:
            messageDiv.style.background = '#6c757d';
    }
    
    document.body.appendChild(messageDiv);
    
    // Remove after 3 seconds
    setTimeout(() => {
        messageDiv.remove();
    }, 3000);
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
