#!/usr/bin/env python3
"""
Enhanced MANVUE Backend Server with MongoDB and Image Storage
Includes image upload, ML integration, and full CRUD operations
"""

import json
import os
import io
import base64
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
import uvicorn
from fastapi import FastAPI, HTTPException, UploadFile, File, Form, BackgroundTasks, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
import hashlib
import secrets
from PIL import Image
import logging

# Import database functions
from database import (
    test_connection, store_image, store_image_base64, get_image, get_image_metadata,
    delete_image, list_images, create_product, get_product, get_products,
    update_product, delete_product, create_user, get_user_by_email, update_user
)

# ML integration
try:
    from ML.api.ml_server import predict, preprocess_image
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    logging.warning("ML server not available - running without ML features")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="MANVUE Enhanced API",
    description="Full-featured backend for MANVUE with MongoDB and ML integration",
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

# Pydantic Models
class User(BaseModel):
    email: str
    password: str
    name: Optional[str] = None

class UserResponse(BaseModel):
    id: str
    email: str
    name: Optional[str] = None
    created_at: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class Product(BaseModel):
    name: str
    title: Optional[str] = None
    price: float
    originalPrice: Optional[float] = None
    category: str
    type: str
    size: List[str] = []
    color: List[str] = []
    brand: Optional[str] = None
    rating: Optional[float] = 4.5
    reviews: Optional[int] = 0
    image_ids: List[str] = []  # GridFS image IDs
    image_urls: List[str] = []  # External image URLs (fallback)
    tags: List[str] = []
    inStock: bool = True
    description: Optional[str] = None
    features: List[str] = []

class ProductResponse(BaseModel):
    id: str
    name: str
    title: Optional[str] = None
    price: float
    originalPrice: Optional[float] = None
    category: str
    type: str
    size: List[str] = []
    color: List[str] = []
    brand: Optional[str] = None
    rating: Optional[float] = 4.5
    reviews: Optional[int] = 0
    image_ids: List[str] = []
    image_urls: List[str] = []
    image: Optional[str] = None  # Primary image URL for backward compatibility
    tags: List[str] = []
    inStock: bool = True
    description: Optional[str] = None
    features: List[str] = []
    created_at: str
    updated_at: str

class ImageUploadResponse(BaseModel):
    success: bool
    file_id: str
    filename: str
    content_type: str
    size: int
    image_url: str
    ml_predictions: Optional[Dict] = None

class ImageMetadataResponse(BaseModel):
    id: str
    filename: str
    content_type: str
    upload_date: str
    size: int
    metadata: Dict

class MLPredictionRequest(BaseModel):
    image_data: str = Field(..., description="Base64 encoded image data")
    include_colors: bool = Field(True, description="Include color analysis")

