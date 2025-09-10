from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import db
from auth import hash_password, verify_password, create_token
from products import get_products, add_product

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class User(BaseModel):
    email: str
    password: str

class Product(BaseModel):
    title: str
    price: float
    image_url: str

@app.post("/register")
async def register(user: User):
    existing = await db.users.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = hash_password(user.password)
    await db.users.insert_one({"email": user.email, "password": hashed})
    return {"msg": "User registered"}

@app.post("/login")
async def login(user: User):
    db_user = await db.users.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/products")
async def fetch_products():
    return await get_products()

@app.post("/products")
async def create_product(product: Product):
    return await add_product(product.dict())