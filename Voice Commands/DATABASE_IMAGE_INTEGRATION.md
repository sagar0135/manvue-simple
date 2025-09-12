# Database Image Integration Guide

This guide explains how to integrate database-driven images into your MANVUE product pages.

## 🚀 Quick Start

### 1. Seed Sample Data
First, create some sample product data in your database:

```bash
cd api/scripts
python seed_product_data.py
```

This will create sample products with color-specific images that you can test with.

### 2. Start the API Server
Make sure your API server is running:

```bash
python api/start_enhanced_backend.py
```

The API should be available at `http://localhost:5001`

### 3. Update Product ID
In your frontend product page (`frontend/categories/tshirts/classic-cotton-crew-neck.html`), update the `PRODUCT_ID` constant to match one of the created product IDs from the seeding script.

### 4. Test the Integration
Open your product page and you should see:
- Product data loaded from the database
- Color-specific images that change when you select different colors
- Fallback to hardcoded images if the API is unavailable

## 🏗️ Architecture

### API Endpoints

#### Get Product Data
```
GET /api/products/{product_id}
```
Returns complete product information including available colors, sizes, and image URLs.

#### Get Product Images by Color
```
GET /api/products/{product_id}/images/{color}
```
Returns images specific to a color variant.

### Database Structure

Products are stored with the following structure:
```json
{
  "id": "product_id",
  "name": "Product Name",
  "price": 24.99,
  "color": ["Black", "White", "Navy"],
  "image_urls": ["url1", "url2", "url3"],
  "image_ids": ["gridfs_id1", "gridfs_id2"]
}
```

### Frontend Integration

The frontend automatically:
1. Fetches product data from the API on page load
2. Loads color-specific images for each available color
3. Updates the UI with database data
4. Falls back to hardcoded data if the API is unavailable

## 🎨 Color-Specific Images

### How It Works
1. Each product has multiple `image_urls` stored in the database
2. When a color is selected, the frontend uses the corresponding images
3. Images are loaded dynamically from the database
4. Thumbnail images are automatically generated from full-size images

### Adding New Colors
To add new colors to a product:
1. Update the product in the database with new color values
2. Add corresponding image URLs for each color
3. The frontend will automatically pick up the new colors

## 🔧 Configuration

### API Base URL
Update the `API_BASE_URL` constant in your frontend:
```javascript
const API_BASE_URL = 'http://localhost:5001/api';
```

### Product ID
Update the `PRODUCT_ID` constant to match your database:
```javascript
const PRODUCT_ID = 'your-product-id-here';
```

## 🛠️ Customization

### Adding More Image Variants
To add more image views (front, back, side):
1. Add more image URLs to the product in the database
2. Update the `updateThumbnailImages` function to handle more thumbnails
3. Modify the thumbnail HTML structure if needed

### Custom Color Mapping
To add support for new colors, update the `getColorValue` function:
```javascript
function getColorValue(colorName) {
    const colorMap = {
        'Black': 'black',
        'White': 'white',
        'Navy': 'navy',
        'Gray': 'gray',
        'Red': 'red',        // Add new colors here
        'Blue': 'blue',      // Add new colors here
        // ... more colors
    };
    return colorMap[colorName] || colorName.toLowerCase();
}
```

## 🐛 Troubleshooting

### Images Not Loading
1. Check that the API server is running
2. Verify the product ID exists in the database
3. Check browser console for API errors
4. Ensure image URLs are accessible

### Fallback Mode
If the API is unavailable, the page will automatically use fallback data. Check the browser console for error messages.

### CORS Issues
If you encounter CORS issues, make sure your API server is configured to allow requests from your frontend domain.

## 📝 Next Steps

1. **Upload Real Images**: Replace the sample Unsplash URLs with your actual product images
2. **GridFS Integration**: Use the GridFS system to store and serve images directly from MongoDB
3. **Image Optimization**: Implement image resizing and optimization for different screen sizes
4. **Caching**: Add caching mechanisms to improve performance
5. **Error Handling**: Enhance error handling for better user experience

## 🔗 Related Files

- `api/routes/products.py` - Product API endpoints
- `api/services/product_service.py` - Product business logic
- `api/scripts/seed_product_data.py` - Sample data seeding
- `frontend/categories/tshirts/classic-cotton-crew-neck.html` - Frontend integration
- `frontend/css/product-page.css` - Styling for product page

## 📚 API Documentation

For complete API documentation, visit: `http://localhost:5001/docs` when your API server is running.