# Utility functions
def hash_password(password: str) -> str:
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password"""
    return hash_password(plain_password) == hashed_password

def create_token(user_email: str) -> str:
    """Create a simple token (not JWT for simplicity)"""
    return secrets.token_urlsafe(32)

def generate_image_url(file_id: str) -> str:
    """Generate image URL for given file ID"""
    return f"/api/images/{file_id}"

# API Endpoints

@app.get("/")
async def root():
    return {
        "message": "MANVUE Enhanced API Server",
        "version": "2.0.0",
        "features": ["MongoDB", "GridFS", "ML Integration", "Image Upload"]
    }

@app.get("/health")
async def health_check():
    """Enhanced health check with database connectivity"""
    db_connected = await test_connection()
    return {
        "status": "healthy" if db_connected else "degraded",
        "database": "connected" if db_connected else "disconnected",
        "ml_available": ML_AVAILABLE,
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0"
    }

# User Authentication Endpoints
@app.post("/register", response_model=UserResponse)
async def register(user: User):
    """Register a new user"""
    # Check if user already exists
    existing_user = await get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash password and create user
    user_data = {
        "email": user.email,
        "password": hash_password(user.password),
        "name": user.name
    }
    
    user_id = await create_user(user_data)
    
    return UserResponse(
        id=user_id,
        email=user.email,
        name=user.name,
        created_at=datetime.now().isoformat()
    )

@app.post("/login", response_model=LoginResponse)
async def login(user: User):
    """Login user"""
    stored_user = await get_user_by_email(user.email)
    if not stored_user or not verify_password(user.password, stored_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_token(user.email)
    
    return LoginResponse(
        access_token=token,
        token_type="bearer",
        user=UserResponse(
            id=stored_user["_id"],
            email=stored_user["email"],
            name=stored_user.get("name"),
            created_at=stored_user["created_at"].isoformat()
        )
    )

# Image Management Endpoints
@app.post("/api/images/upload", response_model=ImageUploadResponse)
async def upload_image(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    category: Optional[str] = Form(None),
    product_id: Optional[str] = Form(None)
):
    """Upload an image file and store in GridFS"""
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read file data
        file_data = await file.read()
        
        # Optional: Resize image to optimize storage
        try:
            img = Image.open(io.BytesIO(file_data))
            # Resize if too large (max 1920x1920)
            if img.width > 1920 or img.height > 1920:
                img.thumbnail((1920, 1920), Image.Resampling.LANCZOS)
                output = io.BytesIO()
                img.save(output, format=img.format or 'JPEG', quality=85)
                file_data = output.getvalue()
        except Exception as e:
            logger.warning(f"Could not optimize image: {e}")
        
        # Store in GridFS
        metadata = {
            "category": category,
            "product_id": product_id,
            "original_filename": file.filename
        }
        
        file_id = await store_image(file_data, file.filename, file.content_type, metadata)
        
        # Generate response
        response = ImageUploadResponse(
            success=True,
            file_id=file_id,
            filename=file.filename,
            content_type=file.content_type,
            size=len(file_data),
            image_url=generate_image_url(file_id)
        )
        
        # Add ML prediction in background if available
        if ML_AVAILABLE:
            background_tasks.add_task(process_image_ml, file_id, file_data)
        
        return response
    
    except Exception as e:
        logger.error(f"Error uploading image: {e}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.post("/api/images/upload-base64", response_model=ImageUploadResponse)
async def upload_image_base64(
    background_tasks: BackgroundTasks,
    image_data: str = Form(...),
    filename: str = Form(...),
    category: Optional[str] = Form(None),
    product_id: Optional[str] = Form(None)
):
    """Upload base64 encoded image (for Colab integration)"""
    try:
        # Store in GridFS
        metadata = {
            "category": category,
            "product_id": product_id,
            "original_filename": filename,
            "upload_method": "base64"
        }
        
        file_id = await store_image_base64(image_data, filename, "image/jpeg", metadata)
        
        # Get stored file size
        image_meta = await get_image_metadata(file_id)
        
        response = ImageUploadResponse(
            success=True,
            file_id=file_id,
            filename=filename,
            content_type="image/jpeg",
            size=image_meta["length"] if image_meta else 0,
            image_url=generate_image_url(file_id)
        )
        
        # Add ML prediction in background if available
        if ML_AVAILABLE:
            # Decode base64 for ML processing
            if image_data.startswith('data:'):
                image_data = image_data.split(',')[1]
            image_bytes = base64.b64decode(image_data)
            background_tasks.add_task(process_image_ml, file_id, image_bytes)
        
        return response
    
    except Exception as e:
        logger.error(f"Error uploading base64 image: {e}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.get("/api/images/{file_id}")
async def get_image_file(file_id: str):
    """Retrieve image file from GridFS"""
    try:
        image_data = await get_image(file_id)
        if not image_data:
            raise HTTPException(status_code=404, detail="Image not found")
        
        # Get metadata for content type
        metadata = await get_image_metadata(file_id)
        content_type = metadata.get("content_type", "image/jpeg") if metadata else "image/jpeg"
        
        return StreamingResponse(
            io.BytesIO(image_data),
            media_type=content_type,
            headers={"Cache-Control": "max-age=86400"}  # Cache for 24 hours
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving image {file_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve image")

@app.get("/api/images/{file_id}/metadata", response_model=ImageMetadataResponse)
async def get_image_info(file_id: str):
    """Get image metadata"""
    metadata = await get_image_metadata(file_id)
    if not metadata:
        raise HTTPException(status_code=404, detail="Image not found")
    
    return ImageMetadataResponse(
        id=file_id,
        filename=metadata["filename"],
        content_type=metadata["content_type"],
        upload_date=metadata["upload_date"].isoformat(),
        size=metadata["length"],
        metadata={k: v for k, v in metadata.items() if k not in ["filename", "content_type", "upload_date", "length"]}
    )

@app.delete("/api/images/{file_id}")
async def delete_image_file(file_id: str):
    """Delete image from GridFS"""
    success = await delete_image(file_id)
    if not success:
        raise HTTPException(status_code=404, detail="Image not found")
    
    return {"success": True, "message": "Image deleted successfully"}

@app.get("/api/images", response_model=List[ImageMetadataResponse])
async def list_all_images(limit: int = 50, skip: int = 0, category: Optional[str] = None):
    """List all images with optional filtering"""
    images = await list_images(limit, skip)
    
    # Filter by category if specified
    if category:
        images = [img for img in images if img.get("category") == category]
    
    return [
        ImageMetadataResponse(
            id=img["id"],
            filename=img["filename"],
            content_type=img["content_type"],
            upload_date=img["upload_date"].isoformat(),
            size=img["length"],
            metadata={k: v for k, v in img.items() if k not in ["id", "filename", "content_type", "upload_date", "length"]}
        )
        for img in images
    ]

# Product Management Endpoints
@app.get("/products", response_model=List[ProductResponse])
async def get_all_products(category: Optional[str] = None, limit: int = 50, skip: int = 0):
    """Get all products with image URLs"""
    products = await get_products(category, limit, skip)
    
    # Convert to response format and add image URLs
    response_products = []
    for product in products:
        # Generate image URLs from GridFS IDs
        image_urls = [generate_image_url(img_id) for img_id in product.get("image_ids", [])]
        
        # Add external URLs if any
        image_urls.extend(product.get("image_urls", []))
        
        # Set primary image for backward compatibility
        primary_image = image_urls[0] if image_urls else None
        
        response_product = ProductResponse(
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
        response_products.append(response_product)
    
    return response_products

@app.get("/products/{product_id}", response_model=ProductResponse)
async def get_single_product(product_id: str):
    """Get a specific product"""
    product = await get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Generate image URLs
    image_urls = [generate_image_url(img_id) for img_id in product.get("image_ids", [])]
    image_urls.extend(product.get("image_urls", []))
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

@app.post("/products", response_model=ProductResponse)
async def create_new_product(product: Product):
    """Create a new product"""
    product_data = product.dict()
    product_id = await create_product(product_data)
    
    # Return the created product
    created_product = await get_product(product_id)
    image_urls = [generate_image_url(img_id) for img_id in created_product.get("image_ids", [])]
    image_urls.extend(created_product.get("image_urls", []))
    
    return ProductResponse(
        id=created_product["_id"],
        name=created_product["name"],
        title=created_product.get("title", created_product["name"]),
        price=created_product["price"],
        originalPrice=created_product.get("originalPrice"),
        category=created_product["category"],
        type=created_product["type"],
        size=created_product.get("size", []),
        color=created_product.get("color", []),
        brand=created_product.get("brand"),
        rating=created_product.get("rating", 4.5),
        reviews=created_product.get("reviews", 0),
        image_ids=created_product.get("image_ids", []),
        image_urls=image_urls,
        image=image_urls[0] if image_urls else None,
        tags=created_product.get("tags", []),
        inStock=created_product.get("inStock", True),
        description=created_product.get("description"),
        features=created_product.get("features", []),
        created_at=created_product["created_at"].isoformat(),
        updated_at=created_product["updated_at"].isoformat()
    )

@app.put("/products/{product_id}")
async def update_existing_product(product_id: str, product: Product):
    """Update an existing product"""
    update_data = product.dict(exclude_unset=True)
    success = await update_product(product_id, update_data)
    
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return {"success": True, "message": "Product updated successfully"}

@app.delete("/products/{product_id}")
async def delete_existing_product(product_id: str):
    """Delete a product"""
    success = await delete_product(product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return {"success": True, "message": "Product deleted successfully"}

# ML Integration Endpoints
@app.post("/api/ml/predict")
async def predict_image_ml(request: MLPredictionRequest):
    """Get ML predictions for an image"""
    if not ML_AVAILABLE:
        raise HTTPException(status_code=503, detail="ML service not available")
    
    try:
        # Process image with ML model
        prediction_response = await predict({
            "image": request.image_data,
            "include_colors": request.include_colors
        })
        
        return prediction_response
    
    except Exception as e:
        logger.error(f"ML prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

# Background tasks
async def process_image_ml(file_id: str, image_data: bytes):
    """Background task to process uploaded image with ML"""
    if not ML_AVAILABLE:
        return
    
    try:
        # Convert image to base64 for ML processing
        image_b64 = base64.b64encode(image_data).decode('utf-8')
        image_data_url = f"data:image/jpeg;base64,{image_b64}"
        
        # Get ML predictions
        prediction_response = await predict({
            "image": image_data_url,
            "include_colors": True
        })
        
        # Update image metadata with ML results
        metadata = await get_image_metadata(file_id)
        if metadata:
            metadata["ml_predictions"] = prediction_response
            # Note: In a real implementation, you'd update the GridFS metadata
            logger.info(f"ML processing completed for image {file_id}")
    
    except Exception as e:
        logger.error(f"Background ML processing failed for {file_id}: {e}")

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize the application"""
    logger.info("Starting MANVUE Enhanced API Server...")
    
    # Test database connection
    db_connected = await test_connection()
    if db_connected:
        logger.info("✅ Database connection established")
    else:
        logger.warning("⚠️ Database connection failed - some features may not work")
    
    # Check ML availability
    if ML_AVAILABLE:
        logger.info("✅ ML services available")
    else:
        logger.warning("⚠️ ML services not available")
    
    logger.info("🚀 MANVUE Enhanced API Server started successfully")

if __name__ == "__main__":
    # Start server
    port = int(os.environ.get("PORT", 5001))
    uvicorn.run(
        "enhanced_main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )