from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from backend.database import db
from backend.auth import hash_password, verify_password, create_token, decode_token

app = FastAPI()

class User(BaseModel):
    email: str
    password: str
    name: str | None = None

@app.post("/register")
async def register(user: User):
    existing = await db.users.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = hash_password(user.password)
    await db.users.insert_one({"email": user.email, "password": hashed, "name": user.name})
    return {"msg": "User registered successfully"}

@app.post("/login")
async def login(user: User):
    db_user = await db.users.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/products")
async def get_products():
    products = await db.products.find().to_list(100)
    return products
