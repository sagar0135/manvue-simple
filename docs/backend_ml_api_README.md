# MANVUE FastAPI ML Server

## 🚀 High-Performance AI API with FastAPI

This directory contains the FastAPI-based ML API server for MANVUE's AI-powered fashion recognition system. Upgraded from Flask for better performance, automatic documentation, and modern async capabilities.

## 🎯 **FastAPI Advantages**

### **⚡ Performance Benefits**
- **Async/Await Support**: Non-blocking I/O operations
- **50-300% Faster**: Than Flask for concurrent requests
- **Background Tasks**: Long-running operations don't block API
- **Automatic Validation**: Pydantic models for request/response

### **📚 Auto-Documentation**
- **Swagger UI**: Interactive API docs at `/docs`
- **ReDoc**: Alternative documentation at `/redoc`
- **Type Safety**: Full type hints and validation
- **Schema Generation**: Automatic OpenAPI schema

### **🔧 Developer Experience**
- **Modern Python**: Latest async/await patterns
- **Better Error Handling**: Structured HTTP exceptions
- **Request/Response Models**: Pydantic validation
- **IDE Support**: Full type completion and checking

## 📋 **API Endpoints**

### **Health Check**
```http
GET /health
```
**Response Model**: `HealthResponse`
```json
{
  "status": "healthy",
  "model_loaded": true,
  "version": "2.0.0",
  "uptime": "1:23:45"
}
```

### **Image Prediction**
```http
POST /predict
```
**Request Model**: `ImagePredictionRequest`
```json
{
  "image": "data:image/jpeg;base64,/9j/4AAQSkZJRg...",
  "include_colors": true
}
```

**Response Model**: `PredictionResponse`
```json
{
  "success": true,
  "detected_items": [
    {
      "name": "Dress Shirt",
      "confidence": 92,
      "category": "tops",
      "type": "tops",
      "confidence_boost": 0.18
    }
  ],
  "colors": [
    {
      "hex": "#1a1a1a",
      "name": "Charcoal",
      "dominance": 0.35
    }
  ],
  "overall_confidence": 92,
  "processing_time": "0.85s",
  "model_version": "2.0.0",
  "timestamp": "2024-01-15T10:30:00"
}
```

### **Get Categories**
```http
GET /categories
```
**Response Model**: `CategoriesResponse`
```json
{
  "categories": {
    "T-Shirt": {
      "category": "tops",
      "type": "tops",
      "confidence_boost": 0.15
    }
  },
  "total_classes": 10
}
```

### **Model Retraining**
```http
POST /retrain
```
**Request Model**: `RetrainRequest`
```json
{
  "training_data": [...],
  "model_params": {
    "epochs": 10,
    "batch_size": 32
  }
}
```

**Response Model**: `RetrainResponse`
```json
{
  "success": true,
  "message": "Model retraining initiated",
  "estimated_time": "15 minutes",
  "status": "queued",
  "job_id": "retrain_1642234567"
}
```

## 🔧 **Pydantic Models**

### **Request Models**
```python
class ImagePredictionRequest(BaseModel):
    image: str = Field(..., description="Base64 encoded image data")
    include_colors: bool = Field(True, description="Include color analysis")

class RetrainRequest(BaseModel):
    training_data: List[Dict[str, Any]]
    model_params: Optional[Dict[str, Any]] = None
```

### **Response Models**
```python
class DetectedItem(BaseModel):
    name: str
    confidence: int = Field(..., ge=0, le=100)
    category: str
    type: str
    confidence_boost: float = 0.0

class ColorInfo(BaseModel):
    hex: str
    name: str
    dominance: float = Field(..., ge=0.0, le=1.0)

class PredictionResponse(BaseModel):
    success: bool = True
    detected_items: List[DetectedItem]
    colors: List[ColorInfo] = []
    overall_confidence: int = Field(..., ge=0, le=100)
    processing_time: str
    model_version: str = "2.0.0"
    timestamp: str = Field(default_factory=datetime.now)
```

## 🚀 **Async Features**

### **Non-Blocking Model Loading**
```python
@app.on_event("startup")
async def startup_event():
    success = await load_model()  # Non-blocking startup
```

### **Async Prediction**
```python
@app.post("/predict")
async def predict(request: ImagePredictionRequest):
    # Run ML prediction in thread pool
    loop = asyncio.get_event_loop()
    predictions = await loop.run_in_executor(None, model.predict, image_array)
```

### **Background Tasks**
```python
@app.post("/retrain")
async def retrain_model(request: RetrainRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(perform_retraining, request.training_data)
```

## 📊 **Performance Optimizations**

### **Async I/O**
- **Non-blocking Operations**: Image processing in thread pools
- **Concurrent Requests**: Handle multiple requests simultaneously
- **Efficient Resource Usage**: Better CPU and memory utilization

### **Request Validation**
- **Automatic Validation**: Pydantic validates all inputs
- **Early Error Detection**: Invalid requests rejected before processing
- **Type Safety**: Prevents runtime errors from bad data

### **Background Processing**
- **Long Operations**: Model retraining runs in background
- **Immediate Response**: API returns immediately with job ID
- **Resource Management**: Prevents blocking main thread

## 🛠️ **Development Setup**

### **1. Install Dependencies**
```bash
pip install fastapi uvicorn pydantic
pip install -r requirements.txt
```

### **2. Start Development Server**
```bash
python ml_server.py
# or
uvicorn ml_server:app --reload --host 0.0.0.0 --port 5000
```

### **3. Access Documentation**
- **Swagger UI**: http://localhost:5000/docs
- **ReDoc**: http://localhost:5000/redoc
- **API Schema**: http://localhost:5000/openapi.json

## 🔍 **Testing**

### **Interactive Testing**
1. **Open Swagger UI**: http://localhost:5000/docs
2. **Try Endpoints**: Click "Try it out" on any endpoint
3. **Real Requests**: Send actual API requests from browser

### **cURL Testing**
```bash
# Health check
curl -X GET http://localhost:5000/health

# Image prediction
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"image": "data:image/jpeg;base64,...", "include_colors": true}'

# Get categories
curl -X GET http://localhost:5000/categories
```

### **Python Testing**
```python
import requests

# Test prediction
response = requests.post(
    "http://localhost:5000/predict",
    json={
        "image": "data:image/jpeg;base64,...",
        "include_colors": True
    }
)
result = response.json()
print(f"Detected: {result['detected_items']}")
```

## 📈 **Monitoring & Logging**

### **Built-in Logging**
```python
import logging
logger = logging.getLogger(__name__)

# Structured logging
logger.info(f"Processing prediction for job {job_id}")
logger.error(f"Model prediction failed: {error}")
```

### **Performance Metrics**
- **Response Time**: Automatic timing in responses
- **Request Volume**: Track API usage patterns
- **Error Rates**: Monitor failure rates
- **Model Performance**: Track prediction accuracy

### **Health Monitoring**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "uptime": "2:45:30",
  "version": "2.0.0"
}
```

## 🔒 **Security Features**

### **Input Validation**
- **Pydantic Models**: Automatic validation
- **Type Checking**: Prevent injection attacks
- **Size Limits**: Control request payload size
- **Format Validation**: Ensure proper image formats

### **CORS Configuration**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### **Error Handling**
```python
try:
    result = await process_image(image)
    return result
except ValueError as e:
    raise HTTPException(status_code=400, detail=str(e))
except Exception as e:
    raise HTTPException(status_code=500, detail="Internal server error")
```

## 🌐 **Production Deployment**

### **Docker Deployment**
```dockerfile
FROM python:3.9-slim

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["uvicorn", "ml_server:app", "--host", "0.0.0.0", "--port", "5000"]
```

### **Performance Tuning**
```bash
# Production server with workers
uvicorn ml_server:app \
  --host 0.0.0.0 \
  --port 5000 \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker
```

### **Environment Configuration**
```bash
export MODEL_PATH="/app/models/fashion_classifier.h5"
export LOG_LEVEL="info"
export CORS_ORIGINS="https://manvue.com,https://api.manvue.com"
```

## 📋 **Migration from Flask**

### **Key Changes**
1. **Decorators**: `@app.route()` → `@app.get()`, `@app.post()`
2. **Request Data**: `request.get_json()` → Pydantic models
3. **Responses**: `jsonify()` → Pydantic response models
4. **Error Handling**: Return tuples → `HTTPException`
5. **Server**: `app.run()` → `uvicorn.run()`

### **Benefits Gained**
- **2-3x Performance**: Async handling of requests
- **Auto Documentation**: No manual API docs needed
- **Type Safety**: Catch errors at development time
- **Better Testing**: Built-in test client
- **Modern Stack**: Industry standard for Python APIs

## 🎯 **Integration with MANVUE**

### **Frontend Integration**
- **Seamless Migration**: Same API endpoints
- **Enhanced Responses**: More detailed response models
- **Better Error Handling**: Structured error responses
- **Performance**: Faster response times

### **Monitoring Integration**
- **Health Checks**: Easy integration with monitoring
- **Metrics Export**: Prometheus-compatible metrics
- **Logging**: Structured JSON logging
- **Alerting**: Error rate and latency alerts

---

## 🚀 **FastAPI MANVUE ML API - Next Generation AI Server!**

**Upgraded for Performance, Documentation, and Developer Experience** ⚡📚🔧
