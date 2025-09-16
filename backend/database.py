"""
Database connection and operations for Fashion Recommender
MongoDB integration with GridFS for image storage
"""

import os
import logging
from typing import List, Dict, Any, Optional
from pymongo import MongoClient
from gridfs import GridFS
from bson import ObjectId
import numpy as np
from datetime import datetime

logger = logging.getLogger(__name__)

class DatabaseManager:
    """MongoDB database manager for fashion recommender"""
    
    def __init__(self, connection_string: str = None, database_name: str = "fashion_recommender"):
        self.connection_string = connection_string or os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
        self.database_name = database_name
        self.client = None
        self.db = None
        self.fs = None
        self._connect()
    
    def _connect(self):
        """Establish database connection"""
        try:
            self.client = MongoClient(self.connection_string)
            self.db = self.client[self.database_name]
            self.fs = GridFS(self.db)
            
            # Test connection
            self.client.admin.command('ping')
            logger.info("✅ Connected to MongoDB successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to connect to MongoDB: {e}")
            raise
    
    def get_collection(self, collection_name: str):
        """Get a collection from the database"""
        return self.db[collection_name]
    
    def save_image(self, image_data: bytes, filename: str, metadata: Dict[str, Any] = None) -> str:
        """Save image to GridFS and return file ID"""
        try:
            file_id = self.fs.put(
                image_data,
                filename=filename,
                metadata=metadata or {}
            )
            logger.info(f"✅ Image saved with ID: {file_id}")
            return str(file_id)
        except Exception as e:
            logger.error(f"❌ Error saving image: {e}")
            raise
    
    def get_image(self, file_id: str) -> bytes:
        """Retrieve image from GridFS"""
        try:
            file_id = ObjectId(file_id)
            image_data = self.fs.get(file_id).read()
            return image_data
        except Exception as e:
            logger.error(f"❌ Error retrieving image: {e}")
            raise
    
    def delete_image(self, file_id: str) -> bool:
        """Delete image from GridFS"""
        try:
            file_id = ObjectId(file_id)
            self.fs.delete(file_id)
            logger.info(f"✅ Image deleted: {file_id}")
            return True
        except Exception as e:
            logger.error(f"❌ Error deleting image: {e}")
            return False
    
    def save_product(self, product_data: Dict[str, Any]) -> str:
        """Save product to database"""
        try:
            products_collection = self.get_collection('products')
            product_data['created_at'] = datetime.now()
            product_data['updated_at'] = datetime.now()
            
            result = products_collection.insert_one(product_data)
            product_id = str(result.inserted_id)
            logger.info(f"✅ Product saved with ID: {product_id}")
            return product_id
        except Exception as e:
            logger.error(f"❌ Error saving product: {e}")
            raise
    
    def get_product(self, product_id: str) -> Optional[Dict[str, Any]]:
        """Get product by ID"""
        try:
            products_collection = self.get_collection('products')
            product = products_collection.find_one({"_id": ObjectId(product_id)})
            if product:
                product['_id'] = str(product['_id'])
            return product
        except Exception as e:
            logger.error(f"❌ Error getting product: {e}")
            return None
    
    def search_products(self, query: Dict[str, Any], limit: int = 10) -> List[Dict[str, Any]]:
        """Search products with query"""
        try:
            products_collection = self.get_collection('products')
            products = list(products_collection.find(query).limit(limit))
            
            # Convert ObjectId to string
            for product in products:
                product['_id'] = str(product['_id'])
            
            return products
        except Exception as e:
            logger.error(f"❌ Error searching products: {e}")
            return []
    
    def find_similar_items(self, image_features: np.ndarray, limit: int = 10) -> List[Dict[str, Any]]:
        """Find similar items based on image features"""
        try:
            products_collection = self.get_collection('products')
            
            # For now, return random products (implement proper similarity search)
            # In production, you would use vector similarity search
            similar_products = list(products_collection.aggregate([
                {"$sample": {"size": limit}}
            ]))
            
            # Convert ObjectId to string
            for product in similar_products:
                product['_id'] = str(product['_id'])
            
            return similar_products
        except Exception as e:
            logger.error(f"❌ Error finding similar items: {e}")
            return []
    
    def save_user_preferences(self, user_id: str, preferences: Dict[str, Any]) -> bool:
        """Save user preferences"""
        try:
            users_collection = self.get_collection('users')
            users_collection.update_one(
                {"user_id": user_id},
                {
                    "$set": {
                        "preferences": preferences,
                        "updated_at": datetime.now()
                    }
                },
                upsert=True
            )
            logger.info(f"✅ User preferences saved for user: {user_id}")
            return True
        except Exception as e:
            logger.error(f"❌ Error saving user preferences: {e}")
            return False
    
    def get_user_preferences(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user preferences"""
        try:
            users_collection = self.get_collection('users')
            user = users_collection.find_one({"user_id": user_id})
            return user.get('preferences') if user else None
        except Exception as e:
            logger.error(f"❌ Error getting user preferences: {e}")
            return None
    
    def save_recommendation_history(self, user_id: str, recommendations: List[Dict[str, Any]]) -> bool:
        """Save recommendation history"""
        try:
            recommendations_collection = self.get_collection('recommendations')
            recommendation_data = {
                "user_id": user_id,
                "recommendations": recommendations,
                "created_at": datetime.now()
            }
            recommendations_collection.insert_one(recommendation_data)
            logger.info(f"✅ Recommendation history saved for user: {user_id}")
            return True
        except Exception as e:
            logger.error(f"❌ Error saving recommendation history: {e}")
            return False
    
    def get_recommendation_history(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get user's recommendation history"""
        try:
            recommendations_collection = self.get_collection('recommendations')
            history = list(recommendations_collection.find(
                {"user_id": user_id}
            ).sort("created_at", -1).limit(limit))
            
            # Convert ObjectId to string
            for item in history:
                item['_id'] = str(item['_id'])
            
            return history
        except Exception as e:
            logger.error(f"❌ Error getting recommendation history: {e}")
            return []
    
    def close(self):
        """Close database connection"""
        if self.client:
            self.client.close()
            logger.info("✅ Database connection closed")

# Global database instance
_db_instance = None

def get_database_connection() -> DatabaseManager:
    """Get database connection instance"""
    global _db_instance
    if _db_instance is None:
        _db_instance = DatabaseManager()
    return _db_instance

def test_connection() -> bool:
    """Test database connection"""
    try:
        db = get_database_connection()
        db.client.admin.command('ping')
        return True
    except Exception as e:
        logger.error(f"Database connection test failed: {e}")
        return False
