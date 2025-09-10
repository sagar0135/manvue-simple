"""
Image Management API Routes
Handles image upload, retrieval, and management with MongoDB GridFS
"""

import io
import base64
from typing import List, Optional
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, BackgroundTasks
from fastapi.responses import StreamingResponse
from PIL import Image
import logging

# Import our models and services
from ..models.image_models import ImageUploadResponse, ImageMetadataResponse
from ..services.image_service import ImageService
from ..core.config import get_settings

# Configure logging
logger = logging.getLogger(__name__)
settings = get_settings()

# Create router
router = APIRouter(prefix="/images", tags=["Images"])

# Initialize image service
image_service = ImageService()

@router.post("/upload", response_model=ImageUploadResponse)
async def upload_image(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    category: Optional[str] = Form(None),
    product_id: Optional[str] = Form(None)
):
    """Upload an image file and store in GridFS"""
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read file data
        file_data = await file.read()
        
        # Optional: Resize image to optimize storage
        try:
            img = Image.open(io.BytesIO(file_data))
            # Resize if too large (max 1920x1920)
            if img.width > 1920 or img.height > 1920:
                img.thumbnail((1920, 1920), Image.Resampling.LANCZOS)
                output = io.BytesIO()
                img.save(output, format=img.format or 'JPEG', quality=85)
                file_data = output.getvalue()
        except Exception as e:
            logger.warning(f"Could not optimize image: {e}")
        
        # Store in GridFS using service
        result = await image_service.upload_image(
            file_data, 
            file.filename, 
            file.content_type,
            category=category,
            product_id=product_id
        )
        
        # Add ML processing in background if available
        background_tasks.add_task(image_service.process_image_ml, result.file_id, file_data)
        
        return result
    
    except Exception as e:
        logger.error(f"Error uploading image: {e}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.post("/upload-base64", response_model=ImageUploadResponse)
async def upload_image_base64(
    background_tasks: BackgroundTasks,
    image_data: str = Form(...),
    filename: str = Form(...),
    category: Optional[str] = Form(None),
    product_id: Optional[str] = Form(None)
):
    """Upload base64 encoded image (for Colab integration)"""
    try:
        result = await image_service.upload_image_base64(
            image_data,
            filename,
            category=category,
            product_id=product_id
        )
        
        # Add ML processing in background if available
        if image_data.startswith('data:'):
            image_data = image_data.split(',')[1]
        image_bytes = base64.b64decode(image_data)
        background_tasks.add_task(image_service.process_image_ml, result.file_id, image_bytes)
        
        return result
    
    except Exception as e:
        logger.error(f"Error uploading base64 image: {e}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.get("/{file_id}")
async def get_image_file(file_id: str):
    """Retrieve image file from GridFS"""
    try:
        image_data, content_type = await image_service.get_image_file(file_id)
        
        return StreamingResponse(
            io.BytesIO(image_data),
            media_type=content_type,
            headers={"Cache-Control": "max-age=86400"}  # Cache for 24 hours
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving image {file_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve image")

@router.get("/{file_id}/metadata", response_model=ImageMetadataResponse)
async def get_image_info(file_id: str):
    """Get image metadata"""
    try:
        return await image_service.get_image_metadata(file_id)
    except Exception as e:
        logger.error(f"Error getting image metadata {file_id}: {e}")
        raise HTTPException(status_code=404, detail="Image not found")

@router.delete("/{file_id}")
async def delete_image_file(file_id: str):
    """Delete image from GridFS"""
    try:
        success = await image_service.delete_image(file_id)
        if not success:
            raise HTTPException(status_code=404, detail="Image not found")
        
        return {"success": True, "message": "Image deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting image {file_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete image")

@router.get("", response_model=List[ImageMetadataResponse])
async def list_all_images(limit: int = 50, skip: int = 0, category: Optional[str] = None):
    """List all images with optional filtering"""
    try:
        return await image_service.list_images(limit, skip, category)
    except Exception as e:
        logger.error(f"Error listing images: {e}")
        raise HTTPException(status_code=500, detail="Failed to list images")
