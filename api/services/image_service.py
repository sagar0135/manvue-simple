"""
Image Service
Business logic for image management with MongoDB GridFS
"""

import base64
import logging
from typing import List, Optional, Tuple
from datetime import datetime

# Import database functions
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from backend.database import (
    store_image, store_image_base64, get_image, get_image_metadata,
    delete_image as db_delete_image, list_images as db_list_images
)

from ..models.image_models import ImageUploadResponse, ImageMetadataResponse

# Configure logging
logger = logging.getLogger(__name__)

class ImageService:
    """Service for handling image operations"""
    
    def __init__(self):
        self.api_base_url = "http://localhost:5001"  # This should come from config
    
    def _generate_image_url(self, file_id: str) -> str:
        """Generate image URL for given file ID"""
        return f"{self.api_base_url}/api/images/{file_id}"
    
    async def upload_image(
        self, 
        image_data: bytes, 
        filename: str, 
        content_type: str,
        category: Optional[str] = None,
        product_id: Optional[str] = None
    ) -> ImageUploadResponse:
        """
        Upload image to GridFS
        
        Args:
            image_data: Raw image bytes
            filename: Original filename
            content_type: MIME type
            category: Product category
            product_id: Associated product ID
            
        Returns:
            ImageUploadResponse with file details
        """
        try:
            metadata = {
                "category": category,
                "product_id": product_id,
                "original_filename": filename
            }
            
            file_id = await store_image(image_data, filename, content_type, metadata)
            
            return ImageUploadResponse(
                success=True,
                file_id=file_id,
                filename=filename,
                content_type=content_type,
                size=len(image_data),
                image_url=self._generate_image_url(file_id)
            )
        
        except Exception as e:
            logger.error(f"Error uploading image: {e}")
            raise
    
    async def upload_image_base64(
        self,
        image_data: str,
        filename: str,
        category: Optional[str] = None,
        product_id: Optional[str] = None
    ) -> ImageUploadResponse:
        """
        Upload base64 encoded image
        
        Args:
            image_data: Base64 encoded image
            filename: Original filename
            category: Product category
            product_id: Associated product ID
            
        Returns:
            ImageUploadResponse with file details
        """
        try:
            metadata = {
                "category": category,
                "product_id": product_id,
                "original_filename": filename,
                "upload_method": "base64"
            }
            
            file_id = await store_image_base64(image_data, filename, "image/jpeg", metadata)
            
            # Get stored file size
            image_meta = await get_image_metadata(file_id)
            
            return ImageUploadResponse(
                success=True,
                file_id=file_id,
                filename=filename,
                content_type="image/jpeg",
                size=image_meta["length"] if image_meta else 0,
                image_url=self._generate_image_url(file_id)
            )
        
        except Exception as e:
            logger.error(f"Error uploading base64 image: {e}")
            raise
    
    async def get_image_file(self, file_id: str) -> Tuple[bytes, str]:
        """
        Get image file data and content type
        
        Args:
            file_id: GridFS file ID
            
        Returns:
            Tuple of (image_data, content_type)
        """
        try:
            image_data = await get_image(file_id)
            if not image_data:
                raise FileNotFoundError(f"Image {file_id} not found")
            
            # Get metadata for content type
            metadata = await get_image_metadata(file_id)
            content_type = metadata.get("content_type", "image/jpeg") if metadata else "image/jpeg"
            
            return image_data, content_type
        
        except Exception as e:
            logger.error(f"Error retrieving image {file_id}: {e}")
            raise
    
    async def get_image_metadata(self, file_id: str) -> ImageMetadataResponse:
        """
        Get image metadata
        
        Args:
            file_id: GridFS file ID
            
        Returns:
            ImageMetadataResponse with metadata
        """
        try:
            metadata = await get_image_metadata(file_id)
            if not metadata:
                raise FileNotFoundError(f"Image {file_id} not found")
            
            return ImageMetadataResponse(
                id=file_id,
                filename=metadata["filename"],
                content_type=metadata["content_type"],
                upload_date=metadata["upload_date"].isoformat(),
                size=metadata["length"],
                metadata={k: v for k, v in metadata.items() 
                         if k not in ["filename", "content_type", "upload_date", "length"]}
            )
        
        except Exception as e:
            logger.error(f"Error getting image metadata {file_id}: {e}")
            raise
    
    async def delete_image(self, file_id: str) -> bool:
        """
        Delete image from GridFS
        
        Args:
            file_id: GridFS file ID
            
        Returns:
            bool: True if successful
        """
        try:
            return await db_delete_image(file_id)
        
        except Exception as e:
            logger.error(f"Error deleting image {file_id}: {e}")
            raise
    
    async def list_images(
        self, 
        limit: int = 50, 
        skip: int = 0, 
        category: Optional[str] = None
    ) -> List[ImageMetadataResponse]:
        """
        List images with optional filtering
        
        Args:
            limit: Maximum number of images
            skip: Number of images to skip
            category: Filter by category
            
        Returns:
            List of ImageMetadataResponse
        """
        try:
            images = await db_list_images(limit, skip)
            
            # Filter by category if specified
            if category:
                images = [img for img in images if img.get("category") == category]
            
            return [
                ImageMetadataResponse(
                    id=img["id"],
                    filename=img["filename"],
                    content_type=img["content_type"],
                    upload_date=img["upload_date"].isoformat(),
                    size=img["length"],
                    metadata={k: v for k, v in img.items() 
                             if k not in ["id", "filename", "content_type", "upload_date", "length"]}
                )
                for img in images
            ]
        
        except Exception as e:
            logger.error(f"Error listing images: {e}")
            raise
    
    async def process_image_ml(self, file_id: str, image_data: bytes):
        """
        Background task to process uploaded image with ML
        
        Args:
            file_id: GridFS file ID
            image_data: Raw image bytes
        """
        try:
            # Import ML service to avoid circular imports
            from .ml_service import MLService
            
            ml_service = MLService()
            if not ml_service.is_available():
                logger.info(f"ML service not available for processing image {file_id}")
                return
            
            # Convert image to base64 for ML processing
            image_b64 = base64.b64encode(image_data).decode('utf-8')
            image_data_url = f"data:image/jpeg;base64,{image_b64}"
            
            # Get ML predictions
            prediction_response = await ml_service.predict_image(image_data_url, True)
            
            logger.info(f"ML processing completed for image {file_id}")
            # Note: In a real implementation, you'd update the GridFS metadata with ML results
            
        except Exception as e:
            logger.error(f"Background ML processing failed for {file_id}: {e}")
