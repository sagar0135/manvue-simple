# ManVue Organized API

A well-structured, production-ready API for the ManVue e-commerce platform with MongoDB integration, image storage, and ML-powered features.

## 🏗️ Architecture

```
api/
├── main.py                 # Main FastAPI application
├── requirements.txt        # Python dependencies
├── core/                   # Core configuration and utilities
│   ├── __init__.py
│   └── config.py          # Settings and configuration
├── routes/                 # API endpoint definitions
│   ├── __init__.py
│   ├── images.py          # Image upload/management endpoints
│   ├── products.py        # Product CRUD endpoints
│   ├── auth.py            # Authentication endpoints
│   └── ml.py              # Machine learning endpoints
├── models/                 # Pydantic models for request/response
│   ├── __init__.py
│   ├── image_models.py    # Image-related models
│   ├── product_models.py  # Product-related models
│   ├── auth_models.py     # Authentication models
│   └── ml_models.py       # ML-related models
└── services/               # Business logic and service classes
    ├── __init__.py
    ├── image_service.py   # Image management logic
    ├── product_service.py # Product management logic
    ├── auth_service.py    # Authentication logic
    └── ml_service.py      # ML processing logic
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd api
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file in the project root:

```env
MONGO_URI=mongodb://localhost:27017
DB_NAME=manvue_db
SECRET_KEY=your-secret-key-here
DEBUG=true
LOG_LEVEL=INFO
```

### 3. Start the API Server

From the project root directory:

```bash
python start_enhanced_backend.py
```

Or directly from the api directory:

```bash
cd api
python main.py
```

### 4. Access the API

- **API Server**: http://localhost:5001
- **Interactive Documentation**: http://localhost:5001/docs
- **ReDoc Documentation**: http://localhost:5001/redoc

## 📋 API Endpoints

### Images
- `POST /api/images/upload` - Upload image file
- `POST /api/images/upload-base64` - Upload base64 image (Colab)
- `GET /api/images/{file_id}` - Get image file
- `GET /api/images/{file_id}/metadata` - Get image metadata
- `GET /api/images` - List images
- `DELETE /api/images/{file_id}` - Delete image

### Products
- `GET /api/products` - List all products
- `GET /api/products/{product_id}` - Get specific product
- `POST /api/products` - Create new product
- `PUT /api/products/{product_id}` - Update product
- `DELETE /api/products/{product_id}` - Delete product
- `GET /api/products/search/text` - Search products
- `GET /api/products/category/{category}` - Get products by category
- `GET /api/products/featured/trending` - Get featured products

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user
- `POST /api/auth/logout` - User logout
- `POST /api/auth/refresh` - Refresh token

### Machine Learning
- `POST /api/ml/predict` - Analyze image with ML
- `POST /api/ml/similarity` - Compute image-text similarity
- `GET /api/ml/status` - ML service status
- `POST /api/ml/analyze-colors` - Extract image colors
- `POST /api/ml/categorize` - Categorize fashion item
- `GET /api/ml/categories` - Get available categories

## 🧩 Component Details

### Routes
Each route module handles specific API endpoints:
- **Clean separation of concerns**
- **Consistent error handling**
- **Input validation with Pydantic**
- **Comprehensive documentation**

### Models
Pydantic models for type safety and validation:
- **Request/response models**
- **Data validation**
- **Automatic API documentation**
- **Type hints throughout**

### Services
Business logic separated from API layer:
- **Database operations**
- **Complex business rules**
- **External service integration**
- **Reusable across endpoints**

### Core Configuration
Centralized configuration management:
- **Environment-based settings**
- **Type-safe configuration**
- **Easy deployment configuration**
- **Development/production modes**

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MONGO_URI` | MongoDB connection string | `mongodb://localhost:27017` |
| `DB_NAME` | Database name | `manvue_db` |
| `SECRET_KEY` | JWT secret key | `your-secret-key-change-in-production` |
| `DEBUG` | Debug mode | `false` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `5001` |

