"""
Product Management API Routes
Handles product CRUD operations with MongoDB integration
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException
import logging

# Import our models and services
from ..models.product_models import Product, ProductResponse, ProductCreateRequest
from ..services.product_service import ProductService

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/products", tags=["Products"])

# Initialize product service
product_service = ProductService()

@router.get("", response_model=List[ProductResponse])
async def get_all_products(category: Optional[str] = None, limit: int = 50, skip: int = 0):
    """Get all products with image URLs"""
    try:
        return await product_service.get_products(category, limit, skip)
    except Exception as e:
        logger.error(f"Error getting products: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve products")

@router.get("/{product_id}", response_model=ProductResponse)
async def get_single_product(product_id: str):
    """Get a specific product"""
    try:
        product = await product_service.get_product(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting product {product_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve product")

@router.post("", response_model=ProductResponse)
async def create_new_product(product: ProductCreateRequest):
    """Create a new product"""
    try:
        return await product_service.create_product(product.dict())
    except Exception as e:
        logger.error(f"Error creating product: {e}")
        raise HTTPException(status_code=500, detail="Failed to create product")

@router.put("/{product_id}")
async def update_existing_product(product_id: str, product: ProductCreateRequest):
    """Update an existing product"""
    try:
        success = await product_service.update_product(product_id, product.dict(exclude_unset=True))
        if not success:
            raise HTTPException(status_code=404, detail="Product not found")
        return {"success": True, "message": "Product updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating product {product_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to update product")

@router.delete("/{product_id}")
async def delete_existing_product(product_id: str):
    """Delete a product"""
    try:
        success = await product_service.delete_product(product_id)
        if not success:
            raise HTTPException(status_code=404, detail="Product not found")
        return {"success": True, "message": "Product deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting product {product_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete product")

@router.get("/search/text")
async def search_products_text(query: str, category: Optional[str] = None, limit: int = 20):
    """Search products by text query"""
    try:
        return await product_service.search_products_text(query, category, limit)
    except Exception as e:
        logger.error(f"Error searching products: {e}")
        raise HTTPException(status_code=500, detail="Failed to search products")

@router.get("/category/{category}")
async def get_products_by_category(category: str, limit: int = 50, skip: int = 0):
    """Get products by category"""
    try:
        return await product_service.get_products(category, limit, skip)
    except Exception as e:
        logger.error(f"Error getting products by category {category}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve products")

@router.get("/featured/trending")
async def get_featured_products(limit: int = 10):
    """Get featured/trending products"""
    try:
        return await product_service.get_featured_products(limit)
    except Exception as e:
        logger.error(f"Error getting featured products: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve featured products")

@router.get("/{product_id}/images")
async def get_product_images(product_id: str, color: Optional[str] = None):
    """Get product images, optionally filtered by color"""
    try:
        product = await product_service.get_product(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # If color is specified, try to get color-specific images
        if color:
            # This would need to be implemented based on your database structure
            # For now, we'll return all images and let the frontend handle color filtering
            pass
        
        return {
            "product_id": product_id,
            "images": product.image_urls,
            "primary_image": product.image,
            "image_ids": product.image_ids,
            "colors": product.color
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting product images for {product_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve product images")

@router.get("/{product_id}/images/{color}")
async def get_product_images_by_color(product_id: str, color: str):
    """Get product images for a specific color variant"""
    try:
        product = await product_service.get_product(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Check if the requested color is available
        if color not in product.color:
            raise HTTPException(status_code=400, detail=f"Color '{color}' not available for this product")
        
        # For now, return all images. In a real implementation, you'd have color-specific image IDs
        # stored in the database or use image metadata to filter by color
        return {
            "product_id": product_id,
            "color": color,
            "images": product.image_urls,
            "primary_image": product.image,
            "image_ids": product.image_ids
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting product images for {product_id} color {color}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve product images")