"""
Image-related Pydantic models
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime

class ImageUploadResponse(BaseModel):
    success: bool
    file_id: str
    filename: str
    content_type: str
    size: int
    image_url: str
    ml_predictions: Optional[Dict] = None

class ImageMetadataResponse(BaseModel):
    id: str
    filename: str
    content_type: str
    upload_date: str
    size: int
    metadata: Dict

class ImageUploadRequest(BaseModel):
    image_data: str = Field(..., description="Base64 encoded image data")
    filename: str = Field(..., description="Original filename")
    category: Optional[str] = Field(None, description="Product category")
    product_id: Optional[str] = Field(None, description="Associated product ID")

class ColorInfo(BaseModel):
    hex: str = Field(..., description="Hex color code")
    name: str = Field(..., description="Color name")
    dominance: float = Field(..., ge=0.0, le=1.0, description="Color dominance (0.0-1.0)")
