"""
Machine Learning API Routes
Handles ML predictions, image analysis, and AI-powered features
"""

from fastapi import APIRouter, HTTPException
import logging

# Import our models and services
from ..models.ml_models import MLPredictionRequest, MLPredictionResponse, SimilarityRequest, SimilarityResponse
from ..services.ml_service import MLService

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/ml", tags=["Machine Learning"])

# Initialize ML service
ml_service = MLService()

@router.post("/predict", response_model=MLPredictionResponse)
async def predict_image_ml(request: MLPredictionRequest):
    """Get ML predictions for an image"""
    try:
        if not ml_service.is_available():
            raise HTTPException(status_code=503, detail="ML service not available")
        
        prediction_response = await ml_service.predict_image(request.image_data, request.include_colors)
        return prediction_response
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"ML prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@router.post("/similarity", response_model=SimilarityResponse)
async def compute_similarity(request: SimilarityRequest):
    """Compute similarity between image and text"""
    try:
        if not ml_service.is_available():
            raise HTTPException(status_code=503, detail="ML service not available")
        
        similarity = await ml_service.compute_similarity(request.image_path, request.text)
        return SimilarityResponse(
            similarity=similarity,
            image_path=request.image_path,
            text=request.text
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Similarity computation error: {e}")
        raise HTTPException(status_code=500, detail=f"Similarity computation failed: {str(e)}")

@router.get("/status")
async def get_ml_status():
    """Check ML service status"""
    try:
        status = ml_service.get_status()
        return status
    except Exception as e:
        logger.error(f"Error getting ML status: {e}")
        raise HTTPException(status_code=500, detail="Failed to get ML status")

@router.post("/analyze-colors")
async def analyze_image_colors(image_data: str):
    """Extract colors from an image"""
    try:
        colors = await ml_service.extract_colors(image_data)
        return {
            "colors": colors,
            "color_count": len(colors)
        }
    except Exception as e:
        logger.error(f"Color analysis error: {e}")
        raise HTTPException(status_code=500, detail=f"Color analysis failed: {str(e)}")

@router.post("/categorize")
async def categorize_image(image_data: str):
    """Categorize fashion item from image"""
    try:
        if not ml_service.is_available():
            raise HTTPException(status_code=503, detail="ML service not available")
        
        category = await ml_service.categorize_image(image_data)
        return {
            "category": category,
            "confidence": category.get("confidence", 0)
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Categorization error: {e}")
        raise HTTPException(status_code=500, detail=f"Categorization failed: {str(e)}")

@router.get("/categories")
async def get_available_categories():
    """Get available ML categories"""
    try:
        categories = ml_service.get_available_categories()
        return {
            "categories": categories,
            "total_categories": len(categories)
        }
    except Exception as e:
        logger.error(f"Error getting categories: {e}")
        raise HTTPException(status_code=500, detail="Failed to get categories")