### Settings Classes

The API supports multiple environment configurations:

```python
# Development
class DevelopmentSettings(Settings):
    debug: bool = True
    log_level: str = "DEBUG"

# Production  
class ProductionSettings(Settings):
    debug: bool = False
    allowed_origins: list = ["https://yourdomain.com"]

# Testing
class TestingSettings(Settings):
    db_name: str = "manvue_test_db"
```

## 🧪 Testing

Run tests with pytest:

```bash
cd api
pytest
```

Test specific modules:

```bash
pytest tests/test_images.py
pytest tests/test_products.py
pytest tests/test_auth.py
```

## 📊 Monitoring and Logging

### Health Check

The API includes comprehensive health monitoring:

```bash
curl http://localhost:5001/health
```

Response includes:
- Overall system status
- Database connectivity
- ML service availability
- Service uptime
- Memory usage

### Logging

Structured logging with configurable levels:

```python
# Configure in core/config.py
LOG_LEVEL=DEBUG  # DEBUG, INFO, WARNING, ERROR
```

## 🚀 Deployment

### Docker

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY api/requirements.txt .
RUN pip install -r requirements.txt

COPY api/ .
COPY backend/ ./backend/

CMD ["python", "main.py"]
```

### Production Considerations

1. **Environment Variables**: Use proper secrets management
2. **CORS**: Configure specific allowed origins
3. **Database**: Use MongoDB Atlas or clustered setup
4. **Monitoring**: Add application monitoring (e.g., Sentry)
5. **Load Balancing**: Use nginx or cloud load balancer
6. **SSL/TLS**: Terminate SSL at load balancer level

## 🔗 Integration

### Frontend Integration

Update frontend API calls:

```javascript
// Update base URL
const API_BASE_URL = "http://localhost:5001";

// Use new endpoints
fetch(`${API_BASE_URL}/api/products`)
fetch(`${API_BASE_URL}/api/images/upload`, {
    method: 'POST',
    body: formData
})
```

### Google Colab Integration

Use the provided Colab integration script:

```python
from backend.colab_integration import ManVueImageUploader

uploader = ManVueImageUploader("http://localhost:5001")
result = uploader.upload_image_file("image.jpg", category="shoes")
```

## 🛠️ Development

### Adding New Endpoints

1. **Create route**: Add to appropriate route module
2. **Define models**: Create Pydantic models
3. **Implement service**: Add business logic to service class
4. **Test**: Write tests for new functionality

### Code Style

Follow these conventions:
- **PEP 8** for Python code style
- **Type hints** for all functions
- **Docstrings** for all classes and functions
- **Async/await** for I/O operations

### Database Schema

The API works with these MongoDB collections:
- `products` - Product information
- `users` - User accounts
- `fs.files` / `fs.chunks` - GridFS image storage

## 🔍 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
2. **Database Connection**: Check MongoDB is running
3. **CORS Issues**: Configure allowed origins properly
4. **File Upload**: Check file size limits and types

### Debug Mode

Enable debug mode for detailed error information:

```env
DEBUG=true
LOG_LEVEL=DEBUG
```

## 📚 API Documentation

When the server is running, visit:
- **Swagger UI**: http://localhost:5001/docs
- **ReDoc**: http://localhost:5001/redoc

These provide interactive API documentation with:
- Endpoint descriptions
- Request/response schemas
- Try-it-out functionality
- Code examples

## 🎯 Next Steps

1. **Authentication**: Implement JWT tokens properly
2. **Caching**: Add Redis for performance
3. **Rate Limiting**: Implement API rate limiting
4. **Webhooks**: Add webhook support for events
5. **Analytics**: Add API usage analytics
6. **Version**: Implement API versioning

---

For more information, see the [MongoDB Integration Guide](../MONGODB_INTEGRATION_GUIDE.md) or check the interactive API documentation when the server is running.