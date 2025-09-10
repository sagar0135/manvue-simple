"""
Machine Learning-related Pydantic models
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime

class MLPredictionRequest(BaseModel):
    image_data: str = Field(..., description="Base64 encoded image data")
    include_colors: bool = Field(True, description="Include color analysis")

class DetectedItem(BaseModel):
    name: str = Field(..., description="Detected item name")
    confidence: int = Field(..., ge=0, le=100, description="Confidence percentage (0-100)")
    category: str = Field(..., description="MANVUE category")
    type: str = Field(..., description="Product type")
    confidence_boost: float = Field(0.0, description="Category-specific confidence boost")

class ColorInfo(BaseModel):
    hex: str = Field(..., description="Hex color code")
    name: str = Field(..., description="Color name")
    dominance: float = Field(..., ge=0.0, le=1.0, description="Color dominance (0.0-1.0)")

class MLPredictionResponse(BaseModel):
    success: bool = Field(True, description="Request success status")
    detected_items: List[DetectedItem] = Field(..., description="List of detected fashion items")
    colors: List[ColorInfo] = Field(default=[], description="Extracted colors from image")
    overall_confidence: int = Field(..., ge=0, le=100, description="Overall prediction confidence")
    processing_time: str = Field(..., description="Processing time")
    model_version: str = Field("2.0.0", description="ML model version")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())

class SimilarityRequest(BaseModel):
    image_path: str = Field(..., description="Path to the image file")
    text: str = Field(..., description="Text to compare with image")

class SimilarityResponse(BaseModel):
    similarity: float = Field(..., description="Cosine similarity score")
    image_path: str = Field(..., description="Path to the image file")
    text: str = Field(..., description="Text compared")

class EmbeddingRequest(BaseModel):
    image_path: str = Field(..., description="Path to the image file")

class TextEmbeddingRequest(BaseModel):
    text: str = Field(..., description="Text to generate embedding for")

class EmbeddingResponse(BaseModel):
    embedding: List[float] = Field(..., description="Generated embedding")
    model_used: str = Field("CLIP", description="Model used for embedding")

class CategoryInfo(BaseModel):
    category: str = Field(..., description="MANVUE category")
    type: str = Field(..., description="Product type")
    confidence_boost: float = Field(..., description="Confidence boost factor")

class MLStatusResponse(BaseModel):
    available: bool = Field(..., description="Whether ML service is available")
    models_loaded: Dict[str, bool] = Field(..., description="Status of loaded models")
    version: str = Field(..., description="ML service version")
    device: str = Field(..., description="Computing device (cpu/cuda)")
    memory_usage: Optional[Dict[str, Any]] = Field(None, description="Memory usage statistics")

class ImageAnalysisRequest(BaseModel):
    image_data: str = Field(..., description="Base64 encoded image data")
    analysis_type: str = Field("full", description="Type of analysis: full, colors, category")

class ImageAnalysisResponse(BaseModel):
    analysis_type: str
    results: Dict[str, Any]
    processing_time: float
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
