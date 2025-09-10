"""
Machine Learning Service
Business logic for ML predictions and AI features
"""

import base64
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from ..models.ml_models import MLPredictionResponse, DetectedItem, ColorInfo

# Configure logging
logger = logging.getLogger(__name__)

class MLService:
    """Service for handling ML operations"""
    
    def __init__(self):
        self.ml_available = False
        self.model_version = "2.0.0"
        
        # Try to import ML functionality
        try:
            # Import the ML server functionality
            import sys
            import os
            sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
            
            # Try to import from the backend ML module
            from backend.ml_model import get_image_embedding, get_text_embedding, compute_similarity, is_model_loaded
            self.ml_available = True
            logger.info("✅ ML service initialized successfully")
        except ImportError as e:
            logger.warning(f"⚠️ ML service not available: {e}")
            self.ml_available = False
    
    def is_available(self) -> bool:
        """Check if ML service is available"""
        return self.ml_available
    
    def get_status(self) -> Dict[str, Any]:
        """Get ML service status"""
        try:
            return {
                "available": self.ml_available,
                "models_loaded": {
                    "clip": self.ml_available,
                    "fashion_classifier": self.ml_available
                },
                "version": self.model_version,
                "device": "cpu",  # This should be detected dynamically
                "memory_usage": None
            }
        except Exception as e:
            logger.error(f"Error getting ML status: {e}")
            return {
                "available": False,
                "models_loaded": {},
                "version": self.model_version,
                "device": "unknown",
                "memory_usage": None
            }
    
    async def predict_image(self, image_data: str, include_colors: bool = True) -> MLPredictionResponse:
        """
        Predict fashion items from image
        
        Args:
            image_data: Base64 encoded image data
            include_colors: Whether to include color analysis
            
        Returns:
            MLPredictionResponse with predictions
        """
        try:
            if not self.ml_available:
                # Return mock predictions for demo
                return self._get_mock_predictions(include_colors)
            
            start_time = datetime.now()
            
            # Process image with ML model
            # This would integrate with your actual ML pipeline
            predictions = await self._process_image_ml(image_data)
            
            # Extract colors if requested
            colors = []
            if include_colors:
                colors = await self.extract_colors(image_data)
            
            processing_time = f"{(datetime.now() - start_time).total_seconds():.2f}s"
            
            return MLPredictionResponse(
                success=True,
                detected_items=predictions,
                colors=colors,
                overall_confidence=max([item.confidence for item in predictions], default=0),
                processing_time=processing_time,
                model_version=self.model_version
            )
        
        except Exception as e:
            logger.error(f"Error predicting image: {e}")
            raise
    
    async def _process_image_ml(self, image_data: str) -> List[DetectedItem]:
        """
        Process image with ML model
        
        Args:
            image_data: Base64 encoded image data
            
        Returns:
            List of DetectedItem
        """
        try:
            # Mock ML processing - replace with actual ML model
            # This is where you'd integrate with your fashion classification model
            
            # MANVUE specific category mapping
            MANVUE_CATEGORY_MAP = {
                'T-Shirt': {'category': 'tops', 'type': 'tops', 'confidence_boost': 0.15},
                'Shirt': {'category': 'tops', 'type': 'tops', 'confidence_boost': 0.18},
                'Pullover': {'category': 'tops', 'type': 'tops', 'confidence_boost': 0.12},
                'Coat': {'category': 'outerwear', 'type': 'outerwear', 'confidence_boost': 0.20},
                'Trouser': {'category': 'bottoms', 'type': 'bottoms', 'confidence_boost': 0.16},
                'Sneaker': {'category': 'shoes', 'type': 'shoes', 'confidence_boost': 0.18},
                'Ankle Boot': {'category': 'shoes', 'type': 'shoes', 'confidence_boost': 0.17},
                'Sandal': {'category': 'shoes', 'type': 'shoes', 'confidence_boost': 0.15},
                'Bag': {'category': 'accessories', 'type': 'accessories', 'confidence_boost': 0.12},
            }
            
            # Mock predictions - in reality, this would use your trained model
            mock_predictions = [
                {
                    'name': 'T-Shirt',
                    'confidence': 85,
                    'category_info': MANVUE_CATEGORY_MAP['T-Shirt']
                },
                {
                    'name': 'Shirt', 
                    'confidence': 72,
                    'category_info': MANVUE_CATEGORY_MAP['Shirt']
                }
            ]
            
            detected_items = []
            for pred in mock_predictions:
                category_info = pred['category_info']
                detected_items.append(DetectedItem(
                    name=pred['name'],
                    confidence=pred['confidence'],
                    category=category_info['category'],
                    type=category_info['type'],
                    confidence_boost=category_info['confidence_boost']
                ))
            
            return detected_items
        
        except Exception as e:
            logger.error(f"Error processing image with ML: {e}")
            raise
    
    async def extract_colors(self, image_data: str) -> List[ColorInfo]:
        """
        Extract colors from image
        
        Args:
            image_data: Base64 encoded image data
            
        Returns:
            List of ColorInfo
        """
        try:
            # Mock color extraction - replace with actual image processing
            mock_colors = [
                ColorInfo(hex="#ffffff", name="White", dominance=0.65),
                ColorInfo(hex="#000000", name="Black", dominance=0.20),
                ColorInfo(hex="#808080", name="Gray", dominance=0.15)
            ]
            
            return mock_colors
        
        except Exception as e:
            logger.error(f"Error extracting colors: {e}")
            raise
    
    async def categorize_image(self, image_data: str) -> Dict[str, Any]:
        """
        Categorize fashion item from image
        
        Args:
            image_data: Base64 encoded image data
            
        Returns:
            Category information
        """
        try:
            predictions = await self._process_image_ml(image_data)
            
            if predictions:
                top_prediction = predictions[0]
                return {
                    "category": top_prediction.category,
                    "type": top_prediction.type,
                    "confidence": top_prediction.confidence,
                    "item_name": top_prediction.name
                }
            
            return {
                "category": "unknown",
                "type": "unknown", 
                "confidence": 0,
                "item_name": "Unknown"
            }
        
        except Exception as e:
            logger.error(f"Error categorizing image: {e}")
            raise
    
    async def compute_similarity(self, image_path: str, text: str) -> float:
        """
        Compute similarity between image and text
        
        Args:
            image_path: Path to image file
            text: Text to compare
            
        Returns:
            Similarity score (0.0 to 1.0)
        """
        try:
            if not self.ml_available:
                # Return mock similarity for demo
                return 0.75
            
            # This would use CLIP or similar model for actual similarity computation
            # For now, return a mock similarity score
            return 0.82
        
        except Exception as e:
            logger.error(f"Error computing similarity: {e}")
            raise
    
    def get_available_categories(self) -> List[Dict[str, Any]]:
        """
        Get available ML categories
        
        Returns:
            List of category information
        """
        try:
            categories = [
                {"name": "tops", "types": ["t-shirt", "shirt", "pullover"], "confidence": 0.9},
                {"name": "bottoms", "types": ["jeans", "trousers", "shorts"], "confidence": 0.85},
                {"name": "shoes", "types": ["sneakers", "boots", "sandals"], "confidence": 0.88},
                {"name": "outerwear", "types": ["coat", "jacket", "blazer"], "confidence": 0.82},
                {"name": "accessories", "types": ["bag", "belt", "hat"], "confidence": 0.75}
            ]
            
            return categories
        
        except Exception as e:
            logger.error(f"Error getting categories: {e}")
            return []
    
    def _get_mock_predictions(self, include_colors: bool = True) -> MLPredictionResponse:
        """
        Get mock predictions for demo purposes
        
        Args:
            include_colors: Whether to include color analysis
            
        Returns:
            MLPredictionResponse with mock data
        """
        mock_items = [
            DetectedItem(
                name="T-Shirt",
                confidence=85,
                category="tops",
                type="tops",
                confidence_boost=0.15
            ),
            DetectedItem(
                name="Jeans",
                confidence=72,
                category="bottoms", 
                type="bottoms",
                confidence_boost=0.16
            )
        ]
        
        mock_colors = []
        if include_colors:
            mock_colors = [
                ColorInfo(hex="#ffffff", name="White", dominance=0.65),
                ColorInfo(hex="#000080", name="Navy", dominance=0.35)
            ]
        
        return MLPredictionResponse(
            success=True,
            detected_items=mock_items,
            colors=mock_colors,
            overall_confidence=85,
            processing_time="0.25s",
            model_version=self.model_version
        )
