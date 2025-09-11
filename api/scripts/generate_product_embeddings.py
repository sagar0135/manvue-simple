#!/usr/bin/env python3
"""
Script to generate CLIP embeddings for existing products
This script processes all products in the database and generates embeddings for their images
"""

import asyncio
import logging
import sys
import os
from typing import List, Dict, Any

# Add parent directories to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from backend.database import (
    get_products, 
    store_product_embedding, 
    get_product_embedding,
    test_connection
)
from backend.ml_model import get_image_embedding, is_model_loaded
import requests
from PIL import Image
import io

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProductEmbeddingGenerator:
    """Generate embeddings for product images"""
    
    def __init__(self):
        self.processed_count = 0
        self.error_count = 0
        self.skipped_count = 0
    
    async def download_image(self, image_url: str) -> bytes:
        """
        Download image from URL
        
        Args:
            image_url: Image URL
            
        Returns:
            bytes: Image data
        """
        try:
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()
            return response.content
        except Exception as e:
            logger.error(f"Error downloading image {image_url}: {e}")
            return None
    
    async def generate_embedding_for_product(self, product: Dict[str, Any]) -> bool:
        """
        Generate embedding for a single product
        
        Args:
            product: Product data
            
        Returns:
            bool: True if successful
        """
        try:
            product_id = str(product.get("_id", product.get("id")))
            
            # Check if embedding already exists
            existing_embedding = await get_product_embedding(product_id)
            if existing_embedding:
                logger.info(f"Embedding already exists for product {product_id}, skipping")
                self.skipped_count += 1
                return True
            
            # Get image URL
            image_url = product.get("image_url") or product.get("image")
            if not image_url:
                logger.warning(f"No image URL for product {product_id}, skipping")
                self.skipped_count += 1
                return False
            
            # Download image
            image_data = await self.download_image(image_url)
            if not image_data:
                logger.error(f"Failed to download image for product {product_id}")
                self.error_count += 1
                return False
            
            # Save image temporarily
            temp_path = f"/tmp/temp_product_{product_id}_{self.processed_count}.jpg"
            with open(temp_path, 'wb') as f:
                f.write(image_data)
            
            try:
                # Generate embedding
                embedding = get_image_embedding(temp_path)
                
                # Store embedding
                success = await store_product_embedding(product_id, embedding)
                
                if success:
                    logger.info(f"Generated embedding for product {product_id}")
                    self.processed_count += 1
                    return True
                else:
                    logger.error(f"Failed to store embedding for product {product_id}")
                    self.error_count += 1
                    return False
                    
            finally:
                # Clean up temp file
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
        
        except Exception as e:
            logger.error(f"Error processing product {product_id}: {e}")
            self.error_count += 1
            return False
    
    async def generate_all_embeddings(self, batch_size: int = 10):
        """
        Generate embeddings for all products
        
        Args:
            batch_size: Number of products to process in parallel
        """
        try:
            # Check if CLIP model is loaded
            if not is_model_loaded():
                logger.error("CLIP model not loaded. Please ensure the model is available.")
                return
            
            # Get all products
            logger.info("Fetching all products...")
            products = await get_products(limit=1000)  # Adjust limit as needed
            
            if not products:
                logger.warning("No products found in database")
                return
            
            logger.info(f"Found {len(products)} products to process")
            
            # Process products in batches
            for i in range(0, len(products), batch_size):
                batch = products[i:i + batch_size]
                logger.info(f"Processing batch {i//batch_size + 1}/{(len(products) + batch_size - 1)//batch_size}")
                
                # Process batch concurrently
                tasks = [self.generate_embedding_for_product(product) for product in batch]
                await asyncio.gather(*tasks, return_exceptions=True)
                
                # Small delay between batches
                await asyncio.sleep(1)
            
            # Print summary
            logger.info("=" * 50)
            logger.info("EMBEDDING GENERATION SUMMARY")
            logger.info("=" * 50)
            logger.info(f"Total products: {len(products)}")
            logger.info(f"Successfully processed: {self.processed_count}")
            logger.info(f"Already had embeddings: {self.skipped_count}")
            logger.info(f"Errors: {self.error_count}")
            logger.info("=" * 50)
            
        except Exception as e:
            logger.error(f"Error in generate_all_embeddings: {e}")

async def main():
    """Main function"""
    try:
        # Test database connection
        if not await test_connection():
            logger.error("Failed to connect to database")
            return
        
        # Create generator and run
        generator = ProductEmbeddingGenerator()
        await generator.generate_all_embeddings()
        
    except Exception as e:
        logger.error(f"Error in main: {e}")

if __name__ == "__main__":
    print("🚀 Starting Product Embedding Generation...")
    print("📊 This will generate CLIP embeddings for all product images")
    print("⏱️  This process may take several minutes depending on the number of products")
    print()
    
    asyncio.run(main())
