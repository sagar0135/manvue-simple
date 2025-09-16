"""
Visual Search Service
Handles image recognition, similarity search, and outfit recommendations
"""

import logging
import base64
import io
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from PIL import Image
import asyncio
from datetime import datetime

# Import ML model functions
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

# Try enhanced ML service first, then fallback to backend ML model
try:
    from .enhanced_ml_service import EnhancedMLService
    enhanced_ml_available = True
except ImportError as e:
    logging.warning(f"Enhanced ML service not available: {e}")
    enhanced_ml_available = False

try:
    from backend.ml_model import get_image_embedding, get_text_embedding, compute_similarity, is_model_loaded
    CLIP_AVAILABLE = True
except ImportError as e:
    logging.warning(f"CLIP model not available: {e}")
    CLIP_AVAILABLE = False

# Import database and product services
from .product_service import ProductService
from ..models.product_models import ProductResponse
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from backend.database import get_all_product_embeddings, store_product_embedding

logger = logging.getLogger(__name__)

class VisualSearchService:
    """Service for visual search and outfit recommendations"""
    
    def __init__(self):
        self.product_service = ProductService()
        self.clip_available = CLIP_AVAILABLE
        self.enhanced_ml_available = enhanced_ml_available
        
        # Initialize enhanced ML service if available
        if self.enhanced_ml_available:
            try:
                self.enhanced_ml = EnhancedMLService()
                logger.info("✅ Enhanced ML service initialized")
            except Exception as e:
                logger.error(f"Failed to initialize enhanced ML service: {e}")
                self.enhanced_ml = None
                self.enhanced_ml_available = False
        else:
            self.enhanced_ml = None
        
        # Outfit recommendation rules
        self.outfit_rules = {
            'tops': {
                'compatible_bottoms': ['bottoms', 'jeans', 'trousers', 'shorts'],
                'compatible_outerwear': ['jackets', 'blazers', 'coats'],
                'compatible_shoes': ['sneakers', 'dress_shoes', 'boots', 'loafers'],
                'compatible_accessories': ['belts', 'watches', 'bags']
            },
            'bottoms': {
                'compatible_tops': ['shirts', 'tshirts', 'polo', 'sweaters'],
                'compatible_outerwear': ['jackets', 'blazers', 'coats'],
                'compatible_shoes': ['sneakers', 'dress_shoes', 'boots', 'loafers'],
                'compatible_accessories': ['belts', 'watches']
            },
            'outerwear': {
                'compatible_tops': ['shirts', 'tshirts', 'polo', 'sweaters'],
                'compatible_bottoms': ['bottoms', 'jeans', 'trousers'],
                'compatible_shoes': ['boots', 'dress_shoes', 'sneakers'],
                'compatible_accessories': ['scarves', 'gloves', 'hats']
            },
            'shoes': {
                'compatible_tops': ['shirts', 'tshirts', 'polo', 'sweaters'],
                'compatible_bottoms': ['bottoms', 'jeans', 'trousers', 'shorts'],
                'compatible_outerwear': ['jackets', 'blazers', 'coats'],
                'compatible_accessories': ['socks', 'belts']
            }
        }
    
    def _preprocess_image(self, image_data: str) -> Optional[Image.Image]:
        """
        Preprocess base64 image data for ML model
        
        Args:
            image_data: Base64 encoded image data
            
        Returns:
            PIL Image object or None if processing fails
        """
        try:
            # Remove data URL prefix if present
            if ',' in image_data:
                image_data = image_data.split(',')[1]
            
            # Decode base64
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
            
            return image
            
        except Exception as e:
            logger.error(f"Error preprocessing image: {e}")
            return None
    
    def _get_image_embedding_from_data(self, image_data: str) -> Optional[List[float]]:
        """
        Get CLIP embedding from base64 image data
        
        Args:
            image_data: Base64 encoded image data
            
        Returns:
            Image embedding as list of floats or None
        """
        if not self.clip_available:
            logger.warning("CLIP model not available")
            return None
        
        try:
            # Save image temporarily to get embedding
            image = self._preprocess_image(image_data)
            if not image:
                return None
            
            # Save to temporary file
            temp_path = f"/tmp/temp_image_{datetime.now().timestamp()}.jpg"
            image.save(temp_path)
            
            # Get embedding
            embedding = get_image_embedding(temp_path)
            
            # Clean up temp file
            os.unlink(temp_path)
            
            return embedding
            
        except Exception as e:
            logger.error(f"Error getting image embedding: {e}")
            return None
    
    def _compute_similarity_scores(self, query_embedding: List[float], product_embeddings: Dict[str, List[float]]) -> Dict[str, float]:
        """
        Compute similarity scores between query and product embeddings
        
        Args:
            query_embedding: Query image embedding
            product_embeddings: Dict of product_id -> embedding
            
        Returns:
            Dict of product_id -> similarity score
        """
        similarities = {}
        
        for product_id, product_embedding in product_embeddings.items():
            try:
                similarity = compute_similarity(query_embedding, product_embedding)
                similarities[product_id] = similarity
            except Exception as e:
                logger.error(f"Error computing similarity for product {product_id}: {e}")
                similarities[product_id] = 0.0
        
        return similarities
    
    async def _get_product_embeddings(self, products: List[ProductResponse]) -> Dict[str, List[float]]:
        """
        Get embeddings for all product images from database
        
        Args:
            products: List of products
            
        Returns:
            Dict of product_id -> embedding
        """
        try:
            # Get all embeddings from database
            all_embeddings = await get_all_product_embeddings()
            
            # Filter embeddings for the requested products
            product_embeddings = {}
            for product in products:
                if product.id in all_embeddings:
                    product_embeddings[product.id] = all_embeddings[product.id]
                else:
                    # Generate placeholder embedding for products without embeddings
                    logger.warning(f"No embedding found for product {product.id}, using placeholder")
                    product_embeddings[product.id] = np.random.rand(512).tolist()
            
            return product_embeddings
            
        except Exception as e:
            logger.error(f"Error getting product embeddings: {e}")
            # Fallback to placeholder embeddings
            return {product.id: np.random.rand(512).tolist() for product in products}
    
    async def find_similar_products(
        self, 
        image_data: str, 
        limit: int = 10,
        category_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Find products similar to the uploaded image
        
        Args:
            image_data: Base64 encoded image data
            limit: Maximum number of results
            category_filter: Optional category filter
            
        Returns:
            List of similar products with similarity scores
        """
        try:
            # Try enhanced ML service first
            if self.enhanced_ml_available and self.enhanced_ml and self.enhanced_ml.is_available():
                logger.info("Using enhanced ML service for visual search")
                return await self._find_similar_with_enhanced_ml(image_data, limit)
            else:
                logger.info("Using fallback ML service for visual search")
                return await self._find_similar_with_fallback(image_data, limit, category_filter)
                
        except Exception as e:
            logger.error(f"Error finding similar products: {e}")
            return []
    
    async def _find_similar_with_enhanced_ml(
        self, 
        image_data: str, 
        limit: int
    ) -> List[Dict[str, Any]]:
        """Find similar products using enhanced ML service"""
        try:
            # Preprocess image
            image = self._preprocess_image(image_data)
            if not image:
                return []
            
            # Use enhanced ML service
            search_results = self.enhanced_ml.find_similar_products(image, top_k=limit)
            
            # Format results to match expected structure
            formatted_results = []
            for result in search_results:
                formatted_results.append({
                    'product': {
                        'id': result.get('product_id', 'unknown'),
                        'name': result.get('name', 'Unknown Product'),
                        'category': result.get('category', 'Unknown'),
                        'price': 0,  # Would need to fetch from product service
                        'image_url': f"/api/images/{result.get('filename', '')}"
                    },
                    'similarity_score': result.get('similarity_score', 0.0),
                    'confidence': result.get('confidence', 0),
                    'metadata': result
                })
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error in enhanced ML search: {e}")
            return []
    
    async def _find_similar_with_fallback(
        self, 
        image_data: str, 
        limit: int,
        category_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Fallback method using original ML service"""
        try:
            # Get image embedding
            query_embedding = self._get_image_embedding_from_data(image_data)
            if not query_embedding:
                logger.warning("Could not generate query embedding")
                return []
            
            # Get all products (or filtered by category)
            products = await self.product_service.get_products(
                category=category_filter,
                limit=100  # Get more products for better similarity search
            )
            
            if not products:
                return []
            
            # Get product embeddings
            product_embeddings = await self._get_product_embeddings(products)
            
            # Compute similarities
            similarities = self._compute_similarity_scores(query_embedding, product_embeddings)
            
            # Sort by similarity and return top results
            sorted_products = sorted(
                products,
                key=lambda p: similarities.get(p.id, 0.0),
                reverse=True
            )[:limit]
            
            # Format results with similarity scores
            results = []
            for product in sorted_products:
                similarity_score = similarities.get(product.id, 0.0)
                results.append({
                    'product': product,
                    'similarity_score': similarity_score,
                    'confidence': min(int(similarity_score * 100), 100)
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Error in fallback search: {e}")
            return []
    
    def _get_compatible_categories(self, detected_category: str) -> Dict[str, List[str]]:
        """
        Get compatible categories for outfit building
        
        Args:
            detected_category: The category of the detected item
            
        Returns:
            Dict of compatible categories
        """
        return self.outfit_rules.get(detected_category, {})
    
    async def generate_outfit_recommendations(
        self, 
        similar_products: List[Dict[str, Any]], 
        max_outfits: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Generate outfit recommendations based on similar products
        
        Args:
            similar_products: List of similar products with scores
            max_outfits: Maximum number of outfit recommendations
            
        Returns:
            List of outfit recommendations
        """
        try:
            if not similar_products:
                return []
            
            # Get the top similar product as the base
            base_product = similar_products[0]['product']
            base_category = base_product.category.lower()
            
            # Get compatible categories
            compatible_categories = self._get_compatible_categories(base_category)
            
            outfits = []
            
            for i in range(max_outfits):
                outfit = {
                    'id': f'outfit_{i+1}',
                    'base_product': base_product,
                    'confidence': similar_products[0]['confidence'],
                    'items': [base_product],
                    'total_price': base_product.price,
                    'style_description': self._generate_style_description(base_product, i)
                }
                
                # Add compatible items
                for category_type, compatible_list in compatible_categories.items():
                    if compatible_list:
                        # Get products from compatible categories
                        compatible_products = await self.product_service.get_products(
                            category=compatible_list[0],  # Use first compatible category
                            limit=20
                        )
                        
                        if compatible_products:
                            # Select a random compatible product
                            import random
                            selected_product = random.choice(compatible_products)
                            outfit['items'].append(selected_product)
                            outfit['total_price'] += selected_product.price
                
                outfits.append(outfit)
            
            return outfits
            
        except Exception as e:
            logger.error(f"Error generating outfit recommendations: {e}")
            return []
    
    def _generate_style_description(self, base_product: ProductResponse, outfit_index: int) -> str:
        """
        Generate a style description for the outfit
        
        Args:
            base_product: The base product
            outfit_index: Index of the outfit variant
            
        Returns:
            Style description string
        """
        style_templates = [
            f"Modern {base_product.category} look with contemporary styling",
            f"Classic {base_product.category} ensemble with timeless appeal",
            f"Casual {base_product.category} outfit perfect for everyday wear"
        ]
        
        return style_templates[outfit_index % len(style_templates)]
    
    async def analyze_image_and_recommend(
        self, 
        image_data: str, 
        max_products: int = 10,
        max_outfits: int = 3
    ) -> Dict[str, Any]:
        """
        Complete image analysis with product search and outfit recommendations
        
        Args:
            image_data: Base64 encoded image data
            max_products: Maximum number of similar products
            max_outfits: Maximum number of outfit recommendations
            
        Returns:
            Complete analysis results
        """
        try:
            start_time = datetime.now()
            
            # Find similar products
            similar_products = await self.find_similar_products(
                image_data, 
                limit=max_products
            )
            
            # Generate outfit recommendations
            outfit_recommendations = await self.generate_outfit_recommendations(
                similar_products,
                max_outfits=max_outfits
            )
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return {
                'success': True,
                'similar_products': similar_products,
                'outfit_recommendations': outfit_recommendations,
                'analysis_metadata': {
                    'processing_time': f"{processing_time:.2f}s",
                    'total_products_found': len(similar_products),
                    'total_outfits_generated': len(outfit_recommendations),
                    'clip_model_available': self.clip_available
                }
            }
            
        except Exception as e:
            logger.error(f"Error in complete image analysis: {e}")
            return {
                'success': False,
                'error': str(e),
                'similar_products': [],
                'outfit_recommendations': []
            }
