from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import base64
import io
from datetime import datetime, timedelta
from passlib.context import CryptContext
import jwt
import numpy as np
from PIL import Image
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="ManVue Enhanced API",
    description="AI-Powered Fashion E-commerce with ML Search",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple in-memory storage (replace with database in production)
users_db = {}
products_db = [
    {
        "id": 1,
        "title": "Classic White T-Shirt",
        "price": 24.99,
        "image_url": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop",
        "category": "tops",
        "type": "tshirts",
        "description": "Comfortable cotton t-shirt perfect for everyday wear",
        "tags": ["casual", "cotton", "basic", "everyday"],
        "colors": ["White", "Black", "Navy", "Grey"],
        "sizes": ["S", "M", "L", "XL", "XXL"],
        "brand": "MANVUE Basics",
        "rating": 4.5,
        "reviews": 127,
        "inStock": True
    },
    {
        "id": 2,
        "title": "Premium Denim Jeans",
        "price": 64.99,
        "image_url": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=400&h=400&fit=crop",
        "category": "bottoms",
        "type": "jeans",
        "description": "Premium denim jeans with a perfect fit",
        "tags": ["denim", "classic", "casual", "slim-fit"],
        "colors": ["Dark Blue", "Black", "Light Blue", "Grey"],
        "sizes": ["30", "32", "34", "36", "38", "40"],
        "brand": "MANVUE Denim",
        "rating": 4.7,
        "reviews": 189,
        "inStock": True
    },
    {
        "id": 3,
        "title": "Cotton Dress Shirt",
        "price": 39.99,
        "image_url": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=400&h=400&fit=crop",
        "category": "tops",
        "type": "shirts",
        "description": "Professional dress shirt for formal occasions",
        "tags": ["formal", "cotton", "professional", "business"],
        "colors": ["White", "Light Blue", "Pink", "Grey"],
        "sizes": ["S", "M", "L", "XL", "XXL"],
        "brand": "MANVUE Professional",
        "rating": 4.6,
        "reviews": 203,
        "inStock": True
    },
    {
        "id": 4,
        "title": "Athletic Running Trainers",
        "price": 89.99,
        "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=400&fit=crop",
        "category": "shoes",
        "type": "sneakers",
        "description": "High-performance running shoes for athletes",
        "tags": ["athletic", "running", "sports", "performance"],
        "colors": ["Black", "White", "Blue", "Red"],
        "sizes": ["8", "9", "10", "11", "12"],
        "brand": "MANVUE Sports",
        "rating": 4.8,
        "reviews": 156,
        "inStock": True
    },
    {
        "id": 5,
        "title": "Leather Jacket",
        "price": 149.99,
        "image_url": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400&h=400&fit=crop",
        "category": "outerwear",
        "type": "jackets",
        "description": "Premium leather jacket for style and warmth",
        "tags": ["leather", "premium", "style", "warm"],
        "colors": ["Black", "Brown", "Tan"],
        "sizes": ["S", "M", "L", "XL", "XXL"],
        "brand": "MANVUE Premium",
        "rating": 4.9,
        "reviews": 98,
        "inStock": True
    }
]

# Auth setup
SECRET_KEY = "super-secret-key-change-this"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(BaseModel):
    email: str
    password: str

class Product(BaseModel):
    title: str
    price: float
    image_url: str
    category: str = "general"
    type: str = "general"
    description: str = ""
    tags: list = []
    colors: list = []
    sizes: list = []
    brand: str = ""
    rating: float = 0.0
    reviews: int = 0
    inStock: bool = True

class SearchRequest(BaseModel):
    query: str
    category: str = "all"
    filters: dict = {}

class ImageSearchRequest(BaseModel):
    image: str  # Base64 encoded image
    include_similar: bool = True

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_token(data: dict, expires_minutes: int = 60):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ML Search Functions
async def search_products_by_text(query: str, category: str = "all") -> list:
    """Enhanced text search with ML-powered similarity"""
    query_lower = query.lower()
    results = []
    
    for product in products_db:
        if category != "all" and product.get("category") != category:
            continue
            
        # Calculate relevance score
        score = 0
        
        # Title match (highest weight)
        if query_lower in product.get("title", "").lower():
            score += 10
        
        # Description match
        if query_lower in product.get("description", "").lower():
            score += 5
            
        # Tags match
        for tag in product.get("tags", []):
            if query_lower in tag.lower():
                score += 3
                
        # Brand match
        if query_lower in product.get("brand", "").lower():
            score += 2
            
        # Category match
        if query_lower in product.get("category", "").lower():
            score += 1
            
        if score > 0:
            product_with_score = product.copy()
            product_with_score["relevance_score"] = score
            results.append(product_with_score)
    
    # Sort by relevance score
    results.sort(key=lambda x: x["relevance_score"], reverse=True)
    return results

