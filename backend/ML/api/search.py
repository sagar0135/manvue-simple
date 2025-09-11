import sys, json, io
from pymongo import MongoClient
import gridfs
import numpy as np
from PIL import Image
import torch
from transformers import CLIPProcessor, CLIPModel
import faiss

# MongoDB connection
MONGO_URI = "mongodb+srv://19276146:19276146@manvue.ilich4r.mongodb.net/?retryWrites=true&w=majority&appName=MANVUE"
client = MongoClient(MONGO_URI)
db = client["MANVUE"]
fs = gridfs.GridFS(db)

# Load CLIP
device = "cuda" if torch.cuda.is_available() else "cpu"
clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# Load FAISS index (you should build and save it beforehand in Colab, then load here)
index = faiss.read_index("fashion.index")
with open("metadata.json", "r") as f:
    metadata = json.load(f)

# Get filename from Node.js
filename = sys.argv[1]

# Retrieve uploaded image from MongoDB
file = fs.find_one({"filename": filename})
if not file:
    print(json.dumps({"error": "File not found"}))
    sys.exit(1)

img = Image.open(io.BytesIO(file.read())).convert("RGB")

# Get embedding
inputs = clip_processor(images=[img], return_tensors="pt").to(device)
with torch.no_grad():
    outputs = clip_model.get_image_features(**inputs)
emb = outputs / outputs.norm(p=2, dim=-1, keepdim=True)
emb = emb.cpu().numpy().astype("float32")

# Search FAISS
D, I = index.search(emb, 5)
results = [metadata[idx] for idx in I[0]]

print(json.dumps(results))
