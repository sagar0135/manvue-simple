# MANVUE Image Scripts

This directory contains scripts for converting external images to MongoDB GridFS and seeding product data.

## 🚀 Quick Start

### Complete Setup (Recommended)
Run the complete setup script to convert images and seed data in one go:

```bash
cd api/scripts
python setup_manvue_images.py
```

This script will:
1. Check your MongoDB connection
2. Download external images from URLs
3. Store images in GridFS
4. Seed products with GridFS image references
5. Verify the complete setup

### Manual Steps

#### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 2. Convert Images to GridFS
```bash
python convert_images_to_gridfs.py
```

This will:
- Download images from external URLs (Unsplash)
- Store them in MongoDB GridFS
- Generate a `converted_products_with_gridfs_ids.json` file with GridFS IDs

#### 3. Seed Product Data
```bash
python seed_product_data.py
```

This will:
- Check for converted images (from step 2)
- Create products in the database with GridFS image references
- Fall back to external URLs if no converted images found

## 📁 Files

- `setup_manvue_images.py` - Complete setup script (recommended)
- `convert_images_to_gridfs.py` - Image conversion to GridFS
- `seed_product_data.py` - Product data seeding
- `requirements.txt` - Python dependencies
- `README.md` - This file

## 🔧 Configuration

### Environment Variables
Set these in your `.env` file:

```env
MONGO_URI=mongodb://localhost:27017
DB_NAME=manvue_db
```

### API Base URL
The scripts assume your API runs on `http://localhost:5001`. 
Update the `api_base_url` in `ProductService` if different.

## 🎯 What Gets Created

### Images in GridFS
- All external images are downloaded and stored in MongoDB
- Images are optimized and have proper metadata
- Each image gets a unique GridFS file ID

### Product Data
- Products with complete information (name, price, colors, etc.)
- GridFS image IDs linked to products
- Fallback external URLs for compatibility

### Example Product Structure
```json
{
  "name": "Classic Cotton Crew Neck",
  "price": 24.99,
  "color": ["Black", "White", "Navy", "Gray"],
  "image_ids": ["gridfs_id_1", "gridfs_id_2", "gridfs_id_3"],
  "image_urls": ["http://localhost:5001/api/images/gridfs_id_1", ...]
}
```

## 🌐 API Endpoints

After running the scripts, your API will serve:

- `GET /api/products` - List all products with image URLs
- `GET /api/products/{id}` - Get specific product
- `GET /api/images/{file_id}` - Serve images from GridFS
- `GET /api/products/{id}/images` - Get product images

## 🐛 Troubleshooting

### Database Connection Issues
```bash
# Check MongoDB is running
systemctl status mongod  # Linux
brew services list mongodb  # macOS

# Test connection manually
python -c "import asyncio; from backend.database import test_connection; print(asyncio.run(test_connection()))"
```

### Image Download Issues
- Check internet connectivity
- Verify Unsplash URLs are accessible
- Check for rate limiting or firewall issues

### Missing Dependencies
```bash
pip install -r requirements.txt
```

### Port Issues
- Ensure port 5001 is available for the API
- Update `api_base_url` in ProductService if using different port

## 📊 Output

### Successful Run Example
```
🚀 MANVUE Image Setup - Converting External Images to GridFS
============================================================
🔌 Checking database connection...
✅ Database connection successful!
📁 Checking existing images in GridFS...
📭 No existing images found in GridFS

🎯 No existing images found. Starting conversion process...
📥 Downloading: https://images.unsplash.com/photo-1521572163474...
✅ Downloaded: classic_cotton_crew_neck_image_1.jpg (45230 bytes)
💾 Stored in GridFS: classic_cotton_crew_neck_image_1.jpg (ID: 507f1f77bcf86cd799439011)
...

🌱 Starting product data seeding...
📁 Found converted GridFS images! Using GridFS image IDs.
Creating product: Classic Cotton Crew Neck
  📷 Using 3 GridFS images
✅ Created product: Classic Cotton Crew Neck (ID: 507f1f77bcf86cd799439012)
...

🎉 Setup completed successfully!
```

## 🔗 Related Files

- `../../backend/database.py` - Database connection and GridFS functions
- `../routes/products.py` - Product API endpoints  
- `../routes/images.py` - Image serving endpoints
- `../services/product_service.py` - Product business logic
