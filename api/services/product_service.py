"""
Product Service
Business logic for product management with MongoDB
"""

import logging
from typing import List, Optional, Dict, Any
from datetime import datetime

# Import database functions
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from backend.database import (
    create_product, get_product as db_get_product, get_products as db_get_products,
    update_product as db_update_product, delete_product as db_delete_product
)

from ..models.product_models import ProductResponse

# Configure logging
logger = logging.getLogger(__name__)

class ProductService:
    """Service for handling product operations"""
    
    def __init__(self):
        self.api_base_url = "http://localhost:5001"  # This should come from config
    
    def _generate_image_url(self, file_id: str) -> str:
        """Generate image URL for given file ID"""
        return f"{self.api_base_url}/api/images/{file_id}"
    
    def _convert_to_response(self, product: Dict[str, Any]) -> ProductResponse:
        """
        Convert database product to ProductResponse
        
        Args:
            product: Product data from database
            
        Returns:
            ProductResponse with image URLs
        """
        # Generate image URLs from GridFS IDs
        image_urls = [self._generate_image_url(img_id) for img_id in product.get("image_ids", [])]
        
        # Add external URLs if any
        image_urls.extend(product.get("image_urls", []))
        
        # Set primary image for backward compatibility
        primary_image = image_urls[0] if image_urls else None
        
        return ProductResponse(
            id=product["_id"],
            name=product["name"],
            title=product.get("title", product["name"]),
            price=product["price"],
            originalPrice=product.get("originalPrice"),
            category=product["category"],
            type=product["type"],
            size=product.get("size", []),
            color=product.get("color", []),
            brand=product.get("brand"),
            rating=product.get("rating", 4.5),
            reviews=product.get("reviews", 0),
            image_ids=product.get("image_ids", []),
            image_urls=image_urls,
            image=primary_image,
            tags=product.get("tags", []),
            inStock=product.get("inStock", True),
            description=product.get("description"),
            features=product.get("features", []),
            created_at=product["created_at"].isoformat(),
            updated_at=product["updated_at"].isoformat()
        )
    
    async def get_products(
        self, 
        category: Optional[str] = None, 
        limit: int = 50, 
        skip: int = 0
    ) -> List[ProductResponse]:
        """
        Get products with optional filtering
        
        Args:
            category: Filter by category
            limit: Maximum number of products
            skip: Number of products to skip
            
        Returns:
            List of ProductResponse
        """
        try:
            products = await db_get_products(category, limit, skip)
            return [self._convert_to_response(product) for product in products]
        
        except Exception as e:
            logger.error(f"Error getting products: {e}")
            raise
    
    async def get_product(self, product_id: str) -> Optional[ProductResponse]:
        """
        Get a specific product
        
        Args:
            product_id: Product ID
            
        Returns:
            ProductResponse or None if not found
        """
        try:
            product = await db_get_product(product_id)
            if not product:
                return None
            
            return self._convert_to_response(product)
        
        except Exception as e:
            logger.error(f"Error getting product {product_id}: {e}")
            raise
    
    async def create_product(self, product_data: Dict[str, Any]) -> ProductResponse:
        """
        Create a new product
        
        Args:
            product_data: Product data
            
        Returns:
            ProductResponse for created product
        """
        try:
            product_id = await create_product(product_data)
            
            # Return the created product
            created_product = await db_get_product(product_id)
            return self._convert_to_response(created_product)
        
        except Exception as e:
            logger.error(f"Error creating product: {e}")
            raise
    
    async def update_product(self, product_id: str, update_data: Dict[str, Any]) -> bool:
        """
        Update an existing product
        
        Args:
            product_id: Product ID
            update_data: Data to update
            
        Returns:
            bool: True if successful
        """
        try:
            return await db_update_product(product_id, update_data)
        
        except Exception as e:
            logger.error(f"Error updating product {product_id}: {e}")
            raise
    
    async def delete_product(self, product_id: str) -> bool:
        """
        Delete a product
        
        Args:
            product_id: Product ID
            
        Returns:
            bool: True if successful
        """
        try:
            return await db_delete_product(product_id)
        
        except Exception as e:
            logger.error(f"Error deleting product {product_id}: {e}")
            raise
    
    async def search_products_text(
        self, 
        query: str, 
        category: Optional[str] = None, 
        limit: int = 20
    ) -> List[ProductResponse]:
        """
        Search products by text query
        
        Args:
            query: Search query
            category: Filter by category
            limit: Maximum number of results
            
        Returns:
            List of ProductResponse
        """
        try:
            # Simple text search implementation
            # In a real application, this would use MongoDB text search or external search engine
            all_products = await db_get_products(category, limit=100)
            
            # Filter products that match the query
            matching_products = []
            query_lower = query.lower()
            
            for product in all_products:
                # Search in name, description, tags, brand
                searchable_text = f"{product.get('name', '')} {product.get('description', '')} {' '.join(product.get('tags', []))} {product.get('brand', '')}".lower()
                
                if query_lower in searchable_text:
                    matching_products.append(product)
                
                if len(matching_products) >= limit:
                    break
            
            return [self._convert_to_response(product) for product in matching_products]
        
        except Exception as e:
            logger.error(f"Error searching products: {e}")
            raise
    
    async def get_featured_products(self, limit: int = 10) -> List[ProductResponse]:
        """
        Get featured/trending products
        
        Args:
            limit: Maximum number of products
            
        Returns:
            List of ProductResponse
        """
        try:
            # Get products sorted by rating and reviews (as a simple featured algorithm)
            products = await db_get_products(limit=limit * 2)  # Get more to sort
            
            # Sort by rating and review count
            featured_products = sorted(
                products, 
                key=lambda p: (p.get('rating', 0) * 0.7) + (min(p.get('reviews', 0), 100) * 0.003),
                reverse=True
            )[:limit]
            
            return [self._convert_to_response(product) for product in featured_products]
        
        except Exception as e:
            logger.error(f"Error getting featured products: {e}")
            raise
    
    async def get_products_by_ids(self, product_ids: List[str]) -> List[ProductResponse]:
        """
        Get multiple products by their IDs
        
        Args:
            product_ids: List of product IDs
            
        Returns:
            List of ProductResponse
        """
        try:
            products = []
            for product_id in product_ids:
                product = await self.get_product(product_id)
                if product:
                    products.append(product)
            
            return products
        
        except Exception as e:
            logger.error(f"Error getting products by IDs: {e}")
            raise
    
    async def get_similar_products(
        self, 
        product_id: str, 
        limit: int = 5
    ) -> List[ProductResponse]:
        """
        Get products similar to the given product
        
        Args:
            product_id: Reference product ID
            limit: Maximum number of similar products
            
        Returns:
            List of ProductResponse
        """
        try:
            # Get the reference product
            reference_product = await db_get_product(product_id)
            if not reference_product:
                return []
            
            # Find products in the same category with similar tags
            category_products = await db_get_products(
                category=reference_product.get("category"),
                limit=limit * 3
            )
            
            # Score products based on tag similarity
            reference_tags = set(reference_product.get("tags", []))
            similar_products = []
            
            for product in category_products:
                if product["_id"] == product_id:  # Skip the reference product
                    continue
                
                product_tags = set(product.get("tags", []))
                similarity_score = len(reference_tags & product_tags) / max(len(reference_tags | product_tags), 1)
                
                if similarity_score > 0:
                    similar_products.append((product, similarity_score))
            
            # Sort by similarity and return top results
            similar_products.sort(key=lambda x: x[1], reverse=True)
            
            return [
                self._convert_to_response(product) 
                for product, score in similar_products[:limit]
            ]
        
        except Exception as e:
            logger.error(f"Error getting similar products for {product_id}: {e}")
            raise
