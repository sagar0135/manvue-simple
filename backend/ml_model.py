import torch
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Device configuration
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
logger.info(f"Using device: {DEVICE}")

# Initialize CLIP model and processor
try:
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(DEVICE)
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    logger.info("CLIP model loaded successfully")
except Exception as e:
    logger.error(f"Failed to load CLIP model: {e}")
    model = None
    processor = None

def get_image_embedding(image_path: str):
    """
    Generate CLIP embedding for an image
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        list: Image embedding as a list of floats
    """
    if model is None or processor is None:
        raise RuntimeError("CLIP model not loaded")
    
    try:
        # Load and preprocess image
        image = Image.open(image_path).convert("RGB")
        inputs = processor(images=image, return_tensors="pt").to(DEVICE)
        
        # Generate embedding
        with torch.no_grad():
            emb = model.get_image_features(**inputs)
        
        return emb.cpu().numpy().tolist()[0]
    
    except Exception as e:
        logger.error(f"Error generating image embedding: {e}")
        raise

def get_text_embedding(query: str):
    """
    Generate CLIP embedding for text
    
    Args:
        query (str): Text query to embed
        
    Returns:
        list: Text embedding as a list of floats
    """
    if model is None or processor is None:
        raise RuntimeError("CLIP model not loaded")
    
    try:
        # Preprocess text
        inputs = processor(text=[query], return_tensors="pt").to(DEVICE)
        
        # Generate embedding
        with torch.no_grad():
            emb = model.get_text_features(**inputs)
        
        return emb.cpu().numpy().tolist()[0]
    
    except Exception as e:
        logger.error(f"Error generating text embedding: {e}")
        raise

def compute_similarity(image_embedding: list, text_embedding: list):
    """
    Compute cosine similarity between image and text embeddings
    
    Args:
        image_embedding (list): Image embedding
        text_embedding (list): Text embedding
        
    Returns:
        float: Cosine similarity score
    """
    import numpy as np
    
    # Convert to numpy arrays
    img_emb = np.array(image_embedding)
    txt_emb = np.array(text_embedding)
    
    # Compute cosine similarity
    similarity = np.dot(img_emb, txt_emb) / (np.linalg.norm(img_emb) * np.linalg.norm(txt_emb))
    
    return float(similarity)

def is_model_loaded():
    """
    Check if the CLIP model is loaded and ready
    
    Returns:
        bool: True if model is loaded, False otherwise
    """
    return model is not None and processor is not None
