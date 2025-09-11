"""
Visual Search related Pydantic models
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from .product_models import ProductResponse

class VisualSearchRequest(BaseModel):
    image: str = Field(..., description="Base64 encoded image data")
    max_products: int = Field(10, ge=1, le=50, description="Maximum number of similar products")
    max_outfits: int = Field(3, ge=1, le=10, description="Maximum number of outfit recommendations")
    category_filter: Optional[str] = Field(None, description="Filter results by category")
    
    class Config:
        schema_extra = {
            "example": {
                "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ...",
                "max_products": 10,
                "max_outfits": 3,
                "category_filter": "tops"
            }
        }

class SimilarProduct(BaseModel):
    product: ProductResponse
    similarity_score: float = Field(..., ge=0.0, le=1.0, description="Similarity score (0-1)")
    confidence: int = Field(..., ge=0, le=100, description="Confidence percentage (0-100)")

class OutfitItem(BaseModel):
    product: ProductResponse
    role: str = Field(..., description="Role in outfit (base, top, bottom, outerwear, shoes, accessory)")

class OutfitRecommendation(BaseModel):
    id: str
    base_product: ProductResponse
    confidence: int = Field(..., ge=0, le=100, description="Overall outfit confidence")
    items: List[OutfitItem]
    total_price: float = Field(..., ge=0, description="Total price of all items")
    style_description: str = Field(..., description="Description of the outfit style")

class AnalysisMetadata(BaseModel):
    processing_time: str
    total_products_found: int
    total_outfits_generated: int
    clip_model_available: bool

class VisualSearchResponse(BaseModel):
    success: bool
    similar_products: List[SimilarProduct] = []
    outfit_recommendations: List[OutfitRecommendation] = []
    analysis_metadata: Optional[AnalysisMetadata] = None
    error: Optional[str] = None

class ImageAnalysisRequest(BaseModel):
    image: str = Field(..., description="Base64 encoded image data")
    include_colors: bool = Field(True, description="Include color analysis")
    include_outfit_suggestions: bool = Field(True, description="Include outfit recommendations")

class DetectedItem(BaseModel):
    name: str
    confidence: int = Field(..., ge=0, le=100)
    category: str
    type: str
    confidence_boost: float = Field(0.0, ge=0.0, le=1.0)

class ColorInfo(BaseModel):
    hex: str
    name: str
    dominance: float = Field(..., ge=0.0, le=1.0)

class ImageAnalysisResponse(BaseModel):
    success: bool
    detected_items: List[DetectedItem] = []
    colors: List[ColorInfo] = []
    similar_products: List[SimilarProduct] = []
    outfit_recommendations: List[OutfitRecommendation] = []
    overall_confidence: int = Field(0, ge=0, le=100)
    processing_time: str
    error: Optional[str] = None
