from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
from datetime import datetime, timedelta
from passlib.context import CryptContext
import jwt

app = FastAPI()

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
        "title": "Casual Shirt",
        "price": 29.99,
        "image_url": "https://via.placeholder.com/150",
        "category": "shirts"
    },
    {
        "id": 2,
        "title": "Denim Jeans",
        "price": 49.99,
        "image_url": "https://via.placeholder.com/150",
        "category": "bottoms"
    },
    {
        "id": 3,
        "title": "Cotton T-Shirt",
        "price": 19.99,
        "image_url": "https://via.placeholder.com/150",
        "category": "tshirts"
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

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_token(data: dict, expires_minutes: int = 60):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@app.get("/")
async def root():
    return {"message": "ManVue API is running"}

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
