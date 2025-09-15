#!/usr/bin/env python3
"""
ManVue Product HTML Generator
Automatically generates responsive product pages with cart functionality
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any

class ProductHTMLGenerator:
    def __init__(self, output_dir="frontend/products"):
        self.output_dir = output_dir
        self.products_data = self.load_products_data()
        self.ensure_output_directory()
    
    def load_products_data(self) -> List[Dict]:
        """Load products data from JSON file"""
        try:
            # Try to load from sample products JSON first
            json_file = 'frontend/data/sample_products.json'
            if os.path.exists(json_file):
                with open(json_file, 'r', encoding='utf-8') as f:
                    products = json.load(f)
                    print(f"Loaded {len(products)} products from {json_file}")
                    return products
            
            # Fallback: create some sample products
            return self.create_sample_products()
        except Exception as e:
            print(f"Error loading products: {e}")
            return self.create_sample_products()
    
    def create_sample_products(self) -> List[Dict]:
        """Create sample products if no data file exists"""
        return [
            {
                "id": "tshirt-001",
                "name": "Classic Cotton Crew Neck",
                "brand": "MANVUE Basics",
                "price": 24.99,
                "originalPrice": 29.99,
                "discount": 17,
                "category": "tshirts",
                "type": "tshirt",
                "description": "Comfortable 100% cotton crew neck t-shirt perfect for everyday wear.",
                "image": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=500&fit=crop",
                "colors": ["Black", "White", "Navy", "Gray"],
                "sizes": ["XS", "S", "M", "L", "XL", "XXL"],
                "rating": 4.5,
                "reviews": 342,
                "inStock": True,
                "tags": ["casual", "cotton", "basic"]
            },
            {
                "id": "shirt-001",
                "name": "Premium Oxford Button-Down",
                "brand": "MANVUE Professional",
                "price": 49.99,
                "originalPrice": 59.99,
                "discount": 17,
                "category": "shirts",
                "type": "dress-shirt",
                "description": "Classic Oxford button-down shirt in premium cotton.",
                "image": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=400&h=500&fit=crop",
                "colors": ["White", "Light Blue", "Navy"],
                "sizes": ["S", "M", "L", "XL", "XXL"],
                "rating": 4.7,
                "reviews": 128,
                "inStock": True,
                "tags": ["formal", "business", "oxford"]
            }
        ]
    
    def ensure_output_directory(self):
        """Create output directory if it doesn't exist"""
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_product_html(self, product: Dict[str, Any]) -> str:
        """Generate HTML for a single product"""
        product_id = product.get('id', 'unknown')
        name = product.get('name', 'Unknown Product')
        price = product.get('price', 0)
        image = product.get('image', 'https://via.placeholder.com/400x400?text=No+Image')
        description = product.get('description', 'No description available')
        category = product.get('category', 'general')
        brand = product.get('brand', 'ManVue')
        rating = product.get('rating', 4.0)
        sizes = product.get('sizes', ['S', 'M', 'L', 'XL'])
        colors = product.get('colors', ['Black', 'White', 'Blue'])
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} - ManVue</title>
    <link rel="stylesheet" href="../css/style.css">
    <link rel="stylesheet" href="../css/product-page.css">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        .product-hero {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px 0;
            margin-bottom: 30px;
        }}
        
        .product-container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }}
        
        .product-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 40px;
            margin-bottom: 50px;
        }}
        
        .product-image-section {{
            position: relative;
        }}
        
        .main-image {{
            width: 100%;
            height: 500px;
            object-fit: cover;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }}
        
        .product-info {{
            padding: 20px 0;
        }}
        
        .product-title {{
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 10px;
            color: #333;
        }}
        
        .product-price {{
            font-size: 2rem;
            font-weight: 600;
            color: #e74c3c;
            margin-bottom: 20px;
        }}
        
        .product-rating {{
            display: flex;
            align-items: center;
            margin-bottom: 20px;
        }}
        
        .stars {{
            color: #ffc107;
            margin-right: 10px;
        }}
        
        .rating-text {{
            color: #666;
            font-size: 0.9rem;
        }}
        
        .product-description {{
            font-size: 1.1rem;
            line-height: 1.6;
            color: #555;
            margin-bottom: 30px;
        }}
        
        .product-options {{
            margin-bottom: 30px;
        }}
        
        .option-group {{
            margin-bottom: 20px;
        }}
        
        .option-label {{
            font-weight: 600;
            margin-bottom: 10px;
            display: block;
            color: #333;
        }}
        
        .size-options, .color-options {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }}
        
        .size-btn, .color-btn {{
            padding: 10px 20px;
            border: 2px solid #e9ecef;
            background: white;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 500;
        }}
        
        .size-btn:hover, .size-btn.selected {{
            border-color: #667eea;
            background: #667eea;
            color: white;
        }}
        
        .color-btn {{
            width: 40px;
            height: 40px;
            border-radius: 50%;
            padding: 0;
            position: relative;
        }}
        
        .color-btn::after {{
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: var(--color);
        }}
        
        .color-btn.selected {{
            border-color: #333;
            box-shadow: 0 0 0 2px #667eea;
        }}
        
        .quantity-selector {{
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 30px;
        }}
        
        .quantity-btn {{
            width: 40px;
            height: 40px;
            border: 2px solid #e9ecef;
            background: white;
            border-radius: 8px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2rem;
            font-weight: 600;
        }}
        
        .quantity-input {{
            width: 60px;
            height: 40px;
            text-align: center;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            font-size: 1.1rem;
            font-weight: 600;
        }}
        
        .action-buttons {{
            display: flex;
            gap: 15px;
            margin-bottom: 30px;
        }}
        
        .btn-primary {{
            flex: 1;
            padding: 15px 30px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        
        .btn-primary:hover {{
            background: #5a6fd8;
            transform: translateY(-2px);
        }}
        
        .btn-secondary {{
            padding: 15px 30px;
            background: white;
            color: #667eea;
            border: 2px solid #667eea;
            border-radius: 10px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        
        .btn-secondary:hover {{
            background: #667eea;
            color: white;
        }}
        
        .product-features {{
            background: #f8f9fa;
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
        }}
        
        .features-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
        }}
        
        .feature-item {{
            text-align: center;
            padding: 20px;
            background: white;
            border-radius: 10px;
        }}
        
        .feature-icon {{
            font-size: 2rem;
            margin-bottom: 10px;
        }}
        
        .feature-title {{
            font-weight: 600;
            margin-bottom: 5px;
            color: #333;
        }}
        
        .feature-desc {{
            font-size: 0.9rem;
            color: #666;
        }}
        
        .related-products {{
            margin-top: 50px;
        }}
        
        .related-title {{
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 30px;
            text-align: center;
            color: #333;
        }}
        
        .related-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
        }}
        
        .related-item {{
            background: white;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }}
        
        .related-item:hover {{
            transform: translateY(-5px);
        }}
        
        .related-image {{
            width: 100%;
            height: 200px;
            object-fit: cover;
        }}
        
        .related-info {{
            padding: 20px;
        }}
        
        .related-name {{
            font-weight: 600;
            margin-bottom: 10px;
            color: #333;
        }}
        
        .related-price {{
            color: #e74c3c;
            font-weight: 600;
            font-size: 1.1rem;
        }}
        
        @media (max-width: 768px) {{
            .product-grid {{
                grid-template-columns: 1fr;
                gap: 20px;
            }}
            
            .product-title {{
                font-size: 2rem;
            }}
            
            .action-buttons {{
                flex-direction: column;
            }}
        }}
    </style>
