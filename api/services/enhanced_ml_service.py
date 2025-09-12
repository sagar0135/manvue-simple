"""
Enhanced ML Service
Integrates CLIP + FAISS + MongoDB from collab system
"""

import logging
import os
import json
import numpy as np
import faiss
import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
from typing import List, Dict, Any, Optional, Tuple
from pymongo import MongoClient
import gridfs
from datetime import datetime
import io

logger = logging.getLogger(__name__)

class EnhancedMLService:
    """Enhanced ML service integrating collab system functionality"""
    
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.clip_model = None
        self.clip_processor = None
        self.faiss_index = None
        self.metadata = []
        self.mongo_client = None
        self.db = None
        self.fs = None
        
        # Initialize components
        self._initialize_clip()
        self._initialize_mongodb()
        self._load_faiss_index()
    
    def _initialize_clip(self):
        """Initialize CLIP model"""
        try:
            clip_model_name = "openai/clip-vit-base-patch32"
            self.clip_model = CLIPModel.from_pretrained(clip_model_name).to(self.device)
            self.clip_processor = CLIPProcessor.from_pretrained(clip_model_name)
            logger.info(f"✅ CLIP model loaded on {self.device}")
        except Exception as e:
            logger.error(f"❌ Failed to load CLIP model: {e}")
            self.clip_model = None
            self.clip_processor = None
    
    def _initialize_mongodb(self):
        """Initialize MongoDB connection"""
        try:
            mongo_uri = "mongodb+srv://19276146:19276146@manvue.ilich4r.mongodb.net/?retryWrites=true&w=majority&appName=MANVUE"
            self.mongo_client = MongoClient(mongo_uri)
            self.db = self.mongo_client["MANVUE"]
            self.fs = gridfs.GridFS(self.db)
            logger.info("✅ Connected to MongoDB MANVUE")
        except Exception as e:
            logger.error(f"❌ Failed to connect to MongoDB: {e}")
    
    def _load_faiss_index(self):
        """Load FAISS index and metadata"""
        try:
            # Try to load from file first
            if os.path.exists("fashion.index"):
                self.faiss_index = faiss.read_index("fashion.index")
                logger.info("✅ FAISS index loaded from file")
            else:
                logger.warning("⚠️ FAISS index file not found, creating new index")
                self.faiss_index = None
            
            # Load metadata
            if os.path.exists("metadata.json"):
                with open("metadata.json", "r") as f:
                    self.metadata = json.load(f)
                logger.info(f"✅ Metadata loaded: {len(self.metadata)} items")
            else:
                logger.warning("⚠️ Metadata file not found")
                self.metadata = []
                
        except Exception as e:
            logger.error(f"❌ Failed to load FAISS index/metadata: {e}")
    
    def is_available(self) -> bool:
        """Check if ML service is available"""
        return (
            self.clip_model is not None and 
            self.clip_processor is not None and
            self.faiss_index is not None and
            len(self.metadata) > 0
        )
    
    def image_to_embedding(self, image: Image.Image) -> Optional[np.ndarray]:
        """Convert PIL image to CLIP embedding"""
        if not self.clip_model or not self.clip_processor:
            return None
        
        try:
            inputs = self.clip_processor(images=[image], return_tensors="pt").to(self.device)
            with torch.no_grad():
                feats = self.clip_model.get_image_features(**inputs)
            feats = feats / feats.norm(p=2, dim=-1, keepdim=True)
            return feats.cpu().numpy()[0].astype("float32")
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            return None
    
    def find_similar_products(
        self, 
        image: Image.Image, 
        top_k: int = 6
    ) -> List[Dict[str, Any]]:
        """Find similar products using FAISS search"""
        if not self.is_available():
            logger.error("ML service not fully available")
            return []
        
        try:
            # Get image embedding
            emb = self.image_to_embedding(image)
            if emb is None:
                return []
            
            # Search FAISS index
            emb = emb.reshape(1, -1)
            D, I = self.faiss_index.search(emb, top_k)
            
            # Get results with metadata
            results = []
            for i, idx in enumerate(I[0]):
                if idx < len(self.metadata):
                    result = self.metadata[idx].copy()
                    result['similarity_score'] = float(D[0][i])
                    result['confidence'] = min(int((1 - D[0][i]) * 100), 100)
                    results.append(result)
            
            return results
            
        except Exception as e:
            logger.error(f"Error in similarity search: {e}")
            return []
    
    def upload_user_image_and_search(
        self, 
        image: Image.Image, 
        username: str = "guest", 
        top_k: int = 6
    ) -> Dict[str, Any]:
        """Upload user image and find similar products (like collab function)"""
        try:
            # Save image to MongoDB GridFS
            buf = io.BytesIO()
            image.save(buf, format="JPEG")
            buf.seek(0)
            
            upload_name = f"user_{username}_{int(datetime.now().timestamp())}.jpg"
            file_id = self.fs.put(
                buf.read(),
                filename=upload_name,
                metadata={
                    "username": username,
                    "uploadedAt": datetime.utcnow(),
                    "search_type": "visual_search"
                }
            )
            
            # Find similar products
            similar_products = self.find_similar_products(image, top_k)
            
            # Save query log
            query_doc = {
                "username": username,
                "uploaded_file_id": str(file_id),
                "uploaded_filename": upload_name,
                "results": similar_products,
                "createdAt": datetime.utcnow(),
                "total_results": len(similar_products)
            }
            
            self.db["queries"].insert_one(query_doc)
            
            return {
                "success": True,
                "file_id": str(file_id),
                "similar_products": similar_products,
                "total_found": len(similar_products)
            }
            
        except Exception as e:
            logger.error(f"Error in upload and search: {e}")
            return {
                "success": False,
                "error": str(e),
                "similar_products": []
            }
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about loaded models and data"""
        return {
            "clip_available": self.clip_model is not None,
            "faiss_index_available": self.faiss_index is not None,
            "faiss_index_size": self.faiss_index.ntotal if self.faiss_index else 0,
            "metadata_count": len(self.metadata),
            "device": self.device,
            "mongodb_connected": self.mongo_client is not None
        }

