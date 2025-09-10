#!/usr/bin/env python3
"""
Simple MANVUE Backend Server for Development
Works without MongoDB - uses in-memory storage
"""

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import hashlib
import secrets

# Create FastAPI app
app = FastAPI(
    title="MANVUE Simple API",
    description="Simple backend for MANVUE development",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage (for development only)
users_db = {}
products_db = []
orders_db = []

# Sample products data
SAMPLE_PRODUCTS = [
    {
        "id": 1,
        "name": "Classic White T-Shirt",
        "price": 24.99,
        "originalPrice": 32.99,
        "category": "men",
        "type": "tops",
        "size": ["S", "M", "L", "XL", "XXL"],
        "color": ["White", "Black", "Navy", "Grey"],
        "brand": "MANVUE Basics",
        "rating": 4.5,
        "reviews": 127,
        "image": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop",
        "tags": ["casual", "cotton", "basic", "everyday", "comfortable"],
        "inStock": True,
        "description": "Comfortable cotton t-shirt perfect for everyday wear. Made from 100% organic cotton with a relaxed fit."
    },
    {
        "id": 2,
        "name": "Premium Denim Jeans",
        "price": 64.99,
        "originalPrice": 74.99,
        "category": "men",
        "type": "bottoms",
        "size": ["30", "32", "34", "36", "38", "40"],
        "color": ["Dark Blue", "Black", "Light Blue", "Grey"],
        "brand": "MANVUE Denim",
        "rating": 4.7,
        "reviews": 189,
        "image": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=400&h=400&fit=crop",
        "tags": ["denim", "classic", "casual", "slim-fit", "premium"],
        "inStock": True,
        "description": "Premium denim jeans with a perfect fit. Slim cut with stretch comfort and reinforced stitching."
    },
    {
        "id": 3,
        "name": "Athletic Running Trainers",
        "price": 104.99,
        "originalPrice": 124.99,
        "category": "men",
        "type": "shoes",
        "size": ["7", "8", "9", "10", "11", "12"],
        "color": ["White", "Black", "Grey", "Navy"],
        "brand": "SportMax",
        "rating": 4.8,
        "reviews": 334,
        "image": "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400&h=400&fit=crop",
        "tags": ["sports", "running", "comfort", "breathable", "athletic"],
        "inStock": True,
        "description": "High-performance running trainers with breathable mesh upper and responsive cushioning."
    },
    {
        "id": 4,
        "name": "Business Formal Shirt",
        "price": 44.99,
        "originalPrice": 54.99,
        "category": "men",
        "type": "tops",
        "size": ["S", "M", "L", "XL", "XXL"],
        "color": ["White", "Light Blue", "Navy", "Pink"],
        "brand": "MANVUE Professional",
        "rating": 4.6,
        "reviews": 256,
        "image": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=400&fit=crop",
        "tags": ["formal", "business", "professional", "cotton", "crisp"],
        "inStock": True,
        "description": "Professional dress shirt perfect for business meetings. Non-iron cotton with modern fit."
    },
    {
        "id": 5,
        "name": "Leather Wallet",
        "price": 34.99,
        "originalPrice": 44.99,
        "category": "men",
        "type": "accessories",
        "size": ["One Size"],
        "color": ["Brown", "Black", "Tan", "Navy"],
        "brand": "LuxeLeather",
        "rating": 4.9,
        "reviews": 89,
        "image": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400&h=400&fit=crop",
        "tags": ["leather", "wallet", "premium", "classic", "durable"],
        "inStock": True,
        "description": "Premium leather wallet with multiple card slots and cash compartment. Handcrafted from genuine leather."
    }
]

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
    id: int
    name: str
    price: float
    originalPrice: float
    category: str
    type: str
    size: List[str]
    color: List[str]
    brand: str
    rating: float
    reviews: int
    image: str
    tags: List[str]
    inStock: bool
    description: str

# Utility functions
def hash_password(password: str) -> str:
    """Simple password hashing for development"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password for development"""
    return hash_password(plain_password) == hashed_password

def create_token(user_email: str) -> str:
    """Create a simple token for development"""
    payload = {
        "sub": user_email,
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    # Simple token generation (not secure for production)
    return secrets.token_urlsafe(32)

# API Endpoints
@app.get("/")
async def root():
    return {"message": "MANVUE Simple API Server", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "users_count": len(users_db),
        "products_count": len(products_db)
    }

@app.post("/register", response_model=UserResponse)
async def register(user: User):
    """Register a new user"""
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_id = secrets.token_urlsafe(16)
    hashed_password = hash_password(user.password)
    
    user_data = {
        "id": user_id,
        "email": user.email,
        "password": hashed_password,
        "name": user.name,
        "created_at": datetime.now().isoformat()
    }
    
    users_db[user.email] = user_data
    
    return UserResponse(
        id=user_id,
        email=user.email,
        name=user.name,
        created_at=user_data["created_at"]
    )

@app.post("/login", response_model=LoginResponse)
async def login(user: User):
    """Login user"""
    if user.email not in users_db:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    stored_user = users_db[user.email]
    if not verify_password(user.password, stored_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_token(user.email)
    
    return LoginResponse(
        access_token=token,
        token_type="bearer",
        user=UserResponse(
            id=stored_user["id"],
            email=stored_user["email"],
            name=stored_user["name"],
            created_at=stored_user["created_at"]
        )
    )

@app.get("/products", response_model=List[Product])
async def get_products():
    """Get all products"""
    return products_db

@app.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: int):
    """Get a specific product"""
    product = next((p for p in products_db if p["id"] == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/products", response_model=Product)
async def create_product(product: Product):
    """Create a new product (admin only)"""
    # In a real app, you'd check for admin permissions
    products_db.append(product.dict())
    return product

# Initialize sample data
@app.on_event("startup")
async def startup_event():
    """Initialize sample data on startup"""
    global products_db
    products_db = SAMPLE_PRODUCTS.copy()
    print(f"MANVUE Simple API Server started with {len(products_db)} products")

if __name__ == "__main__":
    # Start server
    port = int(os.environ.get("PORT", 5000))
    uvicorn.run(
        "simple_server:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )
