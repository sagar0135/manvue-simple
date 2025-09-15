#!/usr/bin/env python3
"""
MANVUE Colab Image Setup Script
Colab-optimized version for converting images to GridFS
"""

import asyncio
import sys
import os
import json
import aiohttp
import io
import base64
from urllib.parse import urlparse
from datetime import datetime
from typing import List, Dict, Tuple, Optional
import logging

# Configure logging for Colab
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class ColabImageConverter:
    """Colab-optimized image converter for MANVUE"""
    
    def __init__(self, api_base_url: str = "http://localhost:5001"):
        self.api_base_url = api_base_url.rstrip('/')
        self.session = None
        self.downloaded_images = []
        self.failed_downloads = []

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def test_api_connection(self) -> bool:
        """Test connection to MANVUE API"""
        try:
            async with self.session.get(f"{self.api_base_url}/health", timeout=10) as response:
                if response.status == 200:
                    logger.info("✅ Connected to MANVUE API successfully")
                    return True
                else:
                    logger.warning(f"⚠️ API connection issue: {response.status}")
                    return False
        except Exception as e:
            logger.error(f"❌ Failed to connect to API: {e}")
            logger.info("💡 Make sure your MANVUE backend server is running")
            return False

    async def download_image(self, url: str, filename: str = None) -> Tuple[bytes, str, str]:
        """Download image from URL"""
        try:
            logger.info(f"📥 Downloading: {url}")
            
            async with self.session.get(url) as response:
                if response.status == 200:
                    image_data = await response.read()
                    content_type = response.headers.get('content-type', 'image/jpeg')
                    
                    if not filename:
                        parsed_url = urlparse(url)
                        filename = os.path.basename(parsed_url.path)
                        if not filename or '.' not in filename:
                            ext = content_type.split('/')[-1] if '/' in content_type else 'jpg'
                            filename = f"image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{ext}"
                    
                    logger.info(f"✅ Downloaded: {filename} ({len(image_data)} bytes)")
                    return image_data, filename, content_type
                else:
                    raise Exception(f"HTTP {response.status}: {response.reason}")
                    
        except Exception as e:
            logger.error(f"❌ Failed to download {url}: {e}")
            raise

    async def upload_to_gridfs(self, image_data: bytes, filename: str, content_type: str, metadata: Dict = None) -> str:
        """Upload image to GridFS via API"""
        try:
            # Convert to base64 for API upload
            img_b64 = base64.b64encode(image_data).decode('utf-8')
            
            # Prepare form data
            data = {
                'image_data': img_b64,
                'filename': filename
            }
            
            if metadata:
                data.update(metadata)
            
            # Upload to API
            async with self.session.post(
                f"{self.api_base_url}/api/images/upload-base64",
                data=data,
                timeout=30
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    file_id = result['file_id']
                    logger.info(f"💾 Stored in GridFS: {filename} (ID: {file_id})")
                    return file_id
                else:
                    error_text = await response.text()
                    raise Exception(f"Upload failed: {response.status} - {error_text}")
                    
        except Exception as e:
            logger.error(f"❌ Failed to store {filename} in GridFS: {e}")
            raise

    async def convert_url_to_gridfs(self, url: str, custom_filename: str = None, metadata: Dict = None) -> str:
        """Download image from URL and store in GridFS"""
        try:
            # Download image
            image_data, filename, content_type = await self.download_image(url, custom_filename)
            
            # Store in GridFS
            file_id = await self.upload_to_gridfs(image_data, filename, content_type, metadata)
            
            self.downloaded_images.append({
                "original_url": url,
                "filename": filename,
                "file_id": file_id,
                "content_type": content_type
            })
            
            return file_id
            
        except Exception as e:
            self.failed_downloads.append({
                "url": url,
                "error": str(e)
            })
            raise

    async def convert_product_images(self, product_data: Dict) -> Dict:
        """Convert all images for a product from URLs to GridFS IDs"""
        logger.info(f"\n🔄 Converting images for product: {product_data.get('name', 'Unknown')}")
        
        image_ids = []
        product_name = product_data.get('name', 'unknown_product')
        
        for i, url in enumerate(product_data.get('image_urls', [])):
            try:
                # Create meaningful filename
                filename = f"{product_name.lower().replace(' ', '_')}_image_{i+1}.jpg"
                
                # Add product metadata
                metadata = {
                    "product_name": product_data.get('name'),
                    "product_category": product_data.get('category'),
                    "product_type": product_data.get('type'),
                    "image_index": i,
                    "original_url": url
                }
                
                # Convert URL to GridFS
                file_id = await self.convert_url_to_gridfs(url, filename, metadata)
                image_ids.append(file_id)
                
            except Exception as e:
                logger.warning(f"⚠️ Skipping failed image: {url}")
                continue
        
        # Update product data
        product_data['image_ids'] = image_ids
        logger.info(f"✅ Converted {len(image_ids)} images for {product_data.get('name')}")
        
        return product_data

    def print_summary(self):
        """Print conversion summary"""
        logger.info(f"\n📊 Image Conversion Summary:")
        logger.info(f"✅ Successfully downloaded: {len(self.downloaded_images)} images")
        logger.info(f"❌ Failed downloads: {len(self.failed_downloads)} images")
        
        if self.downloaded_images:
            logger.info(f"\n📁 Downloaded Images:")
            for img in self.downloaded_images:
                logger.info(f"  - {img['filename']} (ID: {img['file_id']})")
        
        if self.failed_downloads:
            logger.info(f"\n⚠️ Failed Downloads:")
            for fail in self.failed_downloads:
                logger.info(f"  - {fail['url']}: {fail['error']}")

# Sample product data (same as other scripts)
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
        "image_ids": [],
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

async def convert_all_product_images_colab(api_url: str = "http://localhost:5001"):
    """Convert all sample product images to GridFS (Colab version)"""
    logger.info("🚀 Starting MANVUE image conversion for Colab...")
    
    async with ColabImageConverter(api_url) as converter:
        # Test API connection
        if not await converter.test_api_connection():
            logger.error("❌ Cannot connect to MANVUE API. Please check your server.")
            return None
        
        converted_products = []
        
        for product in SAMPLE_PRODUCTS:
            try:
                converted_product = await converter.convert_product_images(product)
                converted_products.append(converted_product)
            except Exception as e:
                logger.error(f"❌ Failed to convert images for {product.get('name', 'Unknown')}: {e}")
        
        # Print summary
        converter.print_summary()
        
        # Save converted product data
        output_file = "converted_products_colab.json"
        with open(output_file, 'w') as f:
            json.dump(converted_products, f, indent=2, default=str)
        
        logger.info(f"\n💾 Converted product data saved to: {output_file}")
        logger.info(f"🎉 Image conversion completed!")
        
        return converted_products

# Colab-specific functions
def setup_colab_environment():
    """Setup Colab environment for MANVUE"""
    logger.info("🔧 Setting up Colab environment for MANVUE...")
    
    # Install required packages
    import subprocess
    import sys
    
    packages = [
        "aiohttp",
        "motor", 
        "pymongo",
        "python-dotenv",
        "pillow"
    ]
    
    for package in packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            logger.info(f"✅ Installed {package}")
        except subprocess.CalledProcessError:
            logger.warning(f"⚠️ Failed to install {package}")
    
    logger.info("✅ Colab environment setup complete!")

def run_colab_setup(api_url: str = "http://localhost:5001"):
    """Run the complete setup in Colab"""
    logger.info("🚀 MANVUE Colab Image Setup")
    logger.info("=" * 40)
    
    # Setup environment
    setup_colab_environment()
    
    # Run conversion
    converted_products = asyncio.run(convert_all_product_images_colab(api_url))
    
    if converted_products:
        logger.info("\n🎉 Setup completed successfully!")
        logger.info("Your images are now stored in MongoDB GridFS.")
        logger.info("You can now use the product data with GridFS image IDs.")
        
        # Display sample results
        logger.info("\n📋 Sample Results:")
        for product in converted_products[:2]:  # Show first 2 products
            logger.info(f"Product: {product['name']}")
            logger.info(f"  - {len(product['image_ids'])} images converted")
            logger.info(f"  - Image IDs: {product['image_ids'][:2]}...")  # Show first 2 IDs
        
        return converted_products
    else:
        logger.error("\n💥 Setup failed. Please check the output above.")
        return None

# Example usage for Colab
if __name__ == "__main__":
    # This will run when executed in Colab
    print("MANVUE Colab Image Setup")
    print("=" * 30)
    print("To use this script in Colab:")
    print("1. Upload this file to your Colab environment")
    print("2. Make sure your MANVUE API server is running")
    print("3. Run: run_colab_setup('http://your-api-url')")
    print()
    print("Example:")
    print("  run_colab_setup('http://localhost:5001')")
    print("  # or")
    print("  run_colab_setup('https://your-deployed-api.com')")
