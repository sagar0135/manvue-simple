"""
Model loading utilities for fashion recommender
Handles loading of pre-trained ML models
"""

import os
import logging
from typing import Optional, Any
import numpy as np
from pathlib import Path

logger = logging.getLogger(__name__)

class ModelLoader:
    """Utility class for loading ML models"""
    
    def __init__(self, models_dir: str = "../models"):
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(exist_ok=True)
    
    def load_fashion_classifier(self) -> Optional[Any]:
        """Load the fashion classification model"""
        try:
            model_path = self.models_dir / "fashion_classifier.h5"
            
            if not model_path.exists():
                logger.warning(f"Fashion classifier model not found at {model_path}")
                return None
            
            # Load TensorFlow model
            import tensorflow as tf
            model = tf.keras.models.load_model(str(model_path))
            
            logger.info("✅ Fashion classifier loaded successfully")
            return model
            
        except Exception as e:
            logger.error(f"❌ Error loading fashion classifier: {e}")
            return None
    
    def load_recommendation_model(self) -> Optional[Any]:
        """Load the recommendation model"""
        try:
            model_path = self.models_dir / "recommendation_model.pkl"
            
            if not model_path.exists():
                logger.warning(f"Recommendation model not found at {model_path}")
                return None
            
            # Load scikit-learn model
            import pickle
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            
            logger.info("✅ Recommendation model loaded successfully")
            return model
            
        except Exception as e:
            logger.error(f"❌ Error loading recommendation model: {e}")
            return None
    
    def load_color_analyzer(self) -> Optional[Any]:
        """Load the color analysis model"""
        try:
            model_path = self.models_dir / "color_analyzer.pkl"
            
            if not model_path.exists():
                logger.warning(f"Color analyzer model not found at {model_path}")
                return None
            
            import pickle
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            
            logger.info("✅ Color analyzer loaded successfully")
            return model
            
        except Exception as e:
            logger.error(f"❌ Error loading color analyzer: {e}")
            return None
    
    def save_model(self, model: Any, model_name: str, model_type: str = "tf") -> bool:
        """Save a model to the models directory"""
        try:
            if model_type == "tf":
                model_path = self.models_dir / f"{model_name}.h5"
                model.save(str(model_path))
            elif model_type == "sklearn":
                model_path = self.models_dir / f"{model_name}.pkl"
                import pickle
                with open(model_path, 'wb') as f:
                    pickle.dump(model, f)
            else:
                raise ValueError(f"Unsupported model type: {model_type}")
            
            logger.info(f"✅ Model saved to {model_path}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error saving model: {e}")
            return False
    
    def list_available_models(self) -> list:
        """List all available models in the models directory"""
        try:
            models = []
            for file_path in self.models_dir.glob("*"):
                if file_path.is_file():
                    models.append({
                        "name": file_path.stem,
                        "extension": file_path.suffix,
                        "size": file_path.stat().st_size,
                        "path": str(file_path)
                    })
            return models
        except Exception as e:
            logger.error(f"❌ Error listing models: {e}")
            return []
    
    def model_exists(self, model_name: str) -> bool:
        """Check if a model exists"""
        h5_path = self.models_dir / f"{model_name}.h5"
        pkl_path = self.models_dir / f"{model_name}.pkl"
        return h5_path.exists() or pkl_path.exists()
