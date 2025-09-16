"""
Image processing utilities for fashion recommender
Handles image preprocessing, feature extraction, and color analysis
"""

import cv2
import numpy as np
from PIL import Image
import io
from typing import Dict, List, Tuple, Any
import logging

logger = logging.getLogger(__name__)

class ImageProcessor:
    """Image processing utilities for fashion items"""
    
    def __init__(self, target_size: Tuple[int, int] = (224, 224)):
        self.target_size = target_size
    
    def process_uploaded_image(self, file) -> np.ndarray:
        """Process uploaded image file for ML prediction"""
        try:
            # Read image from file
            image_data = file.read()
            image = Image.open(io.BytesIO(image_data))
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize image
            image = image.resize(self.target_size)
            
            # Convert to numpy array and normalize
            image_array = np.array(image) / 255.0
            
            # Add batch dimension
            image_array = np.expand_dims(image_array, axis=0)
            
            return image_array
            
        except Exception as e:
            logger.error(f"Error processing uploaded image: {e}")
            raise
    
    def analyze_colors(self, file) -> Dict[str, Any]:
        """Analyze dominant colors in the image"""
        try:
            # Read image
            image_data = file.read()
            image = Image.open(io.BytesIO(image_data))
            image = image.convert('RGB')
            
            # Convert to numpy array
            image_array = np.array(image)
            
            # Reshape image to be a list of pixels
            pixels = image_array.reshape(-1, 3)
            
            # Use K-means to find dominant colors
            from sklearn.cluster import KMeans
            
            kmeans = KMeans(n_clusters=5, random_state=42)
            kmeans.fit(pixels)
            
            # Get dominant colors
            dominant_colors = kmeans.cluster_centers_.astype(int)
            
            # Calculate color distribution
            labels = kmeans.labels_
            color_counts = np.bincount(labels)
            color_percentages = color_counts / len(labels) * 100
            
            # Create color palette
            color_palette = []
            for i, color in enumerate(dominant_colors):
                color_palette.append({
                    'rgb': color.tolist(),
                    'hex': self._rgb_to_hex(color),
                    'percentage': float(color_percentages[i])
                })
            
            return {
                'dominant_colors': dominant_colors.tolist(),
                'color_palette': color_palette,
                'color_distribution': color_percentages.tolist()
            }
            
        except Exception as e:
            logger.error(f"Error analyzing colors: {e}")
            return {
                'dominant_colors': [],
                'color_palette': [],
                'color_distribution': []
            }
    
    def extract_features(self, file) -> np.ndarray:
        """Extract features from image for similarity search"""
        try:
            # Read and process image
            image_data = file.read()
            image = Image.open(io.BytesIO(image_data))
            image = image.convert('RGB')
            image = image.resize(self.target_size)
            
            # Convert to numpy array
            image_array = np.array(image)
            
            # Extract basic features (in production, use a pre-trained CNN)
            features = self._extract_basic_features(image_array)
            
            return features
            
        except Exception as e:
            logger.error(f"Error extracting features: {e}")
            return np.array([])
    
    def _extract_basic_features(self, image: np.ndarray) -> np.ndarray:
        """Extract basic image features"""
        # Convert to grayscale for some features
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        # Extract texture features using LBP
        lbp = self._local_binary_pattern(gray)
        
        # Extract color histogram
        hist_r = cv2.calcHist([image], [0], None, [32], [0, 256])
        hist_g = cv2.calcHist([image], [1], None, [32], [0, 256])
        hist_b = cv2.calcHist([image], [2], None, [32], [0, 256])
        
        # Combine features
        features = np.concatenate([
            lbp.flatten(),
            hist_r.flatten(),
            hist_g.flatten(),
            hist_b.flatten()
        ])
        
        return features
    
    def _local_binary_pattern(self, image: np.ndarray, radius: int = 1, n_points: int = 8) -> np.ndarray:
        """Calculate Local Binary Pattern"""
        # Simple LBP implementation
        rows, cols = image.shape
        lbp = np.zeros_like(image)
        
        for i in range(radius, rows - radius):
            for j in range(radius, cols - radius):
                center = image[i, j]
                binary_string = ''
                
                for k in range(n_points):
                    angle = 2 * np.pi * k / n_points
                    x = int(i + radius * np.cos(angle))
                    y = int(j + radius * np.sin(angle))
                    
                    if x < rows and y < cols:
                        binary_string += '1' if image[x, y] >= center else '0'
                    else:
                        binary_string += '0'
                
                lbp[i, j] = int(binary_string, 2)
        
        return lbp
    
    def _rgb_to_hex(self, rgb: np.ndarray) -> str:
        """Convert RGB array to hex color"""
        return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
    
    def resize_image(self, image: np.ndarray, size: Tuple[int, int]) -> np.ndarray:
        """Resize image to specified size"""
        return cv2.resize(image, size)
    
    def normalize_image(self, image: np.ndarray) -> np.ndarray:
        """Normalize image to [0, 1] range"""
        return image.astype(np.float32) / 255.0
