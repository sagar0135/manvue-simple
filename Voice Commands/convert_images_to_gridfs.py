#!/usr/bin/env python3
"""
Image Conversion Script for MANVUE
Downloads external images and stores them in MongoDB GridFS
"""

import asyncio
import sys
import os
import aiohttp
import io
from urllib.parse import urlparse
from datetime import datetime
from typing import List, Dict, Tuple

# Add the parent directory to the path to import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from backend.database import store_image, gridfs, test_connection

class ImageConverter:
    def __init__(self):
        self.session = None
        self.downloaded_images = []
        self.failed_downloads = []

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def download_image(self, url: str, filename: str = None) -> Tuple[bytes, str, str]:
        """
        Download image from URL and return image data, filename, and content type
        
        Args:
            url: Image URL
            filename: Optional custom filename
            
        Returns:
            Tuple of (image_bytes, filename, content_type)
        """
        try:
            print(f"📥 Downloading: {url}")
            
            async with self.session.get(url) as response:
                if response.status == 200:
                    image_data = await response.read()
                    
                    # Get content type from response headers
                    content_type = response.headers.get('content-type', 'image/jpeg')
                    
                    # Generate filename if not provided
                    if not filename:
                        parsed_url = urlparse(url)
                        filename = os.path.basename(parsed_url.path)
                        if not filename or '.' not in filename:
                            # Generate filename based on content type
                            ext = content_type.split('/')[-1] if '/' in content_type else 'jpg'
                            filename = f"image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{ext}"
                    
                    print(f"✅ Downloaded: {filename} ({len(image_data)} bytes)")
                    return image_data, filename, content_type
                else:
                    raise Exception(f"HTTP {response.status}: {response.reason}")
                    
        except Exception as e:
            print(f"❌ Failed to download {url}: {e}")
            raise

    async def store_image_in_gridfs(self, image_data: bytes, filename: str, content_type: str, metadata: Dict = None) -> str:
        """
        Store image in GridFS and return the file ID
        """
        try:
            file_metadata = {
                "filename": filename,
                "content_type": content_type,
                "upload_date": datetime.utcnow(),
                "source": "converted_from_external_url",
                **(metadata or {})
            }
            
            file_id = await gridfs.upload_from_stream(
                filename,
                io.BytesIO(image_data),
                metadata=file_metadata
            )
            
            print(f"💾 Stored in GridFS: {filename} (ID: {file_id})")
            return str(file_id)
            
        except Exception as e:
            print(f"❌ Failed to store {filename} in GridFS: {e}")
            raise

    async def convert_url_to_gridfs(self, url: str, custom_filename: str = None, metadata: Dict = None) -> str:
        """
        Download image from URL and store in GridFS
        
        Args:
            url: Image URL to download
            custom_filename: Optional custom filename
            metadata: Additional metadata to store
            
        Returns:
            GridFS file ID
        """
        try:
            # Download image
            image_data, filename, content_type = await self.download_image(url, custom_filename)
            
            # Store in GridFS
            file_id = await self.store_image_in_gridfs(image_data, filename, content_type, metadata)
            
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
        """
        Convert all images for a product from URLs to GridFS IDs
        
        Args:
            product_data: Product data containing image_urls
            
        Returns:
            Updated product data with image_ids filled
        """
        print(f"\n🔄 Converting images for product: {product_data.get('name', 'Unknown')}")
        
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
                print(f"⚠️  Skipping failed image: {url}")
                continue
        
        # Update product data
        product_data['image_ids'] = image_ids
        print(f"✅ Converted {len(image_ids)} images for {product_data.get('name')}")
        
        return product_data

    def print_summary(self):
        """Print conversion summary"""
        print(f"\n📊 Image Conversion Summary:")
        print(f"✅ Successfully downloaded: {len(self.downloaded_images)} images")
        print(f"❌ Failed downloads: {len(self.failed_downloads)} images")
        
        if self.downloaded_images:
            print(f"\n📁 Downloaded Images:")
            for img in self.downloaded_images:
                print(f"  - {img['filename']} (ID: {img['file_id']})")
        
        if self.failed_downloads:
            print(f"\n⚠️  Failed Downloads:")
            for fail in self.failed_downloads:
                print(f"  - {fail['url']}: {fail['error']}")

# Sample product data with external URLs (same as seed_product_data.py)
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

async def convert_all_product_images():
    """Convert all sample product images to GridFS"""
    print("🚀 Starting image conversion to GridFS...")
    
    # Test database connection
    if not await test_connection():
        print("❌ Database connection failed. Please check your MongoDB setup.")
        return
    
    async with ImageConverter() as converter:
        converted_products = []
        
        for product in SAMPLE_PRODUCTS:
            try:
                converted_product = await converter.convert_product_images(product)
                converted_products.append(converted_product)
            except Exception as e:
                print(f"❌ Failed to convert images for {product.get('name', 'Unknown')}: {e}")
        
        # Print summary
        converter.print_summary()
        
        # Save converted product data to file for reference
        import json
        output_file = "converted_products_with_gridfs_ids.json"
        with open(output_file, 'w') as f:
            json.dump(converted_products, f, indent=2, default=str)
        
        print(f"\n💾 Converted product data saved to: {output_file}")
        print(f"🎉 Image conversion completed!")
        
        return converted_products

if __name__ == "__main__":
    asyncio.run(convert_all_product_images())