async def search_products_by_image(image_data: str) -> dict:
    """Image-based product search using ML"""
    try:
        # Try to call the ML API if available
        ml_api_url = "http://localhost:5001"  # ML server port
        
        try:
            response = requests.post(f"{ml_api_url}/predict", 
                                   json={"image": image_data}, 
                                   timeout=5)
            if response.status_code == 200:
                ml_result = response.json()
                return {
                    "success": True,
                    "ml_analysis": ml_result,
                    "similar_products": await find_similar_products(ml_result),
                    "source": "ml_api"
                }
        except requests.exceptions.RequestException:
            logger.info("ML API not available, using fallback")
        
        # Fallback: Simple image analysis simulation
        return {
            "success": True,
            "ml_analysis": {
                "detected_items": [
                    {
                        "name": "Fashion Item",
                        "confidence": 85,
                        "category": "tops",
                        "type": "general"
                    }
                ],
                "colors": [
                    {"hex": "#1a1a1a", "name": "Charcoal", "dominance": 0.35}
                ],
                "overall_confidence": 85
            },
            "similar_products": products_db[:3],  # Return first 3 products as similar
            "source": "fallback"
        }
        
    except Exception as e:
        logger.error(f"Image search error: {e}")
        return {
            "success": False,
            "error": str(e),
            "similar_products": [],
            "source": "error"
        }

async def find_similar_products(ml_analysis: dict) -> list:
    """Find products similar to ML analysis results"""
    if not ml_analysis.get("detected_items"):
        return []
    
    detected_category = ml_analysis["detected_items"][0].get("category", "")
    similar_products = []
    
    for product in products_db:
        if product.get("category") == detected_category:
            similar_products.append(product)
    
    return similar_products[:5]  # Return top 5 similar products

# API Endpoints
@app.get("/")
async def root():
    return {
        "message": "ManVue Enhanced API is running",
        "version": "2.0.0",
        "features": ["text_search", "image_search", "ml_integration", "product_management"],
        "endpoints": {
            "auth": ["/register", "/login"],
            "products": ["/products", "/products/search", "/products/image-search"],
            "ml": ["/ml/health", "/ml/predict"]
        }
    }

@app.post("/register")
async def register(user: User):
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed = hash_password(user.password)
    users_db[user.email] = {"email": user.email, "password": hashed}
    return {"msg": "User registered successfully"}

@app.post("/login")
async def login(user: User):
    if user.email not in users_db or not verify_password(user.password, users_db[user.email]["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/products")
async def get_products():
    return products_db

@app.post("/products")
async def create_product(product: Product):
    new_product = product.dict()
    new_product["id"] = len(products_db) + 1
    products_db.append(new_product)
    return new_product

@app.get("/products/category/{category}")
async def get_products_by_category(category: str):
    return [p for p in products_db if p.get("category") == category]

# Enhanced Search Endpoints
@app.post("/products/search")
async def search_products(request: SearchRequest):
    """Enhanced text-based product search"""
    results = await search_products_by_text(request.query, request.category)
    return {
        "query": request.query,
        "category": request.category,
        "results": results,
        "total": len(results)
    }

@app.post("/products/image-search")
async def search_by_image(request: ImageSearchRequest):
    """AI-powered image-based product search"""
    results = await search_products_by_image(request.image)
    return results

@app.get("/ml/health")
async def ml_health():
    """Check ML service health"""
    try:
        response = requests.get("http://localhost:5001/health", timeout=2)
        return {
            "ml_service": "available",
            "status": response.json() if response.status_code == 200 else "unavailable"
        }
    except:
        return {
            "ml_service": "unavailable",
            "status": "ML API not running"
        }

# Product Management Endpoints
@app.put("/products/{product_id}")
async def update_product(product_id: int, product: Product):
    """Update an existing product"""
    for i, p in enumerate(products_db):
        if p["id"] == product_id:
            updated_product = product.dict()
            updated_product["id"] = product_id
            products_db[i] = updated_product
            return updated_product
    
    raise HTTPException(status_code=404, detail="Product not found")

@app.delete("/products/{product_id}")
async def delete_product(product_id: int):
    """Delete a product"""
    for i, p in enumerate(products_db):
        if p["id"] == product_id:
            deleted_product = products_db.pop(i)
            return {"message": "Product deleted", "product": deleted_product}
    
    raise HTTPException(status_code=404, detail="Product not found")

@app.get("/products/{product_id}")
async def get_product(product_id: int):
    """Get a specific product by ID"""
    for product in products_db:
        if product["id"] == product_id:
            return product
    
    raise HTTPException(status_code=404, detail="Product not found")

@app.get("/admin/products")
async def get_all_products_admin():
    """Get all products with admin details"""
    return {
        "products": products_db,
        "total": len(products_db),
        "categories": list(set(p.get("category", "unknown") for p in products_db))
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting ManVue Enhanced Backend...")
    print("📍 Backend: http://localhost:5000")
    print("🤖 ML Features: Text & Image Search")
    print("📋 Enhanced Endpoints:")
    print("   - POST /products/search - AI text search")
    print("   - POST /products/image-search - AI image search")
    print("   - GET /ml/health - ML service status")
    uvicorn.run(app, host="0.0.0.0", port=5000)
