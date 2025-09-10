from database import db

async def get_products(limit: int = 20):
    return await db.products.find().limit(limit).to_list(limit)

async def add_product(product: dict):
    await db.products.insert_one(product)
    return product
