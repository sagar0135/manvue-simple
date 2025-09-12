import motor.motor_asyncio
import motor.motor_gridfs
import os
import io
import base64
from datetime import datetime
from typing import Optional, List, Dict, Any
from bson import ObjectId
from dotenv import load_dotenv
import logging

load_dotenv()

# Configuration
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "manvue_db")

# MongoDB client and database
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]

# GridFS for image storage
gridfs = motor.motor_gridfs.AsyncIOMotorGridFS(db)

# Collections
users_collection = db.users
products_collection = db.products
orders_collection = db.orders
images_collection = db.images
product_embeddings_collection = db.product_embeddings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database connection test
async def test_connection():
    """Test MongoDB connection"""
    try:
        await client.admin.command('ping')
        logger.info(f"Connected to MongoDB: {DB_NAME}")
        return True
    except Exception as e:
        logger.error(f"MongoDB connection failed: {e}")
        return False

# Image storage functions
async def store_image(image_data: bytes, filename: str, content_type: str = "image/jpeg", metadata: Dict = None) -> str:
    """
    Store image in GridFS and return the file ID
    
    Args:
        image_data: Raw image bytes
        filename: Original filename
        content_type: MIME type of the image
        metadata: Additional metadata to store
    
    Returns:
        str: GridFS file ID
    """
    try:
        file_metadata = {
            "filename": filename,
            "content_type": content_type,
            "upload_date": datetime.utcnow(),
            **(metadata or {})
        }
        
        file_id = await gridfs.upload_from_stream(
            filename,
            io.BytesIO(image_data),
            metadata=file_metadata
        )
        
        logger.info(f"Image stored with ID: {file_id}")
        return str(file_id)
    
    except Exception as e:
        logger.error(f"Error storing image: {e}")
        raise

async def store_image_base64(base64_data: str, filename: str, content_type: str = "image/jpeg", metadata: Dict = None) -> str:
    """
    Store base64 encoded image in GridFS
    
    Args:
        base64_data: Base64 encoded image data (with or without data URL prefix)
        filename: Original filename
        content_type: MIME type of the image
        metadata: Additional metadata to store
    
    Returns:
        str: GridFS file ID
    """
    try:
        # Remove data URL prefix if present
        if base64_data.startswith('data:'):
            base64_data = base64_data.split(',')[1]
        
        # Decode base64 to bytes
        image_bytes = base64.b64decode(base64_data)
        
        return await store_image(image_bytes, filename, content_type, metadata)
    
    except Exception as e:
        logger.error(f"Error storing base64 image: {e}")
        raise

async def get_image(file_id: str) -> Optional[bytes]:
    """
    Retrieve image data from GridFS
    
    Args:
        file_id: GridFS file ID
    
    Returns:
        bytes: Image data or None if not found
    """
    try:
        grid_out = await gridfs.open_download_stream(ObjectId(file_id))
        image_data = await grid_out.read()
        return image_data
    
    except Exception as e:
        logger.error(f"Error retrieving image {file_id}: {e}")
        return None

async def get_image_metadata(file_id: str) -> Optional[Dict]:
    """
    Get image metadata from GridFS
    
    Args:
        file_id: GridFS file ID
    
    Returns:
        dict: Image metadata or None if not found
    """
    try:
        grid_out = await gridfs.open_download_stream(ObjectId(file_id))
        return {
            "filename": grid_out.filename,
            "content_type": grid_out.metadata.get("content_type", "image/jpeg"),
            "upload_date": grid_out.upload_date,
            "length": grid_out.length,
            **grid_out.metadata
        }
    
    except Exception as e:
        logger.error(f"Error retrieving image metadata {file_id}: {e}")
        return None

