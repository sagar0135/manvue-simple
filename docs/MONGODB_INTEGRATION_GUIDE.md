# ManVue MongoDB Integration Guide

Complete guide for integrating MongoDB with image storage for your ManVue e-commerce platform.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Install enhanced backend requirements
pip install -r backend/enhanced_requirements.txt
```

### 2. Setup MongoDB

#### Option A: Local MongoDB
```bash
# Install MongoDB locally
# Windows: Download from https://www.mongodb.com/try/download/community
# macOS: brew install mongodb-community
# Linux: Follow official MongoDB installation guide

# Start MongoDB service
# Windows: Start MongoDB service from Services
# macOS: brew services start mongodb/brew/mongodb-community  
# Linux: sudo systemctl start mongod
```

#### Option B: MongoDB Atlas (Cloud)
1. Create account at https://www.mongodb.com/cloud/atlas
2. Create a free cluster
3. Get connection string
4. Update `.env` file with Atlas URI

### 3. Configure Environment

```bash
# Copy and edit environment file
cp .env.example .env
```

Edit `.env`:
```env
MONGO_URI=mongodb://localhost:27017
DB_NAME=manvue_db
PORT=5001
```

### 4. Start Enhanced Backend

```bash
# Use the startup script
python start_enhanced_backend.py

# Or manually
cd backend
python enhanced_main.py
```

### 5. Access Your API

- **API Server**: http://localhost:5001
- **API Documentation**: http://localhost:5001/docs
- **RedDoc**: http://localhost:5001/redoc

## 📸 Image Upload & Storage

### GridFS Integration

The system uses MongoDB GridFS for efficient image storage:

- **Automatic resizing**: Images are optimized for web delivery
- **Metadata storage**: Category, product associations, ML predictions
- **Scalable**: Handles images of any size
- **Fast retrieval**: Cached image delivery

### API Endpoints

#### Upload Image File
```http
POST /api/images/upload
Content-Type: multipart/form-data

file: [image file]
category: "shoes" (optional)
product_id: "product123" (optional)
```

#### Upload Base64 Image (Colab Integration)
```http
POST /api/images/upload-base64
Content-Type: application/x-www-form-urlencoded

image_data: [base64 string]
filename: "image.jpg"
category: "tops" (optional)
product_id: "product123" (optional)
```

#### Get Image
```http
GET /api/images/{file_id}
```

#### List Images
```http
GET /api/images?category=shoes&limit=50&skip=0
```

## 🤖 Google Colab Integration

### Setup in Colab

```python
# 1. Upload the integration script
from google.colab import files
uploaded = files.upload()  # Upload colab_integration.py

# 2. Import and use
from colab_integration import ManVueImageUploader

# 3. Initialize uploader
uploader = ManVueImageUploader("https://your-manvue-api.com")
```

### Upload Single Image

```python
# Upload from file path
result = uploader.upload_image_file(
    "path/to/image.jpg", 
    category="shoes"
)
print(f"Image URL: {result['image_url']}")
```

### Upload from NumPy Array

```python
import numpy as np

# Generate or process image array
image_array = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)

# Upload the array
result = uploader.upload_image_array(
    image_array, 
    filename="generated_image.jpg",
    category="tops"
)
```

### Create Product with Images

```python
# Product data
product_data = {
    "name": "Classic White Sneaker",
    "price": 89.99,
    "category": "shoes",
    "type": "sneakers",
    "description": "Comfortable white sneakers",
    "brand": "ManVue",
    "size": ["7", "8", "9", "10", "11"],
    "color": ["White", "Black"],
    "tags": ["casual", "comfortable"]
}

# Image paths from your Colab environment
image_paths = [
    "sneaker_front.jpg",
    "sneaker_side.jpg", 
    "sneaker_back.jpg"
]

# Create product with images
product = uploader.create_product_with_images(product_data, image_paths)
print(f"Created product: {product['id']}")
```

### Batch Upload

```python
from colab_integration import batch_upload

# Upload multiple images
image_paths = ["img1.jpg", "img2.jpg", "img3.jpg"]
urls = batch_upload(image_paths, category="accessories")

# Check results
for i, url in enumerate(urls):
    print(f"Image {i+1}: {url}")
```

## 🧠 ML Integration

### Automatic Image Analysis

When images are uploaded, the system automatically:

1. **Categorizes** the product using ML models
2. **Extracts colors** and style information  
3. **Generates tags** for better searchability
4. **Creates embeddings** for similarity search

### ML Endpoints

#### Get ML Predictions
```http
POST /api/ml/predict
Content-Type: application/json

