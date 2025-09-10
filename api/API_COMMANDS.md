# 🚀 ManVue API Commands Reference

Quick reference for all API endpoints and commands.

## 🚀 Quick Start

```bash
# Start API services
python launch_api.py

# Test all endpoints
python test_api.py
```

## 📋 API Endpoints

### Core Endpoints

#### Health Check
```bash
curl http://localhost:5000/
```

#### Get All Products
```bash
curl http://localhost:5000/products
```

#### Get Product by ID
```bash
curl http://localhost:5000/products/1
```

#### Add New Product
```bash
curl -X POST http://localhost:5000/products \
  -H "Content-Type: application/json" \
  -d '{
    "title": "New T-Shirt",
    "price": 29.99,
    "category": "tops",
    "type": "tshirts",
    "image_url": "https://via.placeholder.com/150",
    "description": "Comfortable cotton t-shirt",
    "brand": "MANVUE",
    "rating": 4.5
  }'
```

#### Update Product
```bash
curl -X PUT http://localhost:5000/products/1 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated T-Shirt",
    "price": 34.99,
    "category": "tops",
    "type": "tshirts",
    "image_url": "https://via.placeholder.com/150",
    "description": "Updated description",
    "brand": "MANVUE",
    "rating": 4.7
  }'
```

#### Delete Product
```bash
curl -X DELETE http://localhost:5000/products/1
```

### AI Search Endpoints

#### AI Text Search
```bash
curl -X POST http://localhost:5000/products/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "comfortable cotton shirt",
    "category": "tops",
    "filters": {}
  }'
```

#### AI Image Search
```bash
curl -X POST http://localhost:5000/products/image-search \
  -H "Content-Type: application/json" \
  -d '{
    "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ...",
    "include_similar": true
  }'
```

### Authentication Endpoints

#### User Registration
```bash
curl -X POST http://localhost:5000/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

#### User Login
```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

### Admin Endpoints

#### Get All Products (Admin)
```bash
curl http://localhost:5000/admin/products
```

#### Get Products by Category
```bash
curl http://localhost:5000/products/category/tops
```

### ML Service Endpoints

#### ML Health Check
```bash
curl http://localhost:5000/ml/health
```

## 🧪 Testing Commands

### Test API Health
```bash
python test_api.py
```

### Test Specific Endpoint
```bash
# Test health
curl -w "\nStatus: %{http_code}\n" http://localhost:5000/

# Test products
curl -w "\nStatus: %{http_code}\n" http://localhost:5000/products

# Test search
curl -X POST http://localhost:5000/products/search \
  -H "Content-Type: application/json" \
  -d '{"query": "shirt", "category": "all"}' \
  -w "\nStatus: %{http_code}\n"
```

## 🔧 Service Management

### Start Enhanced API
```bash
python enhanced_main.py
```

### Start Simple API
```bash
python simple_main.py
```

### Start ML API
```bash
python ../backend/ML/start_ml_server.py
```

### Start All Services
```bash
python launch_api.py
# Then select option 4
```

## 📊 Response Examples

### Successful Product Response
```json
{
  "id": 1,
  "title": "Classic White T-Shirt",
  "price": 24.99,
  "image_url": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab",
  "category": "tops",
  "type": "tshirts",
  "description": "Comfortable cotton t-shirt",
  "brand": "MANVUE Basics",
  "rating": 4.5,
  "reviews": 127,
  "inStock": true
}
```

### Search Results Response
```json
{
  "query": "cotton shirt",
  "category": "tops",
  "results": [
    {
      "id": 1,
      "title": "Classic White T-Shirt",
      "price": 24.99,
      "relevance_score": 10,
      "category": "tops"
    }
  ],
  "total": 1
}
```

### Image Search Response
```json
{
  "success": true,
  "ml_analysis": {
    "detected_items": [
      {
        "name": "T-Shirt",
        "confidence": 85,
        "category": "tops",
        "type": "tshirts"
      }
    ],
    "colors": [
      {
        "hex": "#ffffff",
        "name": "White",
        "dominance": 0.8
      }
    ],
    "overall_confidence": 85
  },
  "similar_products": [...],
  "source": "ml_api"
}
```

## 🚨 Error Responses

### 404 Not Found
```json
{
  "detail": "Product not found"
}
```

### 400 Bad Request
```json
{
  "detail": "Email already registered"
}
```

### 401 Unauthorized
```json
{
  "detail": "Invalid credentials"
}
```

## 🔗 Useful Links

- **API Documentation**: http://localhost:5000/docs
- **Alternative Docs**: http://localhost:5000/redoc
- **Frontend**: http://localhost:8000
- **ML API**: http://localhost:5001 (if running)

## 💡 Tips

1. **Use the interactive launcher**: `python launch_api.py`
2. **Test everything**: `python test_api.py`
3. **Check API docs**: Visit http://localhost:5000/docs
4. **Monitor logs**: Watch the console output for errors
5. **Use Postman**: Import the API endpoints for easier testing
