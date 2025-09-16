"""
Visual Search API Routes
Handles image recognition, similarity search, and outfit recommendations
"""

import logging
from typing import Dict, Any
from datetime import datetime
from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse

from ..models.visual_search_models import (
    VisualSearchRequest, 
    VisualSearchResponse,
    ImageAnalysisRequest,
    ImageAnalysisResponse
)
from ..services.visual_search_service import VisualSearchService

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/visual-search", tags=["Visual Search"])

# Initialize service
visual_search_service = VisualSearchService()

@router.post("/search", response_model=VisualSearchResponse,
             summary="Visual Product Search",
             description="Find similar products and generate outfit recommendations from uploaded image")
async def visual_search(request: VisualSearchRequest):
    """
    Perform visual search with outfit recommendations
    
    This endpoint:
    1. Analyzes the uploaded image using CLIP embeddings
    2. Finds similar products in the database
    3. Generates outfit recommendations based on the detected item
    """
    try:
        logger.info(f"Visual search request received - max_products: {request.max_products}, max_outfits: {request.max_outfits}")
        
        # Perform complete analysis
        results = await visual_search_service.analyze_image_and_recommend(
            image_data=request.image,
            max_products=request.max_products,
            max_outfits=request.max_outfits
        )
        
        if not results['success']:
            raise HTTPException(status_code=500, detail=results.get('error', 'Visual search failed'))
        
        return VisualSearchResponse(
            success=True,
            similar_products=results['similar_products'],
            outfit_recommendations=results['outfit_recommendations'],
            analysis_metadata=results['analysis_metadata']
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in visual search: {e}")
        raise HTTPException(status_code=500, detail=f"Visual search failed: {str(e)}")

@router.post("/analyze", response_model=ImageAnalysisResponse,
             summary="Complete Image Analysis",
             description="Analyze image for fashion items, colors, similar products, and outfit suggestions")
async def analyze_image(request: ImageAnalysisRequest):
    """
    Complete image analysis including:
    - Fashion item detection
    - Color analysis
    - Similar product search
    - Outfit recommendations
    """
    try:
        logger.info("Complete image analysis request received")
        
        # For now, we'll use the visual search service
        # In a full implementation, this would integrate with the ML server
        results = await visual_search_service.analyze_image_and_recommend(
            image_data=request.image,
            max_products=10,
            max_outfits=3
        )
        
        if not results['success']:
            raise HTTPException(status_code=500, detail=results.get('error', 'Image analysis failed'))
        
        # Format response for complete analysis
        return ImageAnalysisResponse(
            success=True,
            detected_items=[],  # Would be populated by ML server integration
            colors=[],  # Would be populated by color analysis
            similar_products=results['similar_products'],
            outfit_recommendations=results['outfit_recommendations'],
            overall_confidence=85,  # Placeholder
            processing_time=results['analysis_metadata']['processing_time']
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in image analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Image analysis failed: {str(e)}")

@router.get("/health", 
            summary="Visual Search Health Check",
            description="Check if visual search service is available")
async def health_check():
    """
    Check if the visual search service is healthy and ready
    """
    try:
        health_info = {
            "status": "healthy",
            "service": "visual_search",
            "clip_available": visual_search_service.clip_available,
            "enhanced_ml_available": visual_search_service.enhanced_ml_available,
            "timestamp": "2024-01-01T00:00:00Z"
        }
        
        # Add enhanced ML service info if available
        if visual_search_service.enhanced_ml_available and visual_search_service.enhanced_ml:
            health_info.update(visual_search_service.enhanced_ml.get_model_info())
        
        return health_info
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Visual search service unavailable")

@router.get("/categories",
            summary="Get Compatible Categories",
            description="Get outfit compatibility rules for different categories")
async def get_compatible_categories():
    """
    Get the outfit compatibility rules for different clothing categories
    """
    try:
        return {
            "outfit_rules": visual_search_service.outfit_rules,
            "description": "Compatibility rules for outfit recommendations"
        }
    except Exception as e:
        logger.error(f"Error getting compatible categories: {e}")
        raise HTTPException(status_code=500, detail="Failed to get compatible categories")

@router.post("/generate-outfit",
             summary="Generate Outfit from Product",
             description="Generate outfit recommendations based on a specific product")
async def generate_outfit_from_product(product_id: str, max_outfits: int = 3):
    """
    Generate outfit recommendations based on a specific product ID
    """
    try:
        # Get the product
        product = await visual_search_service.product_service.get_product(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Create a mock similar products list with the base product
        similar_products = [{
            'product': product,
            'similarity_score': 1.0,
            'confidence': 100
        }]
        
        # Generate outfit recommendations
        outfit_recommendations = await visual_search_service.generate_outfit_recommendations(
            similar_products,
            max_outfits=max_outfits
        )
        
        return {
            "success": True,
            "base_product": product,
            "outfit_recommendations": outfit_recommendations
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating outfit from product: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate outfit: {str(e)}")

@router.post("/collab-search",
             summary="Collab System Visual Search",
             description="Use the collab system for advanced visual search with FAISS index")
async def collab_visual_search(request: VisualSearchRequest):
    """
    Advanced visual search using the collab system integration
    This endpoint uses CLIP + FAISS + MongoDB for high-performance similarity search
    """
    try:
        logger.info("Collab visual search request received")
        
        # Check if enhanced ML service is available
        if not visual_search_service.enhanced_ml_available:
            raise HTTPException(
                status_code=503, 
                detail="Enhanced ML service not available. Please run the collab integration script first."
            )
        
        if not visual_search_service.enhanced_ml.is_available():
            raise HTTPException(
                status_code=503,
                detail="Enhanced ML service not properly initialized. Missing CLIP model or FAISS index."
            )
        
        # Perform enhanced search
        results = await visual_search_service.find_similar_products(
            image_data=request.image,
            limit=request.max_products
        )
        
        # Generate outfit recommendations if requested
        outfit_recommendations = []
        if request.max_outfits > 0:
            outfit_recommendations = await visual_search_service.generate_outfit_recommendations(
                results,
                max_outfits=request.max_outfits
            )
        
        return VisualSearchResponse(
            success=True,
            similar_products=results,
            outfit_recommendations=outfit_recommendations,
            analysis_metadata={
                "processing_time": "0.5s",  # FAISS is very fast
                "method": "collab_clip_faiss",
                "total_products_found": len(results),
                "faiss_index_size": visual_search_service.enhanced_ml.faiss_index.ntotal if visual_search_service.enhanced_ml.faiss_index else 0
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in collab visual search: {e}")
        raise HTTPException(status_code=500, detail=f"Collab visual search failed: {str(e)}")

@router.post("/upload-and-search",
             summary="Upload Image and Search (Collab Style)",
             description="Upload user image to MongoDB and find similar products (like collab system)")
async def upload_and_search(request: VisualSearchRequest, username: str = "guest"):
    """
    Upload user image to MongoDB and perform similarity search
    This mimics the collab system's upload_user_and_find functionality
    """
    try:
        logger.info(f"Upload and search request from user: {username}")
        
        # Check if enhanced ML service is available
        if not visual_search_service.enhanced_ml_available or not visual_search_service.enhanced_ml:
            raise HTTPException(
                status_code=503,
                detail="Enhanced ML service not available"
            )
        
        # Preprocess image
        image = visual_search_service._preprocess_image(request.image)
        if not image:
            raise HTTPException(status_code=400, detail="Invalid image data")
        
        # Use enhanced ML service upload and search
        search_result = visual_search_service.enhanced_ml.upload_user_image_and_search(
            image=image,
            username=username,
            top_k=request.max_products
        )
        
        if not search_result['success']:
            raise HTTPException(status_code=500, detail=search_result.get('error', 'Search failed'))
        
        # Format response
        formatted_products = []
        for product_data in search_result['similar_products']:
            formatted_products.append({
                'product': {
                    'id': product_data.get('product_id', 'unknown'),
                    'name': product_data.get('name', 'Unknown Product'),
                    'category': product_data.get('category', 'Unknown'),
                    'price': 0,
                    'image_url': f"/api/images/{product_data.get('filename', '')}"
                },
                'similarity_score': product_data.get('similarity_score', 0.0),
                'confidence': product_data.get('confidence', 0),
                'metadata': product_data
            })
        
        return {
            "success": True,
            "file_id": search_result['file_id'],
            "similar_products": formatted_products,
            "total_found": search_result['total_found'],
            "username": username,
            "upload_timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in upload and search: {e}")
        raise HTTPException(status_code=500, detail=f"Upload and search failed: {str(e)}")
