"""
Local Image Processor Service
Handles local image processing, copying, and embedding generation for dataset integration
"""

import requests
from PIL import Image
from io import BytesIO
import time
import pandas as pd
import os
import shutil
from tqdm import tqdm
from typing import List, Dict, Optional, Any
import logging

# Configure logging
logger = logging.getLogger(__name__)

class LocalImageProcessor:
    """
    Service for processing local images and integrating them with the ManVue website
    """
    
    def __init__(self, local_base_url="http://127.0.0.1:5500", images_folder="frontend/images"):
        """
        Initialize the LocalImageProcessor
        
        Args:
            local_base_url: Base URL for the local development server
            images_folder: Folder name for images in the frontend
        """
        self.local_base_url = local_base_url
        self.images_folder = images_folder
        self.full_images_path = os.path.join(os.getcwd(), images_folder)
        
        # Create images directory if it doesn't exist
        os.makedirs(self.full_images_path, exist_ok=True)
        logger.info(f"🖼️ Images will be served from: {self.full_images_path}")
        logger.info(f"🌐 Base URL: {self.local_base_url}/{images_folder}/")

    def copy_dataset_images_to_website(self, df: pd.DataFrame, source_image_dir: str, num_samples: int = 10) -> List[Dict[str, Any]]:
        """
        Copy images from your dataset to the website's images folder
        
        Args:
            df: DataFrame containing product information
            source_image_dir: Path to source images directory
            num_samples: Number of samples to process
            
        Returns:
            List of copied product dictionaries
        """
        logger.info(f"📁 Copying images from: {source_image_dir}")
        logger.info(f"📁 To website folder: {self.full_images_path}")
        
        # Get sample from DataFrame
        sample_df = df.sample(n=min(num_samples, len(df)))
        
        copied_products = []
        successful_copies = 0
        failed_copies = 0
        
        for index, row in sample_df.iterrows():
            source_path = os.path.join(source_image_dir, row['image'])
            dest_path = os.path.join(self.full_images_path, row['image'])
            
            try:
                if os.path.exists(source_path):
                    # Copy image to website folder
                    shutil.copy2(source_path, dest_path)
                    
                    # Create product dict
                    product = {
                        "title": row.get('display name', f"Product {index}"),
                        "description": row.get('description', 'No description available'),
                        "category": row.get('category', 'Unknown'),
                        "image_filename": row['image'],
                        "image_url": f"{self.local_base_url}/{self.images_folder}/{row['image']}",
                        "local_path": dest_path
                    }
                    copied_products.append(product)
                    successful_copies += 1
                    logger.info(f"✅ Copied: {row['image']}")
                else:
                    failed_copies += 1
                    logger.warning(f"❌ Source not found: {source_path}")
                    
            except Exception as e:
                failed_copies += 1
                logger.error(f"❌ Error copying {row['image']}: {e}")
        
        logger.info(f"📊 Copy Summary:")
        logger.info(f"✅ Successfully copied: {successful_copies}")
        logger.info(f"❌ Failed to copy: {failed_copies}")
        
        return copied_products

    def get_image_embedding_local(self, image_url: str, max_retries: int = 3) -> Optional[Image.Image]:
        """
        Get image embedding from local server with error handling
        
        Args:
            image_url: URL of the image to process
            max_retries: Maximum number of retry attempts
            
        Returns:
            PIL Image object or None if failed
        """
        for attempt in range(max_retries):
            try:
                logger.info(f"🔗 Attempting to fetch: {image_url}")
                
                # Add headers to mimic browser request
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                
                response = requests.get(image_url, timeout=10, headers=headers)
                response.raise_for_status()
                
                # Check content
                if len(response.content) == 0:
                    logger.warning(f"❌ Empty content")
                    return None
                
                if len(response.content) < 100:
                    logger.warning(f"❌ Content too small ({len(response.content)} bytes)")
                    return None
                
                # Check if it's HTML (404 page)
                if response.content.startswith(b'<!DOCTYPE') or response.content.startswith(b'<html'):
                    logger.warning(f"❌ Received HTML instead of image")
                    return None
                
                # Try to open image
                image_bytes = BytesIO(response.content)
                image = Image.open(image_bytes)
                image.verify()
                
                # Reopen for processing
                image_bytes.seek(0)
                image = Image.open(image_bytes)
                
                # Convert to RGB if needed
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                
                logger.info(f"✅ Successfully loaded image: {image.size}")
                
                # YOUR EMBEDDING LOGIC HERE
                # Replace this with your actual embedding function:
                # embedding = your_embedding_model(image)
                # return embedding
                
                return image  # Return image object for now
                
            except requests.exceptions.ConnectionError:
                logger.error(f"🔌 Connection failed - is your local server running?")
                logger.info(f"💡 Make sure to start your server: python -m http.server 5500 or use Live Server")
            except requests.exceptions.RequestException as e:
                logger.error(f"🌐 Network error (attempt {attempt + 1}): {e}")
            except Exception as e:
                logger.error(f"❌ Error (attempt {attempt + 1}): {e}")
            
            if attempt < max_retries - 1:
                logger.info(f"⏳ Retrying in 2 seconds...")
                time.sleep(2)
        
        return None

    def process_local_images_directly(self, df: pd.DataFrame, source_image_dir: str, num_samples: int = 5) -> List[Dict[str, Any]]:
        """
        Process images directly from local filesystem (bypass HTTP server)
        
        Args:
            df: DataFrame containing product information
            source_image_dir: Path to source images directory
            num_samples: Number of samples to process
            
        Returns:
            List of processed document dictionaries
        """
        logger.info(f"📁 Processing images directly from: {source_image_dir}")
        
        sample_df = df.sample(n=min(num_samples, len(df)))
        docs = []
        successful = 0
        failed = 0
        
        for index, row in sample_df.iterrows():
            image_path = os.path.join(source_image_dir, row['image'])
            
            logger.info(f"📦 Processing: {row.get('display name', f'Product {index}')}")
            logger.info(f"📂 File: {row['image']}")
            
            try:
                if os.path.exists(image_path):
                    # Open image directly from filesystem
                    with Image.open(image_path) as image:
                        if image.mode != 'RGB':
                            image = image.convert('RGB')
                        
                        logger.info(f"✅ Loaded image: {image.size}")
                        
                        # YOUR EMBEDDING LOGIC HERE
                        # embedding = your_embedding_model(image)
                        
                        doc = {
                            "title": row.get('display name', f"Product {index}"),
                            "description": row.get('description', 'No description'),
                            "category": row.get('category', 'Unknown'),
                            "image_filename": row['image'],
                            "local_path": image_path,
                            "image_url": f"{self.local_base_url}/{self.images_folder}/{row['image']}",
                            "embedding": image,  # Replace with actual embedding
                            "status": "success"
                        }
                        docs.append(doc)
                        successful += 1
                        logger.info(f"✅ Successfully processed!")
                        
                else:
                    logger.warning(f"❌ Image file not found: {image_path}")
                    failed += 1
                    
            except Exception as e:
                logger.error(f"❌ Error processing {row['image']}: {e}")
                failed += 1
        
        logger.info(f"📊 Processing Summary:")
        logger.info(f"✅ Successful: {successful}")
        logger.info(f"❌ Failed: {failed}")
        logger.info(f"📄 Total documents: {len(docs)}")
        
        return docs

    def setup_local_website_images(self, df: pd.DataFrame, source_image_dir: str, num_samples: int = 5) -> List[Dict[str, Any]]:
        """
        Complete setup for local website with dataset images
        
        Args:
            df: DataFrame containing product information
            source_image_dir: Path to source images directory
            num_samples: Number of samples to process
            
        Returns:
            List of processed document dictionaries
        """
        logger.info("🚀 Setting up local website with dataset images...")
        logger.info("=" * 60)
        
        # Method 1: Copy images to website folder and serve via HTTP
        logger.info("🔄 Method 1: Copying images to website folder...")
        products = self.copy_dataset_images_to_website(df, source_image_dir, num_samples)
        
        if products:
            logger.info(f"🌐 Images are now available at URLs like:")
            for product in products[:3]:  # Show first 3
                logger.info(f"  {product['image_url']}")
            
            logger.info(f"💡 To test in browser, visit:")
            logger.info(f"  http://127.0.0.1:5500/{self.images_folder}/{products[0]['image_filename']}")
            
            # Now process via HTTP
            logger.info(f"🔄 Processing images via HTTP server...")
            docs_http = []
            for product in products:
                emb = self.get_image_embedding_local(product['image_url'])
                if emb is not None:
                    product['embedding'] = emb
                    docs_http.append(product)
            
            logger.info(f"✅ HTTP method: {len(docs_http)} successful")
        
        # Method 2: Process directly from source (recommended)
        logger.info(f"🔄 Method 2: Processing directly from source...")
        docs_direct = self.process_local_images_directly(df, source_image_dir, num_samples)
        logger.info(f"✅ Direct method: {len(docs_direct)} successful")
        
        return docs_direct  # Return the more reliable direct method results

    def validate_image(self, image_path: str) -> bool:
        """
        Validate that an image file is valid and can be opened
        
        Args:
            image_path: Path to the image file
            
        Returns:
            True if image is valid, False otherwise
        """
        try:
            with Image.open(image_path) as img:
                img.verify()
            return True
        except Exception as e:
            logger.error(f"Invalid image {image_path}: {e}")
            return False

    def get_image_info(self, image_path: str) -> Optional[Dict[str, Any]]:
        """
        Get basic information about an image file
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Dictionary with image information or None if invalid
        """
        try:
            with Image.open(image_path) as img:
                return {
                    "size": img.size,
                    "mode": img.mode,
                    "format": img.format,
                    "file_size": os.path.getsize(image_path)
                }
        except Exception as e:
            logger.error(f"Error getting image info for {image_path}: {e}")
            return None
