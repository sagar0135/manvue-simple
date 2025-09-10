"""
ManVue Colab Integration Script
Easy image upload from Google Colab to ManVue MongoDB backend

Usage in Colab:
1. Upload this script to your Colab environment
2. Import and configure the ManVueImageUploader
3. Upload images directly from your ML training pipeline

Example:
    from colab_integration import ManVueImageUploader
    
    uploader = ManVueImageUploader("http://your-manvue-api-url.com")
    result = uploader.upload_image("path/to/image.jpg", category="shoes")
    print(f"Image uploaded: {result['image_url']}")
"""

import requests
import base64
import json
import os
from io import BytesIO
from PIL import Image
import logging
from typing import Optional, Dict, Any, List
import matplotlib.pyplot as plt
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ManVueImageUploader:
    """
    A helper class for uploading images from Colab to ManVue backend
    """
    
    def __init__(self, api_base_url: str = "http://localhost:5001", timeout: int = 30):
        """
        Initialize the uploader
        
        Args:
            api_base_url: Base URL of your ManVue API
            timeout: Request timeout in seconds
        """
        self.api_base_url = api_base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        
        # Test connection
        self._test_connection()
    
    def _test_connection(self):
        """Test connection to the API"""
        try:
            response = self.session.get(f"{self.api_base_url}/health", timeout=self.timeout)
            if response.status_code == 200:
                logger.info("✅ Connected to ManVue API successfully")
                health_data = response.json()
                logger.info(f"API Status: {health_data.get('status')}")
                logger.info(f"Database: {health_data.get('database')}")
                logger.info(f"ML Available: {health_data.get('ml_available')}")
            else:
                logger.warning(f"⚠️ API connection issue: {response.status_code}")
        except Exception as e:
            logger.error(f"❌ Failed to connect to API: {e}")
            logger.info("💡 Make sure your ManVue backend server is running")
    
    def upload_image_file(self, 
                         image_path: str, 
                         category: Optional[str] = None,
                         product_id: Optional[str] = None,
                         resize_max: int = 1920) -> Dict[str, Any]:
        """
        Upload an image file to ManVue backend
        
        Args:
            image_path: Path to the image file
            category: Product category (e.g., 'shoes', 'tops', 'bottoms')
            product_id: Associated product ID (if any)
            resize_max: Maximum dimension for resizing (0 to skip resizing)
        
        Returns:
            dict: Upload response with file_id, image_url, etc.
        """
        try:
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image file not found: {image_path}")
            
            # Open and optionally resize image
            with Image.open(image_path) as img:
                # Convert to RGB if necessary
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                
                # Resize if needed
                if resize_max > 0 and (img.width > resize_max or img.height > resize_max):
                    img.thumbnail((resize_max, resize_max), Image.Resampling.LANCZOS)
                    logger.info(f"Resized image to {img.size}")
                
                # Convert to bytes
                img_bytes = BytesIO()
                img.save(img_bytes, format='JPEG', quality=85)
                img_bytes = img_bytes.getvalue()
            
            # Prepare form data
            files = {
                'file': (os.path.basename(image_path), img_bytes, 'image/jpeg')
            }
            
            data = {}
            if category:
                data['category'] = category
            if product_id:
                data['product_id'] = product_id
            
            # Upload to API
            response = self.session.post(
                f"{self.api_base_url}/api/images/upload",
                files=files,
                data=data,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"✅ Image uploaded successfully: {result['file_id']}")
                return result
            else:
                error_msg = f"Upload failed: {response.status_code} - {response.text}"
                logger.error(error_msg)
                raise Exception(error_msg)
                
        except Exception as e:
            logger.error(f"❌ Upload error: {e}")
            raise
    
    def upload_image_array(self, 
                          image_array: np.ndarray, 
                          filename: str = "colab_image.jpg",
                          category: Optional[str] = None,
                          product_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Upload a numpy array as an image
        
        Args:
            image_array: Numpy array representing the image
            filename: Filename for the uploaded image
            category: Product category
            product_id: Associated product ID
        
        Returns:
            dict: Upload response
        """
        try:
            # Convert numpy array to PIL Image
            if image_array.dtype != np.uint8:
                # Normalize if needed
                if image_array.max() <= 1.0:
                    image_array = (image_array * 255).astype(np.uint8)
                else:
                    image_array = image_array.astype(np.uint8)
            
            # Handle different array shapes
            if len(image_array.shape) == 3 and image_array.shape[2] == 3:
                # RGB image
                img = Image.fromarray(image_array, 'RGB')
            elif len(image_array.shape) == 2:
                # Grayscale image
                img = Image.fromarray(image_array, 'L')
                img = img.convert('RGB')  # Convert to RGB for consistency
            else:
                raise ValueError(f"Unsupported array shape: {image_array.shape}")
            
            # Convert to base64
            img_bytes = BytesIO()
            img.save(img_bytes, format='JPEG', quality=85)
            img_b64 = base64.b64encode(img_bytes.getvalue()).decode('utf-8')
            
            return self.upload_image_base64(img_b64, filename, category, product_id)
            
        except Exception as e:
            logger.error(f"❌ Array upload error: {e}")
            raise
    
    def upload_image_base64(self, 
                           image_base64: str, 
                           filename: str = "colab_image.jpg",
                           category: Optional[str] = None,
                           product_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Upload a base64 encoded image
        
        Args:
            image_base64: Base64 encoded image data
            filename: Filename for the uploaded image
            category: Product category
            product_id: Associated product ID
        
        Returns:
            dict: Upload response
        """
        try:
            # Prepare form data
            data = {
                'image_data': image_base64,
                'filename': filename
            }
            
            if category:
                data['category'] = category
            if product_id:
                data['product_id'] = product_id
            
            # Upload to API
            response = self.session.post(
                f"{self.api_base_url}/api/images/upload-base64",
                data=data,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"✅ Base64 image uploaded successfully: {result['file_id']}")
                return result
            else:
                error_msg = f"Upload failed: {response.status_code} - {response.text}"
                logger.error(error_msg)
                raise Exception(error_msg)
                
        except Exception as e:
            logger.error(f"❌ Base64 upload error: {e}")
            raise
    
    def upload_from_url(self, 
                       image_url: str, 
                       filename: Optional[str] = None,
                       category: Optional[str] = None,
                       product_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Download and upload an image from a URL
        
        Args:
            image_url: URL of the image to download
            filename: Filename for the uploaded image
            category: Product category
            product_id: Associated product ID
        
        Returns:
            dict: Upload response
        """
        try:
            # Download image
            response = requests.get(image_url, timeout=self.timeout)
            response.raise_for_status()
            
            # Get filename from URL if not provided
            if not filename:
                filename = os.path.basename(image_url.split('?')[0]) or "downloaded_image.jpg"
            
            # Convert to base64
            img_b64 = base64.b64encode(response.content).decode('utf-8')
            
            return self.upload_image_base64(img_b64, filename, category, product_id)
            
        except Exception as e:
            logger.error(f"❌ URL upload error: {e}")
            raise
    
    def create_product_with_images(self, 
                                  product_data: Dict[str, Any], 
                                  image_paths: List[str]) -> Dict[str, Any]:
        """
        Create a new product and upload associated images
        
        Args:
            product_data: Product information
            image_paths: List of image file paths
        
        Returns:
            dict: Created product data with image URLs
        """
        try:
            # Upload images first
            image_ids = []
            image_urls = []
            
            for image_path in image_paths:
                upload_result = self.upload_image_file(
                    image_path, 
                    category=product_data.get('category')
                )
                image_ids.append(upload_result['file_id'])
                image_urls.append(upload_result['image_url'])
            
            # Add image references to product data
            product_data['image_ids'] = image_ids
            product_data['image_urls'] = image_urls
            
            # Create product
            response = self.session.post(
                f"{self.api_base_url}/products",
                json=product_data,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"✅ Product created successfully: {result['id']}")
                return result
            else:
                error_msg = f"Product creation failed: {response.status_code} - {response.text}"
                logger.error(error_msg)
                raise Exception(error_msg)
                
        except Exception as e:
            logger.error(f"❌ Product creation error: {e}")
            raise
    
    def list_uploaded_images(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List uploaded images
        
        Args:
            category: Filter by category
        
        Returns:
            list: List of image metadata
        """
        try:
            params = {}
            if category:
                params['category'] = category
            
            response = self.session.get(
                f"{self.api_base_url}/api/images",
                params=params,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                images = response.json()
                logger.info(f"Found {len(images)} images")
                return images
            else:
                error_msg = f"List failed: {response.status_code} - {response.text}"
                logger.error(error_msg)
                raise Exception(error_msg)
                
        except Exception as e:
            logger.error(f"❌ List error: {e}")
            raise
    
    def display_uploaded_image(self, file_id: str, figsize: tuple = (8, 8)):
        """
        Display an uploaded image in Colab
        
        Args:
            file_id: GridFS file ID
            figsize: Figure size for matplotlib
        """
        try:
            response = self.session.get(
                f"{self.api_base_url}/api/images/{file_id}",
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                
                plt.figure(figsize=figsize)
                plt.imshow(img)
                plt.axis('off')
                plt.title(f"Image ID: {file_id}")
                plt.show()
            else:
                logger.error(f"Failed to load image: {response.status_code}")
                
        except Exception as e:
            logger.error(f"❌ Display error: {e}")

# Convenience functions for quick usage
def quick_upload(image_path: str, 
                api_url: str = "http://localhost:5001", 
                category: str = None) -> str:
    """
    Quick upload function for single images
    
    Returns:
        str: Image URL
    """
    uploader = ManVueImageUploader(api_url)
    result = uploader.upload_image_file(image_path, category=category)
    return result['image_url']

def batch_upload(image_paths: List[str], 
                api_url: str = "http://localhost:5001", 
                category: str = None) -> List[str]:
    """
    Batch upload multiple images
    
    Returns:
        list: List of image URLs
    """
    uploader = ManVueImageUploader(api_url)
    urls = []
    
    for path in image_paths:
        try:
            result = uploader.upload_image_file(path, category=category)
            urls.append(result['image_url'])
        except Exception as e:
            logger.error(f"Failed to upload {path}: {e}")
            urls.append(None)
    
    return urls

# Example usage in Colab
if __name__ == "__main__":
    # This section shows example usage
    print("ManVue Colab Integration - Example Usage")
    print("=" * 50)
    
    # Example 1: Basic upload
    print("\n1. Basic Image Upload:")
    print("""
    from colab_integration import ManVueImageUploader
    
    # Initialize uploader
    uploader = ManVueImageUploader("http://your-api-url.com")
    
    # Upload an image
    result = uploader.upload_image_file(
        "path/to/your/image.jpg", 
        category="shoes"
    )
    print(f"Uploaded: {result['image_url']}")
    """)
    
    # Example 2: Upload from numpy array
    print("\n2. Upload from NumPy Array:")
    print("""
    import numpy as np
    
    # Generate or load your image array
    image_array = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
    
    # Upload the array
    result = uploader.upload_image_array(
        image_array, 
        filename="generated_image.jpg",
        category="tops"
    )
    """)
    
    # Example 3: Create product with images
    print("\n3. Create Product with Images:")
    print("""
    # Product data
    product_data = {
        "name": "Classic White Sneaker",
        "price": 89.99,
        "category": "shoes",
        "type": "sneakers",
        "description": "Comfortable white sneakers for everyday wear",
        "brand": "ManVue",
        "size": ["7", "8", "9", "10", "11"],
        "color": ["White", "Black"],
        "tags": ["casual", "comfortable", "everyday"]
    }
    
    # Image paths
    image_paths = [
        "sneaker_front.jpg",
        "sneaker_side.jpg", 
        "sneaker_back.jpg"
    ]
    
    # Create product with images
    product = uploader.create_product_with_images(product_data, image_paths)
    print(f"Created product: {product['id']}")
    """)
    
    print("\n" + "=" * 50)
    print("For more examples, check the ManVue documentation!")
