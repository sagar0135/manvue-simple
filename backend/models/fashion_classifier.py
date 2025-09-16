"""
Fashion Classification Model
Handles fashion item classification using pre-trained models
"""

import numpy as np
import logging
from typing import Dict, List, Any, Optional
import tensorflow as tf
from tensorflow.keras.applications import ResNet50, VGG16, MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam

logger = logging.getLogger(__name__)

class FashionClassifier:
    """Fashion classification model wrapper"""
    
    def __init__(self, model_path: str = None, base_model: str = "ResNet50"):
        self.model_path = model_path
        self.base_model = base_model
        self.model = None
        self.class_names = [
            "T-shirt/top", "Trouser", "Pullover", "Dress", "Coat",
            "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot"
        ]
        self._load_model()
    
    def _load_model(self):
        """Load the fashion classification model"""
        try:
            if self.model_path and tf.io.gfile.exists(self.model_path):
                # Load pre-trained model
                self.model = tf.keras.models.load_model(self.model_path)
                logger.info(f"✅ Loaded pre-trained model from {self.model_path}")
            else:
                # Create new model
                self.model = self._create_model()
                logger.info("✅ Created new fashion classification model")
        except Exception as e:
            logger.error(f"❌ Error loading model: {e}")
            self.model = self._create_model()
    
    def _create_model(self) -> Model:
        """Create a new fashion classification model"""
        # Load base model
        if self.base_model == "ResNet50":
            base = ResNet50(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
        elif self.base_model == "VGG16":
            base = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
        elif self.base_model == "MobileNetV2":
            base = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
        else:
            raise ValueError(f"Unsupported base model: {self.base_model}")
        
        # Freeze base model
        base.trainable = False
        
        # Add classification head
        x = base.output
        x = GlobalAveragePooling2D()(x)
        x = Dense(512, activation='relu')(x)
        x = Dropout(0.5)(x)
        x = Dense(256, activation='relu')(x)
        x = Dropout(0.3)(x)
        predictions = Dense(len(self.class_names), activation='softmax')(x)
        
        # Create model
        model = Model(inputs=base.input, outputs=predictions)
        
        # Compile model
        model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def predict(self, image: np.ndarray) -> Dict[str, float]:
        """Predict fashion category from image"""
        try:
            if self.model is None:
                raise ValueError("Model not loaded")
            
            # Ensure image has correct shape
            if len(image.shape) == 3:
                image = np.expand_dims(image, axis=0)
            
            # Make prediction
            predictions = self.model.predict(image, verbose=0)
            
            # Convert to class probabilities
            class_probs = {}
            for i, class_name in enumerate(self.class_names):
                class_probs[class_name] = float(predictions[0][i])
            
            return class_probs
            
        except Exception as e:
            logger.error(f"❌ Error making prediction: {e}")
            return {}
    
    def predict_top_k(self, image: np.ndarray, k: int = 3) -> List[Dict[str, Any]]:
        """Get top-k predictions"""
        try:
            predictions = self.predict(image)
            
            # Sort by probability
            sorted_predictions = sorted(
                predictions.items(), 
                key=lambda x: x[1], 
                reverse=True
            )
            
            # Return top-k
            top_k = []
            for i, (class_name, prob) in enumerate(sorted_predictions[:k]):
                top_k.append({
                    "class": class_name,
                    "probability": prob,
                    "rank": i + 1
                })
            
            return top_k
            
        except Exception as e:
            logger.error(f"❌ Error getting top-k predictions: {e}")
            return []
    
    def get_class_confidence(self, image: np.ndarray, class_name: str) -> float:
        """Get confidence for a specific class"""
        try:
            predictions = self.predict(image)
            return predictions.get(class_name, 0.0)
        except Exception as e:
            logger.error(f"❌ Error getting class confidence: {e}")
            return 0.0
    
    def is_available(self) -> bool:
        """Check if model is available"""
        return self.model is not None
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get model information"""
        return {
            "base_model": self.base_model,
            "num_classes": len(self.class_names),
            "class_names": self.class_names,
            "model_path": self.model_path,
            "available": self.is_available()
        }