</head>
<body>
    <!-- Header -->
    <header class="header">
        <div class="container">
            <div class="header-content">
                <div class="logo">
                    <a href="../index.html" style="text-decoration: none; color: inherit;">
                        <h1>MANVUE</h1>
                        <span class="logo-subtitle">Premium Fashion</span>
                    </a>
                </div>
                
                <div class="header-actions">
                    <div class="wishlist-icon" onclick="toggleWishlist()">♡</div>
                    <div class="cart-icon" onclick="toggleCart()">
                        🛒 <span id="cart-count">0</span>
                    </div>
                </div>
            </div>
        </div>
    </header>

    <!-- Product Hero -->
    <div class="product-hero">
        <div class="product-container">
            <h1>{name}</h1>
            <p>Premium Quality • {brand} • {category.title()}</p>
        </div>
    </div>

    <!-- Product Details -->
    <div class="product-container">
        <div class="product-grid">
            <div class="product-image-section">
                <img src="{image}" alt="{name}" class="main-image" id="main-image">
            </div>
            
            <div class="product-info">
                <h2 class="product-title">{name}</h2>
                <div class="product-price">£{price:.2f}</div>
                
                <div class="product-rating">
                    <div class="stars">
                        {'★' * int(rating)}{'☆' * (5 - int(rating))}
                    </div>
                    <span class="rating-text">({rating}/5) • 127 reviews</span>
                </div>
                
                <div class="product-description">
                    {description}
                </div>
                
                <div class="product-options">
                    <div class="option-group">
                        <label class="option-label">Size</label>
                        <div class="size-options" id="size-options">
                            {self.generate_size_options(sizes)}
                        </div>
                    </div>
                    
                    <div class="option-group">
                        <label class="option-label">Color</label>
                        <div class="color-options" id="color-options">
                            {self.generate_color_options(colors)}
                        </div>
                    </div>
                    
                    <div class="quantity-selector">
                        <label class="option-label">Quantity</label>
                        <button class="quantity-btn" onclick="changeQuantity(-1)">-</button>
                        <input type="number" class="quantity-input" id="quantity" value="1" min="1" max="10">
                        <button class="quantity-btn" onclick="changeQuantity(1)">+</button>
                    </div>
                </div>
                
                <div class="action-buttons">
                    <button class="btn-primary" onclick="addToCart()">
                        <i class="fas fa-shopping-cart"></i> Add to Cart
                    </button>
                    <button class="btn-secondary" onclick="addToWishlist()">
                        <i class="fas fa-heart"></i> Wishlist
                    </button>
                </div>
                
                <div class="product-features">
                    <div class="features-grid">
                        <div class="feature-item">
                            <div class="feature-icon">🚚</div>
                            <div class="feature-title">Free Shipping</div>
                            <div class="feature-desc">On orders over £50</div>
                        </div>
                        <div class="feature-item">
                            <div class="feature-icon">🔄</div>
                            <div class="feature-title">Easy Returns</div>
                            <div class="feature-desc">30-day return policy</div>
                        </div>
                        <div class="feature-item">
                            <div class="feature-icon">🔒</div>
                            <div class="feature-title">Secure Payment</div>
                            <div class="feature-desc">SSL encrypted checkout</div>
                        </div>
                        <div class="feature-item">
                            <div class="feature-icon">📞</div>
                            <div class="feature-title">24/7 Support</div>
                            <div class="feature-desc">Customer service help</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Related Products -->
        <div class="related-products">
            <h3 class="related-title">You Might Also Like</h3>
            <div class="related-grid" id="related-products">
                {self.generate_related_products(category)}
            </div>
        </div>
    </div>

    <!-- Cart Sidebar -->
    <div id="cart-sidebar" class="cart-sidebar">
        <div class="cart-header">
            <h3>Shopping Cart</h3>
            <button onclick="toggleCart()">✕</button>
        </div>
        <div id="cart-items" class="cart-items">
            <!-- Cart items will be loaded here -->
        </div>
        <div class="cart-footer">
            <div class="cart-total">Total: £<span id="cart-total">0.00</span></div>
            <button class="btn-primary" onclick="proceedToCheckout()">Checkout</button>
        </div>
    </div>

    <!-- Wishlist Sidebar -->
    <div id="wishlist-sidebar" class="wishlist-sidebar">
        <div class="wishlist-header">
            <h3>Wishlist</h3>
            <button onclick="toggleWishlist()">✕</button>
        </div>
        <div id="wishlist-items" class="wishlist-items">
            <p>Your wishlist is empty</p>
        </div>
    </div>

    <!-- Scripts -->
    <script src="../data/products.js"></script>
    <script src="../js/script.js"></script>
    <script>
        // Product-specific JavaScript
        const product = {json.dumps(product)};
        let selectedSize = null;
        let selectedColor = null;
        let quantity = 1;

        // Initialize product page
        document.addEventListener('DOMContentLoaded', function() {{
            initializeProductPage();
            loadRelatedProducts();
        }});

        function initializeProductPage() {{
            // Set up size selection
            document.querySelectorAll('.size-btn').forEach(btn => {{
                btn.addEventListener('click', function() {{
                    document.querySelectorAll('.size-btn').forEach(b => b.classList.remove('selected'));
                    this.classList.add('selected');
                    selectedSize = this.textContent;
                }});
            }});

            // Set up color selection
            document.querySelectorAll('.color-btn').forEach(btn => {{
                btn.addEventListener('click', function() {{
                    document.querySelectorAll('.color-btn').forEach(b => b.classList.remove('selected'));
                    this.classList.add('selected');
                    selectedColor = this.dataset.color;
                }});
            }});

            // Select first size and color by default
            if (document.querySelector('.size-btn')) {{
                document.querySelector('.size-btn').click();
            }}
            if (document.querySelector('.color-btn')) {{
                document.querySelector('.color-btn').click();
            }}
        }}

        function changeQuantity(delta) {{
            const input = document.getElementById('quantity');
            const newValue = parseInt(input.value) + delta;
            if (newValue >= 1 && newValue <= 10) {{
                input.value = newValue;
                quantity = newValue;
            }}
        }}

        function addToCart() {{
            if (!selectedSize) {{
                alert('Please select a size');
                return;
            }}
            if (!selectedColor) {{
                alert('Please select a color');
                return;
            }}

            const cartItem = {{
                id: product.id,
                name: product.name,
                price: product.price,
                image: product.image,
                size: selectedSize,
                color: selectedColor,
                quantity: quantity
            }};

            // Add to cart (using existing cart functionality)
            if (typeof addToCart === 'function') {{
                addToCart(cartItem);
            }} else {{
                // Fallback cart functionality
                let cart = JSON.parse(localStorage.getItem('cart') || '[]');
                cart.push(cartItem);
                localStorage.setItem('cart', JSON.stringify(cart));
                updateCartDisplay();
            }}

            // Show success message
            showNotification('Added to cart!', 'success');
        }}

        function addToWishlist() {{
            const wishlistItem = {{
                id: product.id,
                name: product.name,
                price: product.price,
                image: product.image
            }};

            // Add to wishlist (using existing wishlist functionality)
            if (typeof addToWishlist === 'function') {{
                addToWishlist(wishlistItem);
            }} else {{
                // Fallback wishlist functionality
                let wishlist = JSON.parse(localStorage.getItem('wishlist') || '[]');
                wishlist.push(wishlistItem);
                localStorage.setItem('wishlist', JSON.stringify(wishlist));
                updateWishlistDisplay();
            }}

            showNotification('Added to wishlist!', 'success');
        }}

        function loadRelatedProducts() {{
            // Load related products from the same category
            const relatedContainer = document.getElementById('related-products');
            if (relatedContainer && window.products) {{
                const related = window.products
                    .filter(p => p.category === product.category && p.id !== product.id)
                    .slice(0, 4);
                
                relatedContainer.innerHTML = related.map(p => `
                    <div class="related-item" onclick="window.location.href='${{p.id}}.html'">
                        <img src="${{p.image}}" alt="${{p.name}}" class="related-image">
                        <div class="related-info">
                            <div class="related-name">${{p.name}}</div>
                            <div class="related-price">£${{p.price.toFixed(2)}}</div>
                        </div>
                    </div>
                `).join('');
            }}
        }}

        function showNotification(message, type = 'info') {{
            const notification = document.createElement('div');
            notification.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                background: ${{type === 'success' ? '#28a745' : '#007bff'}};
                color: white;
                padding: 15px 20px;
                border-radius: 8px;
                z-index: 10000;
                font-weight: 500;
            `;
            notification.textContent = message;
            document.body.appendChild(notification);
            
            setTimeout(() => {{
                notification.remove();
            }}, 3000);
        }}

        // Update cart display
        function updateCartDisplay() {{
            const cart = JSON.parse(localStorage.getItem('cart') || '[]');
            const cartCount = cart.reduce((sum, item) => sum + item.quantity, 0);
            const cartTotal = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
            
            document.getElementById('cart-count').textContent = cartCount;
            document.getElementById('cart-total').textContent = cartTotal.toFixed(2);
        }}

        // Update wishlist display
        function updateWishlistDisplay() {{
            const wishlist = JSON.parse(localStorage.getItem('wishlist') || '[]');
            const wishlistCount = wishlist.length;
            
            // Update wishlist count if element exists
            const wishlistIcon = document.querySelector('.wishlist-icon');
            if (wishlistIcon && wishlistCount > 0) {{
                wishlistIcon.innerHTML = `♡ <span>${{wishlistCount}}</span>`;
            }}
        }}

        // Initialize displays
        updateCartDisplay();
        updateWishlistDisplay();
    </script>
</body>
</html>"""
    
    def generate_size_options(self, sizes: List[str]) -> str:
        """Generate size option buttons"""
        return ''.join([f'<button class="size-btn" data-size="{size}">{size}</button>' for size in sizes])
    
    def generate_color_options(self, colors: List[str]) -> str:
        """Generate color option buttons"""
        color_map = {
            'Black': '#000000',
            'White': '#ffffff',
            'Blue': '#007bff',
            'Red': '#dc3545',
            'Green': '#28a745',
            'Brown': '#8b4513',
            'Gray': '#6c757d',
            'Grey': '#6c757d',
            'Navy': '#001f3f',
            'Maroon': '#800000'
        }
        
        return ''.join([
            f'<button class="color-btn" data-color="{color}" style="--color: {color_map.get(color, "#000000")}"></button>'
            for color in colors
        ])
    
    def generate_related_products(self, category: str) -> str:
        """Generate related products section"""
        related = [p for p in self.products_data if p.get('category') == category][:4]
        return ''.join([
            f'''
            <div class="related-item" onclick="window.location.href='{p.get("id", "unknown")}.html'">
                <img src="{p.get("image", "")}" alt="{p.get("name", "")}" class="related-image">
                <div class="related-info">
                    <div class="related-name">{p.get("name", "")}</div>
                    <div class="related-price">£{p.get("price", 0):.2f}</div>
                </div>
            </div>
            ''' for p in related
        ])
    
    def generate_all_products(self):
        """Generate HTML files for all products"""
        print(f"Generating HTML files for {len(self.products_data)} products...")
        
        for product in self.products_data:
            product_id = product.get('id', 'unknown')
            html_content = self.generate_product_html(product)
            
            filename = f"{product_id}.html"
            filepath = os.path.join(self.output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"Generated: {filename}")
        
        print(f"✅ Generated {len(self.products_data)} product pages in {self.output_dir}/")
    
    def generate_index_page(self):
        """Generate an index page listing all products"""
        index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>All Products - ManVue</title>
    <link rel="stylesheet" href="../css/style.css">
    <style>
        .products-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 60px 0;
            text-align: center;
        }}
        
        .products-container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
        }}
        
        .products-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin-top: 40px;
        }}
        
        .product-card {{
            background: white;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }}
        
        .product-card:hover {{
            transform: translateY(-5px);
        }}
        
        .product-image {{
            width: 100%;
            height: 250px;
            object-fit: cover;
        }}
        
        .product-info {{
            padding: 20px;
        }}
        
        .product-name {{
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 10px;
            color: #333;
        }}
        
        .product-price {{
            font-size: 1.5rem;
            font-weight: 700;
            color: #e74c3c;
            margin-bottom: 10px;
        }}
        
        .product-category {{
            color: #666;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
    </style>
</head>
<body>
    <div class="products-header">
        <h1>All Products</h1>
        <p>Discover our complete collection of premium fashion items</p>
    </div>
    
    <div class="products-container">
        <div class="products-grid">
            {self.generate_all_product_cards()}
        </div>
    </div>
    
    <script>
        // Add any necessary JavaScript here
    </script>
</body>
</html>"""
        
        with open(os.path.join(self.output_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(index_html)
        
        print("Generated: index.html")
    
    def generate_all_product_cards(self) -> str:
        """Generate product cards for the index page"""
        return ''.join([
            f'''
            <div class="product-card" onclick="window.location.href='{p.get("id", "unknown")}.html'">
                <img src="{p.get("image", "")}" alt="{p.get("name", "")}" class="product-image">
                <div class="product-info">
                    <div class="product-name">{p.get("name", "")}</div>
                    <div class="product-price">£{p.get("price", 0):.2f}</div>
                    <div class="product-category">{p.get("category", "").title()}</div>
                </div>
            </div>
            ''' for p in self.products_data
        ])

if __name__ == "__main__":
    generator = ProductHTMLGenerator()
    generator.generate_all_products()
    generator.generate_index_page()
    print("🎉 Product HTML generation complete!")
