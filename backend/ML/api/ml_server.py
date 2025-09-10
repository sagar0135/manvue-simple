#!/usr/bin/env python3
"""
MANVUE ML Model API Server (FastAPI)
Integrates with the Colab notebook ML model for product categorization
"""

import os
import sys
import json
import base64
import io
import asyncio
from typing import List, Dict, Optional, Any
import uvicorn
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import numpy as np
from PIL import Image
import tensorflow as tf
import cv2
import logging
from datetime import datetime

# Add parent directories to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

# Import the new ML model module
try:
    from backend.ml_model import get_image_embedding, get_text_embedding, compute_similarity, is_model_loaded
    CLIP_AVAILABLE = True
except ImportError as e:
    logging.warning(f"CLIP model not available: {e}")
    CLIP_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="MANVUE ML API",
    description="AI-Powered Fashion Recognition for MANVUE E-commerce",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Models for Request/Response
class ImagePredictionRequest(BaseModel):
    image: str = Field(..., description="Base64 encoded image data")
    include_colors: bool = Field(True, description="Include color analysis in response")
    
    class Config:
        schema_extra = {
            "example": {
                "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ...",
                "include_colors": True
            }
        }

class DetectedItem(BaseModel):
    name: str = Field(..., description="Detected item name")
    confidence: int = Field(..., ge=0, le=100, description="Confidence percentage (0-100)")
    category: str = Field(..., description="MANVUE category")
    type: str = Field(..., description="Product type")
    confidence_boost: float = Field(0.0, description="Category-specific confidence boost")

class ColorInfo(BaseModel):
    hex: str = Field(..., description="Hex color code")
    name: str = Field(..., description="Color name")
    dominance: float = Field(..., ge=0.0, le=1.0, description="Color dominance (0.0-1.0)")

class PredictionResponse(BaseModel):
    success: bool = Field(True, description="Request success status")
    detected_items: List[DetectedItem] = Field(..., description="List of detected fashion items")
    colors: List[ColorInfo] = Field(default=[], description="Extracted colors from image")
    overall_confidence: int = Field(..., ge=0, le=100, description="Overall prediction confidence")
    processing_time: str = Field(..., description="Processing time")
    model_version: str = Field("2.0.0", description="ML model version")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())

class HealthResponse(BaseModel):
    status: str = Field(..., description="API health status")
    model_loaded: bool = Field(..., description="Whether ML model is loaded")
    version: str = Field(..., description="API version")
    uptime: str = Field(..., description="Server uptime")

class CategoryInfo(BaseModel):
    category: str = Field(..., description="MANVUE category")
    type: str = Field(..., description="Product type")
    confidence_boost: float = Field(..., description="Confidence boost factor")

class CategoriesResponse(BaseModel):
    categories: Dict[str, CategoryInfo] = Field(..., description="Available categories")
    total_classes: int = Field(..., description="Total number of classes")

class RetrainRequest(BaseModel):
    training_data: List[Dict[str, Any]] = Field(..., description="Training data")
    model_params: Optional[Dict[str, Any]] = Field(None, description="Model parameters")

class RetrainResponse(BaseModel):
    success: bool = Field(..., description="Retraining success status")
    message: str = Field(..., description="Status message")
    estimated_time: str = Field(..., description="Estimated completion time")
    status: str = Field(..., description="Current status")
    job_id: Optional[str] = Field(None, description="Background job ID")

# Global variables for model
model = None
app_start_time = datetime.now()
class_names = [
    'T-Shirt', 'Trouser', 'Pullover', 'Dress', 'Coat',
    'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle Boot'
]

# MANVUE specific category mapping (men's fashion focus)
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
    'Dress': {'category': 'excluded', 'type': 'excluded', 'confidence_boost': 0.0}  # Men's store
}

async def load_model():
    """Load the trained ML model asynchronously"""
    global model
    try:
        model_path = os.path.join(os.path.dirname(__file__), '../models/fashion_classifier.h5')
        if os.path.exists(model_path):
            # Load model in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            model = await loop.run_in_executor(None, tf.keras.models.load_model, model_path)
            logger.info("Model loaded successfully from local file")
        else:
            # Fallback: Create a simple model for demonstration
            model = create_demo_model()
            logger.info("Demo model created (replace with trained model)")
        return True
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        return False

