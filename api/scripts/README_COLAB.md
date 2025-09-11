# MANVUE Colab Integration Guide

This guide shows how to use MANVUE's image conversion scripts in Google Colab.

## 🚀 Quick Start (Recommended)

### Option 1: One-Click Setup
```python
# Upload colab_quick_start.py to your Colab environment
from colab_quick_start import run_quick_setup

# Run the complete setup
products = run_quick_setup("http://localhost:5001")
```

### Option 2: Full Setup
```python
# Upload colab_image_setup.py to your Colab environment
from colab_image_setup import run_colab_setup

# Run the complete setup
products = run_colab_setup("http://localhost:5001")
```

## 📋 Prerequisites

1. **MANVUE Backend Running**: Your API server must be accessible
2. **MongoDB Access**: Database must be reachable from Colab
3. **Script Upload**: Upload the Python scripts to your Colab environment

## 🔧 Setup Steps

### Step 1: Upload Scripts
Upload these files to your Colab environment:
- `colab_quick_start.py` (for quick setup)
- `colab_image_setup.py` (for full setup)
- `colab_notebook_example.ipynb` (example notebook)

### Step 2: Configure API URL
```python
# For local development
API_URL = "http://localhost:5001"

# For deployed API
API_URL = "https://your-deployed-api.com"

# For ngrok tunnel (if testing locally)
API_URL = "https://your-ngrok-url.ngrok.io"
```

### Step 3: Run Setup
```python
# Quick setup (creates 2 sample products)
from colab_quick_start import run_quick_setup
products = run_quick_setup(API_URL)

# Full setup (creates 3 detailed products)
from colab_image_setup import run_colab_setup
products = run_colab_setup(API_URL)
```

## 📊 What Gets Created

### Images in GridFS
- All external images downloaded and stored in MongoDB
- Optimized and properly formatted
- Unique GridFS file IDs generated

### Product Data
- Complete product information
- GridFS image references
- Ready for your frontend

### Example Output
```json
{
  "id": "507f1f77bcf86cd799439011",
  "name": "Classic Cotton Crew Neck",
  "price": 24.99,
  "image_ids": ["gridfs_id_1", "gridfs_id_2", "gridfs_id_3"],
  "image_urls": [
    "http://localhost:5001/api/images/gridfs_id_1",
    "http://localhost:5001/api/images/gridfs_id_2",
    "http://localhost:5001/api/images/gridfs_id_3"
  ]
}
```

## 🌐 API Endpoints

After setup, your API serves:
- `GET /api/products` - List all products
- `GET /api/products/{id}` - Get specific product
- `GET /api/images/{file_id}` - Serve images from GridFS

## 🐛 Troubleshooting

### Connection Issues
```python
# Test your API connection
import requests
response = requests.get(f"{API_URL}/health")
print(response.json())
```

### Common Solutions
1. **API Not Accessible**: Use ngrok or deploy your API
2. **MongoDB Issues**: Check your database connection
3. **Image Download Fails**: Check internet connectivity in Colab

### Using ngrok for Local Testing
```bash
# Install ngrok
pip install pyngrok

# In your local terminal
ngrok http 5001

# Use the ngrok URL in Colab
API_URL = "https://your-ngrok-url.ngrok.io"
```

## 📱 Frontend Integration

After running the setup:

1. **Get Product IDs**: Use the returned product data
2. **Update Frontend**: Replace hardcoded product IDs
3. **Test Images**: Verify images load from GridFS

```javascript
// In your frontend
const PRODUCT_ID = "507f1f77bcf86cd799439011"; // From Colab output
const API_BASE_URL = "http://localhost:5001/api";
```

## 🔄 Workflow

1. **Develop Locally**: Build your MANVUE backend
2. **Test in Colab**: Use these scripts to populate data
3. **Deploy**: Move to production with real data
4. **Scale**: Add more products and images

## 📚 Example Notebook

Use `colab_notebook_example.ipynb` for a complete walkthrough:
- Step-by-step instructions
- Error handling examples
- Result visualization
- Download options

## 🎯 Benefits

- ✅ **No Local Setup**: Run everything in Colab
- ✅ **Cloud Storage**: Images stored in MongoDB
- ✅ **Scalable**: Handle large datasets
- ✅ **Integrated**: Works with your existing API
- ✅ **Portable**: Move between environments easily

## 🔗 Related Files

- `colab_quick_start.py` - One-click setup
- `colab_image_setup.py` - Full setup with options
- `colab_notebook_example.ipynb` - Complete example
- `colab_integration.py` - General Colab utilities
- `../backend/colab_integration.py` - Original Colab integration

## 💡 Tips

1. **Use ngrok** for local API testing in Colab
2. **Save results** to JSON files for backup
3. **Test connections** before running full setup
4. **Monitor logs** for debugging information
5. **Use quick setup** for testing, full setup for production