async def delete_image(file_id: str) -> bool:
    """
    Delete image from GridFS
    
    Args:
        file_id: GridFS file ID
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        await gridfs.delete(ObjectId(file_id))
        logger.info(f"Image {file_id} deleted successfully")
        return True
    
    except Exception as e:
        logger.error(f"Error deleting image {file_id}: {e}")
        return False

async def list_images(limit: int = 50, skip: int = 0) -> List[Dict]:
    """
    List all images in GridFS
    
    Args:
        limit: Maximum number of images to return
        skip: Number of images to skip
    
    Returns:
        List[Dict]: List of image metadata
    """
    try:
        cursor = gridfs.find().skip(skip).limit(limit)
        images = []
        
        async for grid_out in cursor:
            images.append({
                "id": str(grid_out._id),
                "filename": grid_out.filename,
                "content_type": grid_out.metadata.get("content_type", "image/jpeg"),
                "upload_date": grid_out.upload_date,
                "length": grid_out.length,
                **grid_out.metadata
            })
        
        return images
    
    except Exception as e:
        logger.error(f"Error listing images: {e}")
        return []

# Product database functions
async def create_product(product_data: Dict) -> str:
    """Create a new product"""
    try:
        product_data["created_at"] = datetime.utcnow()
        product_data["updated_at"] = datetime.utcnow()
        
        result = await products_collection.insert_one(product_data)
        logger.info(f"Product created with ID: {result.inserted_id}")
        return str(result.inserted_id)
    
    except Exception as e:
        logger.error(f"Error creating product: {e}")
        raise

async def get_product(product_id: str) -> Optional[Dict]:
    """Get product by ID"""
    try:
        if ObjectId.is_valid(product_id):
            product = await products_collection.find_one({"_id": ObjectId(product_id)})
        else:
            # Try to find by numeric ID for backward compatibility
            product = await products_collection.find_one({"id": int(product_id)})
        
        if product:
            product["_id"] = str(product["_id"])
        
        return product
    
    except Exception as e:
        logger.error(f"Error getting product {product_id}: {e}")
        return None

async def get_products(category: str = None, limit: int = 50, skip: int = 0) -> List[Dict]:
    """Get products with optional filtering"""
    try:
        filter_query = {}
        if category:
            filter_query["category"] = category
        
        cursor = products_collection.find(filter_query).skip(skip).limit(limit)
        products = []
        
        async for product in cursor:
            product["_id"] = str(product["_id"])
            products.append(product)
        
        return products
    
    except Exception as e:
        logger.error(f"Error getting products: {e}")
        return []

async def update_product(product_id: str, update_data: Dict) -> bool:
    """Update product"""
    try:
        update_data["updated_at"] = datetime.utcnow()
        
        if ObjectId.is_valid(product_id):
            result = await products_collection.update_one(
                {"_id": ObjectId(product_id)},
                {"$set": update_data}
            )
        else:
            result = await products_collection.update_one(
                {"id": int(product_id)},
                {"$set": update_data}
            )
        
        return result.modified_count > 0
    
    except Exception as e:
        logger.error(f"Error updating product {product_id}: {e}")
        return False

async def delete_product(product_id: str) -> bool:
    """Delete product"""
    try:
        if ObjectId.is_valid(product_id):
            result = await products_collection.delete_one({"_id": ObjectId(product_id)})
        else:
            result = await products_collection.delete_one({"id": int(product_id)})
        
        return result.deleted_count > 0
    
    except Exception as e:
        logger.error(f"Error deleting product {product_id}: {e}")
        return False

# User database functions
async def create_user(user_data: Dict) -> str:
    """Create a new user"""
    try:
        user_data["created_at"] = datetime.utcnow()
        user_data["updated_at"] = datetime.utcnow()
        
        result = await users_collection.insert_one(user_data)
        logger.info(f"User created with ID: {result.inserted_id}")
        return str(result.inserted_id)
    
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        raise

async def get_user_by_email(email: str) -> Optional[Dict]:
    """Get user by email"""
    try:
        user = await users_collection.find_one({"email": email})
        if user:
            user["_id"] = str(user["_id"])
        return user
    
    except Exception as e:
        logger.error(f"Error getting user by email {email}: {e}")
        return None

async def update_user(user_id: str, update_data: Dict) -> bool:
    """Update user"""
    try:
        update_data["updated_at"] = datetime.utcnow()
        
        result = await users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )
        
        return result.modified_count > 0
    
    except Exception as e:
        logger.error(f"Error updating user {user_id}: {e}")
        return False

# Product embedding functions
async def store_product_embedding(product_id: str, embedding: List[float], model_version: str = "clip-vit-base-patch32") -> bool:
    """
    Store product embedding for similarity search
    
    Args:
        product_id: Product ID
        embedding: CLIP embedding vector
        model_version: Version of the model used
    
    Returns:
        bool: True if successful
    """
    try:
        embedding_data = {
            "product_id": product_id,
            "embedding": embedding,
            "model_version": model_version,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        # Upsert embedding (update if exists, insert if not)
        await product_embeddings_collection.update_one(
            {"product_id": product_id, "model_version": model_version},
            {"$set": embedding_data},
            upsert=True
        )
        
        logger.info(f"Product embedding stored for product {product_id}")
        return True
    
    except Exception as e:
        logger.error(f"Error storing product embedding for {product_id}: {e}")
        return False

async def get_product_embedding(product_id: str, model_version: str = "clip-vit-base-patch32") -> Optional[List[float]]:
    """
    Get product embedding
    
    Args:
        product_id: Product ID
        model_version: Version of the model
    
    Returns:
        List[float]: Embedding vector or None
    """
    try:
        embedding_doc = await product_embeddings_collection.find_one({
            "product_id": product_id,
            "model_version": model_version
        })
        
        if embedding_doc:
            return embedding_doc["embedding"]
        
        return None
    
    except Exception as e:
        logger.error(f"Error getting product embedding for {product_id}: {e}")
        return None

async def get_all_product_embeddings(model_version: str = "clip-vit-base-patch32") -> Dict[str, List[float]]:
    """
    Get all product embeddings
    
    Args:
        model_version: Version of the model
    
    Returns:
        Dict[str, List[float]]: Dict of product_id -> embedding
    """
    try:
        cursor = product_embeddings_collection.find({"model_version": model_version})
        embeddings = {}
        
        async for doc in cursor:
            embeddings[doc["product_id"]] = doc["embedding"]
        
        return embeddings
    
    except Exception as e:
        logger.error(f"Error getting all product embeddings: {e}")
        return {}

async def delete_product_embedding(product_id: str, model_version: str = "clip-vit-base-patch32") -> bool:
    """
    Delete product embedding
    
    Args:
        product_id: Product ID
        model_version: Version of the model
    
    Returns:
        bool: True if successful
    """
    try:
        result = await product_embeddings_collection.delete_one({
            "product_id": product_id,
            "model_version": model_version
        })
        
        return result.deleted_count > 0
    
    except Exception as e:
        logger.error(f"Error deleting product embedding for {product_id}: {e}")
        return False