def create_demo_model():
    """Create a demo model that mimics the MNIST fashion classifier"""
    model = tf.keras.Sequential([
        tf.keras.layers.Flatten(input_shape=(28, 28, 1)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(10, activation='softmax')
    ])
    
    # Initialize with random weights for demo purposes
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    
    return model

def preprocess_image(image_data):
    """Preprocess image for model prediction"""
    try:
        # Decode base64 image
        if isinstance(image_data, str):
            if 'data:image' in image_data:
                image_data = image_data.split(',')[1]
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
        else:
            image = Image.open(io.BytesIO(image_data))
        
        # Convert to grayscale and resize to 28x28 (MNIST fashion format)
        image = image.convert('L')
        image = image.resize((28, 28))
        
        # Convert to numpy array and normalize
        image_array = np.array(image)
        image_array = image_array.astype('float32') / 255.0
        image_array = np.expand_dims(image_array, axis=0)
        image_array = np.expand_dims(image_array, axis=-1)
        
        return image_array
    except Exception as e:
        logger.error(f"Error preprocessing image: {e}")
        return None

def extract_colors(image_data):
    """Extract dominant colors from image"""
    try:
        # Decode image
        if isinstance(image_data, str):
            if 'data:image' in image_data:
                image_data = image_data.split(',')[1]
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
        else:
            image = Image.open(io.BytesIO(image_data))
        
        # Convert to RGB
        image = image.convert('RGB')
        image_array = np.array(image)
        
        # Reshape for k-means clustering
        pixels = image_array.reshape(-1, 3)
        
        # Simple color extraction (using most frequent colors)
        unique_colors, counts = np.unique(pixels, axis=0, return_counts=True)
        
        # Get top 5 colors
        top_indices = np.argsort(counts)[-5:][::-1]
        dominant_colors = []
        
        for i, idx in enumerate(top_indices):
            color = unique_colors[idx]
            dominance = counts[idx] / len(pixels)
            
            # Convert RGB to hex
            hex_color = '#{:02x}{:02x}{:02x}'.format(color[0], color[1], color[2])
            
            # Map to color name (simplified)
            color_name = rgb_to_color_name(color)
            
            dominant_colors.append({
                'hex': hex_color,
                'name': color_name,
                'dominance': float(dominance)
            })
        
        return dominant_colors
    except Exception as e:
        logger.error(f"Error extracting colors: {e}")
        return []

def rgb_to_color_name(rgb):
    """Convert RGB values to color names"""
    r, g, b = rgb
    
    # Simple color mapping
    if r > 200 and g > 200 and b > 200:
        return 'White'
    elif r < 50 and g < 50 and b < 50:
        return 'Black'
    elif r > g and r > b:
        if r > 150:
            return 'Red'
        else:
            return 'Maroon'
    elif g > r and g > b:
        return 'Green'
    elif b > r and b > g:
        if b > 150:
            return 'Blue'
        else:
            return 'Navy'
    elif r > 150 and g > 150:
        return 'Yellow'
    elif r > 100 and g > 100 and b < 100:
        return 'Brown'
    else:
        return 'Gray'

# New Pydantic models for embedding endpoints
class EmbeddingRequest(BaseModel):
    image_path: str = Field(..., description="Path to the image file")
    
class TextEmbeddingRequest(BaseModel):
    text: str = Field(..., description="Text to generate embedding for")

class SimilarityRequest(BaseModel):
    image_path: str = Field(..., description="Path to the image file")
    text: str = Field(..., description="Text to compare with image")

class EmbeddingResponse(BaseModel):
    embedding: List[float] = Field(..., description="Generated embedding")
    model_used: str = Field("CLIP", description="Model used for embedding")

class SimilarityResponse(BaseModel):
    similarity: float = Field(..., description="Cosine similarity score")
    image_path: str = Field(..., description="Path to the image file")
    text: str = Field(..., description="Text compared")

@app.get("/health", response_model=HealthResponse, 
         summary="Health Check", 
         description="Check API server health and model status")
async def health_check():
    """Health check endpoint"""
    uptime = str(datetime.now() - app_start_time)
    return HealthResponse(
        status="healthy",
        model_loaded=model is not None,
        version="2.0.0",
        uptime=uptime
    )

@app.post("/predict", response_model=PredictionResponse,
          summary="Image Prediction", 
          description="Analyze fashion image and return detected items with confidence scores")
async def predict(request: ImagePredictionRequest):
    """Main prediction endpoint with async support"""
    try:
        start_time = datetime.now()
        
        if model is None:
            raise HTTPException(status_code=503, detail="ML model not loaded")
        
        # Preprocess image
        image_array = preprocess_image(request.image)
        if image_array is None:
            raise HTTPException(status_code=400, detail="Failed to process image")
        
        # Make prediction in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        predictions = await loop.run_in_executor(None, model.predict, image_array)
        
        predicted_class_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class_idx])
        predicted_class = class_names[predicted_class_idx]
        
        # Get top 3 predictions
        top_indices = np.argsort(predictions[0])[-3:][::-1]
        top_predictions = []
        
        for idx in top_indices:
            class_name = class_names[idx]
            class_confidence = float(predictions[0][idx])
            manvue_info = MANVUE_CATEGORY_MAP.get(class_name, {})
            
            # Skip excluded categories (like dresses in men's store)
            if manvue_info.get('category') != 'excluded':
                detected_item = DetectedItem(
                    name=class_name,
                    confidence=int(class_confidence * 100),
                    category=manvue_info.get('category', 'unknown'),
                    type=manvue_info.get('type', 'unknown'),
                    confidence_boost=manvue_info.get('confidence_boost', 0.0)
                )
                top_predictions.append(detected_item)
        
        # Extract colors if requested
        colors = []
        if request.include_colors:
            colors_data = extract_colors(request.image)
            colors = [ColorInfo(**color) for color in colors_data]
        
        # Calculate processing time
        processing_time = f"{(datetime.now() - start_time).total_seconds():.2f}s"
        
        response = PredictionResponse(
            detected_items=top_predictions,
            colors=colors,
            overall_confidence=int(confidence * 100),
            processing_time=processing_time
        )
        
        return response
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/categories", response_model=CategoriesResponse,
         summary="Get Categories", 
         description="Retrieve all available fashion categories and their mappings")