{
    "image_data": "data:image/jpeg;base64,...",
    "include_colors": true
}
```

Response:
```json
{
    "detected_items": [
        {
            "name": "Sneaker",
            "confidence": 95,
            "category": "shoes",
            "type": "shoes"
        }
    ],
    "colors": [
        {
            "hex": "#ffffff",
            "name": "White",
            "dominance": 0.75
        }
    ],
    "overall_confidence": 95
}
```

## 💾 Database Schema

### Products Collection

```json
{
    "_id": "ObjectId",
    "name": "Product Name",
    "title": "Display Title",
    "price": 99.99,
    "originalPrice": 129.99,
    "category": "shoes",
    "type": "sneakers",
    "size": ["7", "8", "9"],
    "color": ["White", "Black"],
    "brand": "Brand Name",
    "rating": 4.5,
    "reviews": 123,
    "image_ids": ["gridfs_id1", "gridfs_id2"],
    "image_urls": ["url1", "url2"],
    "tags": ["casual", "sport"],
    "inStock": true,
    "description": "Product description",
    "features": ["Feature 1", "Feature 2"],
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
}
```

### Images in GridFS

```json
{
    "_id": "ObjectId",
    "filename": "image.jpg",
    "contentType": "image/jpeg",
    "length": 1024000,
    "metadata": {
        "category": "shoes",
        "product_id": "product123",
        "upload_date": "2024-01-01T00:00:00Z",
        "ml_predictions": {
            "detected_items": [...],
            "colors": [...]
        }
    }
}
```

## 🔄 Migration from Old System

### Update Frontend

The frontend automatically detects the new image structure:

```javascript
// Old way (still works)
product.image

// New way (automatic)
getProductImageUrl(product) // Handles image_ids, image_urls, fallbacks
```

### Update API Calls

```javascript
// Change API base URL
const API_BASE_URL = "http://localhost:5001"; // Was 5000
```

### Migrate Existing Data

```python
# Run migration script to move existing products to MongoDB
python scripts/migrate_to_mongodb.py
```

## 🛠️ Development

### Testing

```bash
# Run tests
cd backend
pytest

# Test specific functionality
pytest tests/test_image_upload.py
```

### Adding New Features

1. **New Image Processors**: Add to `backend/image_processors/`
2. **New ML Models**: Update `backend/ML/models/`
3. **New API Endpoints**: Add to `backend/enhanced_main.py`

### Performance Optimization

- **Image Caching**: Images are cached for 24 hours
- **Lazy Loading**: Products load images on demand
- **Compression**: Automatic image optimization
- **CDN Ready**: Easy integration with CDN services

## 📱 Frontend Integration

### Updated Product Display

```javascript
// Products now support multiple images
function displayProduct(product) {
    // Get primary image
    const imageUrl = getProductImageUrl(product);
    
    // Get all images for gallery
    const allImages = getAllProductImages(product);
}
```

### Image Gallery

```javascript
// Create image thumbnails
function createThumbnails(product) {
    const images = getAllProductImages(product);
    // Display all available images
}
```

## 🚨 Troubleshooting

### Common Issues

#### MongoDB Connection Failed
```bash
# Check MongoDB status
mongosh --eval "db.runCommand('ping')"

# Start MongoDB service
# Windows: net start MongoDB
# macOS: brew services start mongodb-community
# Linux: sudo systemctl start mongod
```

#### Missing Dependencies
```bash
# Install all requirements
pip install -r backend/enhanced_requirements.txt
```

#### Image Upload Failed
- Check file size (max 16MB for GridFS)
- Verify image format (JPEG, PNG, GIF, WebP)
- Check MongoDB disk space

#### Frontend Not Loading Images
- Verify API is running on port 5001
- Check browser console for CORS errors
- Confirm image URLs are properly generated

### Getting Help

1. **Check Logs**: Server logs show detailed error information
2. **API Documentation**: Visit `/docs` for interactive API testing  
3. **MongoDB Logs**: Check MongoDB logs for database issues
4. **Browser DevTools**: Network tab shows API request/response details

## 🎯 Next Steps

1. **Deploy to Production**: Use Docker containers for easy deployment
2. **Add Authentication**: Implement user authentication and authorization
3. **Scale Images**: Use CDN for global image delivery
4. **ML Enhancement**: Add more sophisticated ML models
5. **Analytics**: Track image performance and user engagement

## 📚 Additional Resources

- [MongoDB Documentation](https://docs.mongodb.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [GridFS Guide](https://docs.mongodb.com/manual/core/gridfs/)
- [Google Colab Guide](https://colab.research.google.com/notebooks/intro.ipynb)

---

**Need Help?** Open an issue or check the API documentation at `/docs` when your server is running.
