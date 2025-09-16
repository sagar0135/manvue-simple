#!/usr/bin/env python3
"""
ManVue Authentication and Payment API
Handles user authentication, registration, and payment processing
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional, List
import hashlib
import uuid
from datetime import datetime, timedelta
import jwt
import pymongo
from pymongo import MongoClient
import stripe
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="ManVue Auth & Payment API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection
MONGO_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client.manvue_db

# Collections
users_collection = db.users
orders_collection = db.orders
payments_collection = db.payments

# Stripe configuration
stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_your_stripe_secret_key")

# JWT configuration
JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24

# Pydantic models
class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    phone: Optional[str] = None
    created_at: str

class PaymentRequest(BaseModel):
    cardNumber: str
    expiry: str
    cvv: str
    cardholderName: str
    amount: float
    items: List[dict]

class OrderResponse(BaseModel):
    orderId: str
    status: str
    total: float
    items: List[dict]
    created_at: str

# Utility functions
def hash_password(password: str) -> str:
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash"""
    return hash_password(password) == hashed

def create_jwt_token(user_id: str) -> str:
    """Create JWT token for user"""
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def verify_jwt_token(token: str) -> Optional[str]:
    """Verify JWT token and return user ID"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload.get("user_id")
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def get_current_user(authorization: str = None) -> Optional[dict]:
    """Get current user from JWT token"""
    if not authorization or not authorization.startswith("Bearer "):
        return None
    
    token = authorization.split(" ")[1]
    user_id = verify_jwt_token(token)
    
    if not user_id:
        return None
    
    user = users_collection.find_one({"_id": user_id})
    return user

# API Routes

@app.post("/api/auth/register", response_model=UserResponse)
async def register_user(user_data: UserRegister):
    """Register a new user"""
    
    # Check if user already exists
    existing_user = users_collection.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    # Create new user
    user_id = str(uuid.uuid4())
    hashed_password = hash_password(user_data.password)
    
    user_doc = {
        "_id": user_id,
        "name": user_data.name,
        "email": user_data.email,
        "password": hashed_password,
        "phone": user_data.phone,
        "created_at": datetime.utcnow().isoformat(),
        "is_active": True
    }
    
    try:
        users_collection.insert_one(user_doc)
        
        # Create JWT token
        token = create_jwt_token(user_id)
        
        return UserResponse(
            id=user_id,
            name=user_data.name,
            email=user_data.email,
            phone=user_data.phone,
            created_at=user_doc["created_at"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

@app.post("/api/auth/login")
async def login_user(login_data: UserLogin):
    """Login user and return JWT token"""
    
    # Find user by email
    user = users_collection.find_one({"email": login_data.email})
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Verify password
    if not verify_password(login_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Check if user is active
    if not user.get("is_active", True):
        raise HTTPException(status_code=401, detail="Account is deactivated")
    
    # Create JWT token
    token = create_jwt_token(user["_id"])
    
    return {
        "token": token,
        "user": UserResponse(
            id=user["_id"],
            name=user["name"],
            email=user["email"],
            phone=user.get("phone"),
            created_at=user["created_at"]
        )
    }

@app.get("/api/auth/me")
async def get_current_user_info(authorization: str = None):
    """Get current user information"""
    user = get_current_user(authorization)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    return UserResponse(
        id=user["_id"],
        name=user["name"],
        email=user["email"],
        phone=user.get("phone"),
        created_at=user["created_at"]
    )

@app.post("/api/payment/process", response_model=OrderResponse)
async def process_payment(payment_data: PaymentRequest, authorization: str = None):
    """Process payment and create order"""
    
    # Verify user authentication
    user = get_current_user(authorization)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    try:
        # Create Stripe payment intent
        intent = stripe.PaymentIntent.create(
            amount=int(payment_data.amount * 100),  # Convert to cents
            currency='gbp',
            metadata={
                'user_id': user["_id"],
                'user_email': user["email"]
            }
        )
        
        # Create order
        order_id = str(uuid.uuid4())
        order_doc = {
            "_id": order_id,
            "user_id": user["_id"],
            "user_email": user["email"],
            "items": payment_data.items,
            "total": payment_data.amount,
            "status": "pending",
            "payment_intent_id": intent.id,
            "created_at": datetime.utcnow().isoformat(),
            "shipping_address": None,
            "billing_address": None
        }
        
        orders_collection.insert_one(order_doc)
        
        # Create payment record
        payment_doc = {
            "_id": str(uuid.uuid4()),
            "order_id": order_id,
            "user_id": user["_id"],
            "amount": payment_data.amount,
            "currency": "gbp",
            "payment_intent_id": intent.id,
            "status": "pending",
            "card_last_four": payment_data.cardNumber[-4:],
            "created_at": datetime.utcnow().isoformat()
        }
        
        payments_collection.insert_one(payment_doc)
        
        return OrderResponse(
            orderId=order_id,
            status="pending",
            total=payment_data.amount,
            items=payment_data.items,
            created_at=order_doc["created_at"]
        )
        
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=f"Payment failed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Order creation failed: {str(e)}")

@app.get("/api/orders")
async def get_user_orders(authorization: str = None):
    """Get user's orders"""
    user = get_current_user(authorization)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    orders = list(orders_collection.find(
        {"user_id": user["_id"]},
        {"_id": 1, "items": 1, "total": 1, "status": 1, "created_at": 1}
    ).sort("created_at", -1))
    
    return {"orders": orders}

@app.get("/api/orders/{order_id}")
async def get_order_details(order_id: str, authorization: str = None):
    """Get specific order details"""
    user = get_current_user(authorization)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    order = orders_collection.find_one({
        "_id": order_id,
        "user_id": user["_id"]
    })
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return order

@app.post("/api/payment/confirm/{payment_intent_id}")
async def confirm_payment(payment_intent_id: str, authorization: str = None):
    """Confirm payment completion"""
    user = get_current_user(authorization)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    try:
        # Retrieve payment intent from Stripe
        intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        
        if intent.status == "succeeded":
            # Update order status
            orders_collection.update_one(
                {"payment_intent_id": payment_intent_id},
                {"$set": {"status": "paid", "updated_at": datetime.utcnow().isoformat()}}
            )
            
            # Update payment status
            payments_collection.update_one(
                {"payment_intent_id": payment_intent_id},
                {"$set": {"status": "completed", "updated_at": datetime.utcnow().isoformat()}}
            )
            
            return {"status": "success", "message": "Payment confirmed"}
        else:
            return {"status": "pending", "message": "Payment still processing"}
            
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=f"Payment confirmation failed: {str(e)}")

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "database": "connected" if client.admin.command('ping') else "disconnected"
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting ManVue Auth & Payment API...")
    print("📱 API: http://localhost:8001")
    print("📚 Docs: http://localhost:8001/docs")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001,
        log_level="info"
    )