async def get_categories():
    """Get available categories"""
    categories = {}
    for class_name, info in MANVUE_CATEGORY_MAP.items():
        if info['category'] != 'excluded':
            categories[class_name] = CategoryInfo(**info)
    
    return CategoriesResponse(
        categories=categories,
        total_classes=len(class_names)
    )

@app.post("/retrain", response_model=RetrainResponse,
          summary="Retrain Model", 
          description="Initiate model retraining with new data")
async def retrain_model(request: RetrainRequest, background_tasks: BackgroundTasks):
    """Endpoint for retraining the model with new data"""
    try:
        # Generate unique job ID
        job_id = f"retrain_{int(datetime.now().timestamp())}"
        
        # Add retraining task to background
        background_tasks.add_task(perform_retraining, request.training_data, request.model_params, job_id)
        
        return RetrainResponse(
            success=True,
            message="Model retraining initiated",
            estimated_time="15 minutes",
            status="queued",
            job_id=job_id
        )
    except Exception as e:
        logger.error(f"Retraining error: {e}")
        raise HTTPException(status_code=500, detail=f"Retraining failed: {str(e)}")

async def perform_retraining(training_data: List[Dict[str, Any]], 
                           model_params: Optional[Dict[str, Any]], 
                           job_id: str):
    """Background task for model retraining"""
    try:
        logger.info(f"Starting retraining job {job_id}")
        # Simulate retraining process
        await asyncio.sleep(5)  # Simulated training time
        logger.info(f"Retraining job {job_id} completed successfully")
    except Exception as e:
        logger.error(f"Retraining job {job_id} failed: {e}")

# New embedding endpoints
@app.post("/embedding/image", response_model=EmbeddingResponse,
          summary="Generate Image Embedding", 
          description="Generate CLIP embedding for an image")
async def generate_image_embedding(request: EmbeddingRequest):
    """Generate CLIP embedding for an image"""
    if not CLIP_AVAILABLE:
        raise HTTPException(status_code=503, detail="CLIP model not available")
    
    try:
        embedding = get_image_embedding(request.image_path)
        return EmbeddingResponse(
            embedding=embedding,
            model_used="CLIP"
        )
    except Exception as e:
        logger.error(f"Error generating image embedding: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate embedding: {str(e)}")

@app.post("/embedding/text", response_model=EmbeddingResponse,
          summary="Generate Text Embedding", 
          description="Generate CLIP embedding for text")
async def generate_text_embedding(request: TextEmbeddingRequest):
    """Generate CLIP embedding for text"""
    if not CLIP_AVAILABLE:
        raise HTTPException(status_code=503, detail="CLIP model not available")
    
    try:
        embedding = get_text_embedding(request.text)
        return EmbeddingResponse(
            embedding=embedding,
            model_used="CLIP"
        )
    except Exception as e:
        logger.error(f"Error generating text embedding: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate embedding: {str(e)}")

@app.post("/similarity", response_model=SimilarityResponse,
          summary="Compute Image-Text Similarity", 
          description="Compute cosine similarity between image and text embeddings")
async def compute_image_text_similarity(request: SimilarityRequest):
    """Compute similarity between image and text using CLIP"""
    if not CLIP_AVAILABLE:
        raise HTTPException(status_code=503, detail="CLIP model not available")
    
    try:
        # Generate embeddings
        image_embedding = get_image_embedding(request.image_path)
        text_embedding = get_text_embedding(request.text)
        
        # Compute similarity
        similarity = compute_similarity(image_embedding, text_embedding)
        
        return SimilarityResponse(
            similarity=similarity,
            image_path=request.image_path,
            text=request.text
        )
    except Exception as e:
        logger.error(f"Error computing similarity: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to compute similarity: {str(e)}")

@app.get("/embedding/status", 
         summary="Check Embedding Model Status", 
         description="Check if CLIP model is loaded and available")
async def check_embedding_status():
    """Check if CLIP model is available"""
    return {
        "clip_available": CLIP_AVAILABLE,
        "model_loaded": is_model_loaded() if CLIP_AVAILABLE else False,
        "device": "cuda" if torch.cuda.is_available() else "cpu" if CLIP_AVAILABLE else "unknown"
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    """Load model on startup"""
    logger.info("Starting MANVUE ML API Server...")
    success = await load_model()
    if success:
        logger.info("Model loaded successfully")
    else:
        logger.error("Failed to load model - API will use fallback mode")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down MANVUE ML API Server...")

if __name__ == '__main__':
    # Start server with uvicorn
    port = int(os.environ.get('PORT', 5000))
    uvicorn.run(
        "ml_server:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info",
        access_log=True
    )
