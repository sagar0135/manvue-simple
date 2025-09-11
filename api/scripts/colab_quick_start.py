#!/usr/bin/env python3
"""
MANVUE Colab Quick Start Script
One-click setup for Google Colab environment
"""

import asyncio
import aiohttp
import base64
import json
import logging
from typing import Dict, List, Any

# Configure logging for Colab
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class MANVUEColabQuickStart:
    """Quick start class for MANVUE in Colab"""
    
    def __init__(self, api_url: str = "http://localhost:5001"):
        self.api_url = api_url.rstrip('/')
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def test_connection(self) -> bool:
        """Test connection to MANVUE API"""
        try:
            async with self.session.get(f"{self.api_url}/health", timeout=10) as response:
                if response.status == 200:
                    logger.info("✅ Connected to MANVUE API")
                    return True
                else:
                    logger.warning(f"⚠️ API issue: {response.status}")
                    return False
        except Exception as e:
            logger.error(f"❌ Connection failed: {e}")
            return False

    async def upload_image_from_url(self, url: str, filename: str, category: str = None) -> str:
        """Upload image from URL to GridFS"""
        try:
            # Download image
            async with self.session.get(url) as response:
                if response.status == 200:
                    image_data = await response.read()
                else:
                    raise Exception(f"Download failed: {response.status}")
            
            # Convert to base64
            img_b64 = base64.b64encode(image_data).decode('utf-8')
            
            # Upload to API
            data = {
                'image_data': img_b64,
                'filename': filename
            }
            if category:
                data['category'] = category
            
            async with self.session.post(
                f"{self.api_url}/api/images/upload-base64",
                data=data,
                timeout=30
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return result['file_id']
                else:
                    raise Exception(f"Upload failed: {response.status}")
                    
        except Exception as e:
            logger.error(f"❌ Upload error: {e}")
            raise

    async def create_product_with_images(self, product_data: Dict, image_urls: List[str]) -> Dict:
        """Create product with images"""
        try:
            # Upload images
            image_ids = []
            for i, url in enumerate(image_urls):
                filename = f"{product_data['name'].lower().replace(' ', '_')}_image_{i+1}.jpg"
                file_id = await self.upload_image_from_url(url, filename, product_data.get('category'))
                image_ids.append(file_id)
            
            # Add image references
            product_data['image_ids'] = image_ids
            
            # Create product
            async with self.session.post(
                f"{self.api_url}/api/products",
                json=product_data,
                timeout=30
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"Product creation failed: {response.status}")
                    
        except Exception as e:
            logger.error(f"❌ Product creation error: {e}")
            raise

async def quick_setup_manvue(api_url: str = "http://localhost:5001"):
    """Quick setup for MANVUE in Colab"""
    logger.info("🚀 MANVUE Colab Quick Start")
    logger.info("=" * 30)
    
    # Sample product data
    sample_products = [
        {
            "name": "Classic Cotton Crew Neck",
            "price": 24.99,
            "category": "men",
            "type": "tops",
            "size": ["XS", "S", "M", "L", "XL"],
            "color": ["Black", "White", "Navy"],
            "brand": "MANVUE Basics",
            "rating": 4.5,
            "reviews": 342,
            "description": "Comfortable 100% cotton crew neck t-shirt",
            "tags": ["casual", "cotton", "basic"]
        },
        {
            "name": "Premium Denim Jeans",
            "price": 64.99,
            "category": "men", 
            "type": "bottoms",
            "size": ["30", "32", "34", "36", "38"],
            "color": ["Dark Blue", "Black", "Light Blue"],
            "brand": "MANVUE Denim",
            "rating": 4.7,
            "reviews": 189,
            "description": "Premium denim jeans with slim fit",
            "tags": ["denim", "classic", "slim-fit"]
        }
    ]
    
    # Sample image URLs
    image_urls = [
        "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=500&fit=crop&auto=format",
        "https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=400&h=500&fit=crop&auto=format",
        "https://images.unsplash.com/photo-1503341504253-dff4815485f1?w=400&h=500&fit=crop&auto=format"
    ]
    
    async with MANVUEColabQuickStart(api_url) as quick_start:
        # Test connection
        if not await quick_start.test_connection():
            logger.error("❌ Cannot connect to MANVUE API")
            return None
        
        created_products = []
        
        # Create products with images
        for product in sample_products:
            try:
                logger.info(f"Creating product: {product['name']}")
                result = await quick_start.create_product_with_images(product, image_urls)
                created_products.append(result)
                logger.info(f"✅ Created: {result['id']}")
            except Exception as e:
                logger.error(f"❌ Failed to create {product['name']}: {e}")
        
        if created_products:
            logger.info(f"\n🎉 Successfully created {len(created_products)} products!")
            logger.info("Your images are now stored in MongoDB GridFS.")
            
            # Save results
            with open('manvue_products.json', 'w') as f:
                json.dump(created_products, f, indent=2, default=str)
            
            logger.info("💾 Product data saved to 'manvue_products.json'")
            return created_products
        else:
            logger.error("❌ No products were created")
            return None

# Colab-friendly functions
def install_dependencies():
    """Install required packages in Colab"""
    import subprocess
    import sys
    
    packages = ["aiohttp", "motor", "pymongo", "python-dotenv", "pillow"]
    
    for package in packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            logger.info(f"✅ Installed {package}")
        except subprocess.CalledProcessError:
            logger.warning(f"⚠️ Failed to install {package}")

def run_quick_setup(api_url: str = "http://localhost:5001"):
    """Run quick setup (Colab-friendly)"""
    logger.info("🔧 Installing dependencies...")
    install_dependencies()
    
    logger.info("🚀 Starting quick setup...")
    return asyncio.run(quick_setup_manvue(api_url))

# Example usage
if __name__ == "__main__":
    print("MANVUE Colab Quick Start")
    print("=" * 25)
    print("To use in Colab:")
    print("1. Upload this script to Colab")
    print("2. Run: run_quick_setup('http://your-api-url')")
    print()
    print("Example:")
    print("  run_quick_setup('http://localhost:5001')")
    print("  # or")
    print("  run_quick_setup('https://your-deployed-api.com')")
