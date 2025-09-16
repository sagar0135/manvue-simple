#!/usr/bin/env python3
"""
Fashion Recommender Flask API
Main application file for the fashion recommender system
"""

import os
import sys
import logging
from datetime import datetime
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename

# Add current directory to path for imports
sys.path.append(os.path.dirname(__file__))

# Import configuration and services
from core.config import get_settings
from database import get_database_connection
from models.fashion_classifier import FashionClassifier
from utils.image_processor import ImageProcessor
from utils.model_loader import ModelLoader

# Get settings
settings = get_settings()

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.get('LOG_LEVEL', 'INFO')),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = settings.get('SECRET_KEY', 'your-secret-key-here')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Enable CORS
CORS(app)

# Initialize services
db = get_database_connection()
model_loader = ModelLoader()
image_processor = ImageProcessor()

# Global variables for loaded models
fashion_classifier = None
recommendation_model = None

def load_models():
    """Load ML models on startup"""
    global fashion_classifier, recommendation_model
    
    try:
        # Load fashion classification model
        fashion_classifier = model_loader.load_fashion_classifier()
        logger.info("✅ Fashion classifier loaded successfully")
        
        # Load recommendation model
        recommendation_model = model_loader.load_recommendation_model()
        logger.info("✅ Recommendation model loaded successfully")
        
    except Exception as e:
        logger.error(f"❌ Error loading models: {e}")
        fashion_classifier = None
        recommendation_model = None

# Application state
app_start_time = datetime.now()

# Routes
@app.route('/')
def home():
    """Home endpoint with API information"""
    return jsonify({
        "message": "Fashion Recommender API",
        "version": "1.0.0",
        "description": "AI-powered fashion recommendation system",
        "features": [
            "Fashion Classification",
            "Style Recommendations", 
            "Color Analysis",
            "Similar Item Search",
            "Trend Analysis"
        ],
        "endpoints": {
            "classify": "POST /api/classify",
            "recommend": "POST /api/recommend",
            "analyze_colors": "POST /api/analyze-colors",
            "similar_items": "POST /api/similar-items",
            "health": "GET /health"
        }
    })

@app.route('/health')
def health_check():
    """Health check endpoint"""
    try:
        # Check database connection
        db_status = "connected" if db else "disconnected"
        
        # Check model availability
        model_status = "loaded" if fashion_classifier else "not_loaded"
        
        # Calculate uptime
        uptime = str(datetime.now() - app_start_time)
        
        return jsonify({
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "uptime": uptime,
            "services": {
                "database": db_status,
                "ml_models": model_status
            }
        })
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/classify', methods=['POST'])
def classify_fashion():
    """Classify fashion items from uploaded images"""
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image file provided"}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({"error": "No image file selected"}), 400
        
        if not fashion_classifier:
            return jsonify({"error": "Fashion classifier not available"}), 503
        
        # Process image
        image_data = image_processor.process_uploaded_image(file)
        
        # Classify
        predictions = fashion_classifier.predict(image_data)
        
        return jsonify({
            "predictions": predictions,
            "top_prediction": max(predictions, key=predictions.get),
            "confidence": max(predictions.values())
        })
        
    except Exception as e:
        logger.error(f"Classification error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/recommend', methods=['POST'])
def recommend_items():
    """Get fashion recommendations based on input"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No input data provided"}), 400
        
        # Extract input parameters
        user_preferences = data.get('preferences', {})
        current_items = data.get('current_items', [])
        style_type = data.get('style_type', 'casual')
        
        if not recommendation_model:
            return jsonify({"error": "Recommendation model not available"}), 503
        
        # Generate recommendations
        recommendations = recommendation_model.recommend(
            user_preferences=user_preferences,
            current_items=current_items,
            style_type=style_type
        )
        
        return jsonify({
            "recommendations": recommendations,
            "style_type": style_type,
            "count": len(recommendations)
        })
        
    except Exception as e:
        logger.error(f"Recommendation error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/analyze-colors', methods=['POST'])
def analyze_colors():
    """Analyze colors in uploaded image"""
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image file provided"}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({"error": "No image file selected"}), 400
        
        # Process image for color analysis
        color_analysis = image_processor.analyze_colors(file)
        
        return jsonify({
            "dominant_colors": color_analysis['dominant_colors'],
            "color_palette": color_analysis['color_palette'],
            "color_distribution": color_analysis['color_distribution']
        })
        
    except Exception as e:
        logger.error(f"Color analysis error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/similar-items', methods=['POST'])
def find_similar_items():
    """Find similar items based on uploaded image"""
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image file provided"}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({"error": "No image file selected"}), 400
        
        # Process image
        image_features = image_processor.extract_features(file)
        
        # Find similar items in database
        similar_items = db.find_similar_items(image_features)
        
        return jsonify({
            "similar_items": similar_items,
            "count": len(similar_items)
        })
        
    except Exception as e:
        logger.error(f"Similar items error: {e}")
        return jsonify({"error": str(e)}), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Not Found",
        "message": "The requested endpoint was not found"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "Internal Server Error",
        "message": "An unexpected error occurred"
    }), 500

# Startup event
@app.before_first_request
def startup():
    """Initialize the application"""
    logger.info("🚀 Starting Fashion Recommender API")
    load_models()
    logger.info("✅ Application startup complete")

if __name__ == '__main__':
    # Load models before starting
    load_models()
    
    # Start Flask app
    app.run(
        host=settings.get('HOST', '0.0.0.0'),
        port=int(settings.get('PORT', 5000)),
        debug=settings.get('DEBUG', False)
    )
