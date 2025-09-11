#!/usr/bin/env python3
"""
Product Data Seeding Script
Creates sample product data with GridFS images for testing
"""

import asyncio
import sys
import os
import json
from datetime import datetime

# Add the parent directory to the path to import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from backend.database import create_product, test_connection

# Sample product data with color-specific images
SAMPLE_PRODUCTS = [
    {
        "name": "Classic Cotton Crew Neck",
        "title": "Classic Cotton Crew Neck T-Shirt",
        "price": 24.99,
        "originalPrice": 29.99,
        "category": "men",
        "type": "tops",
        "size": ["XS", "S", "M", "L", "XL", "XXL"],
        "color": ["Black", "White", "Navy", "Gray"],
        "brand": "MANVUE Basics",
        "rating": 4.5,
        "reviews": 342,
        "image_urls": [
            "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=500&fit=crop&auto=format",
            "https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=400&h=500&fit=crop&auto=format",
            "https://images.unsplash.com/photo-1503341504253-dff4815485f1?w=400&h=500&fit=crop&auto=format"
        ],
        "image_ids": [],  # Will be populated when images are uploaded to GridFS
        "tags": ["casual", "cotton", "basic", "everyday", "comfortable"],
        "inStock": True,
        "description": "Comfortable 100% cotton crew neck t-shirt perfect for everyday wear. Made from premium organic cotton with a relaxed fit.",
        "features": [
            "100% Organic Cotton",
            "Pre-shrunk fabric",
            "Reinforced seams",
            "Machine washable",
            "Comfortable fit"
        ]
    },
    {
        "name": "Premium Denim Jeans",
        "title": "Premium Denim Jeans - Slim Fit",
        "price": 64.99,
        "originalPrice": 74.99,
        "category": "men",
        "type": "bottoms",
        "size": ["30", "32", "34", "36", "38", "40"],
        "color": ["Dark Blue", "Black", "Light Blue", "Gray"],
        "brand": "MANVUE Denim",
        "rating": 4.7,
        "reviews": 189,
        "image_urls": [
            "https://images.unsplash.com/photo-1542272604-787c3835535d?w=400&h=500&fit=crop&auto=format",
            "https://images.unsplash.com/photo-1503341504253-dff4815485f1?w=400&h=500&fit=crop&auto=format",
            "https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=400&h=500&fit=crop&auto=format"
        ],
        "image_ids": [],
        "tags": ["denim", "classic", "casual", "slim-fit", "premium"],
        "inStock": True,
        "description": "Premium denim jeans with a perfect slim fit. Made from high-quality denim with stretch comfort and reinforced stitching.",
        "features": [
            "Premium Denim",
            "Slim Fit",
            "Stretch Comfort",
            "Reinforced Stitching",
            "Machine Washable"
        ]
    },
    {
        "name": "Athletic Running Trainers",
        "title": "Athletic Running Trainers - High Performance",
        "price": 104.99,
        "originalPrice": 124.99,
        "category": "men",
        "type": "shoes",
        "size": ["7", "8", "9", "10", "11", "12"],
        "color": ["White", "Black", "Gray", "Navy"],
        "brand": "SportMax",
        "rating": 4.8,
        "reviews": 334,
        "image_urls": [
            "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=400&h=500&fit=crop&auto=format",
            "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=500&fit=crop&auto=format",
            "https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=400&h=500&fit=crop&auto=format"
        ],
        "image_ids": [],
        "tags": ["sports", "running", "comfort", "breathable", "athletic"],
        "inStock": True,
        "description": "High-performance running trainers with breathable mesh upper and responsive cushioning for maximum comfort.",
        "features": [
            "Breathable Mesh Upper",
            "Responsive Cushioning",
            "Lightweight Design",
            "Durable Outsole",
            "Moisture Wicking"
        ]
    }
]

async def load_converted_images():
    """Load converted image data if available"""
    converted_file = "converted_products_with_gridfs_ids.json"
    if os.path.exists(converted_file):
        try:
            with open(converted_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  Could not load converted images: {e}")
    return None

async def seed_products():
    """Seed the database with sample product data"""
    print("🌱 Starting product data seeding...")
    
    # Test database connection
    if not await test_connection():
        print("❌ Database connection failed. Please check your MongoDB setup.")
        return
    
    # Check if we have converted images
    converted_products = await load_converted_images()
    if converted_products:
        print("📁 Found converted GridFS images! Using GridFS image IDs.")
        products_to_use = converted_products
    else:
        print("🌐 No converted images found. Using external URLs.")
        print("💡 Run 'python convert_images_to_gridfs.py' first to convert images to GridFS.")
        products_to_use = SAMPLE_PRODUCTS
    
    created_products = []
    
    for product_data in products_to_use:
        try:
            print(f"Creating product: {product_data['name']}")
            
            # Add timestamps
            product_data = product_data.copy()  # Don't modify original
            product_data['created_at'] = datetime.now()
            product_data['updated_at'] = datetime.now()
            
            # Show image info
            if product_data.get('image_ids'):
                print(f"  📷 Using {len(product_data['image_ids'])} GridFS images")
            elif product_data.get('image_urls'):
                print(f"  🌐 Using {len(product_data['image_urls'])} external image URLs")
            
            # Create the product
            product_id = await create_product(product_data)
            created_products.append({
                'id': product_id,
                'name': product_data['name']
            })
            
            print(f"✅ Created product: {product_data['name']} (ID: {product_id})")
            
        except Exception as e:
            print(f"❌ Error creating product {product_data['name']}: {e}")
    
    print(f"\n🎉 Seeding completed! Created {len(created_products)} products:")
    for product in created_products:
        print(f"  - {product['name']} (ID: {product['id']})")
    
    print("\n📝 Next steps:")
    if converted_products:
        print("1. Start your API server: python api/start_enhanced_backend.py")
        print("2. Update the PRODUCT_ID in your frontend to match one of the created product IDs")
        print("3. Test the product page to see GridFS images!")
    else:
        print("1. Convert images to GridFS: python convert_images_to_gridfs.py")
        print("2. Re-run this seeding script to use GridFS images")
        print("3. Start your API server: python api/start_enhanced_backend.py")
        print("4. Test the product page!")

if __name__ == "__main__":
    asyncio.run(seed_products())
