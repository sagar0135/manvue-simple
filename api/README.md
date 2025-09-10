# 🚀 ManVue API Folder

This folder contains all API-related files and commands for easy access and management.

## 📁 Contents

- **`launch_api.py`** - Main API launcher with interactive menu
- **`test_api.py`** - Comprehensive API testing suite
- **`enhanced_main.py`** - Enhanced API with ML features
- **`simple_main.py`** - Simple API without ML dependencies
- **`API_COMMANDS.md`** - Complete API commands reference
- **`start_api.bat`** - Windows batch file to start API
- **`start_api.sh`** - Unix/Linux/Mac shell script to start API

## 🚀 Quick Start

### Option 1: Interactive Launcher (Recommended)
```bash
python launch_api.py
```

### Option 2: Direct Execution
```bash
# Windows
start_api.bat

# Unix/Linux/Mac
./start_api.sh
```

### Option 3: Manual Start
```bash
# Enhanced API (with ML)
python enhanced_main.py

# Simple API (basic)
python simple_main.py
```

## 🧪 Testing

### Test All Endpoints
```bash
python test_api.py
```

### Test Individual Endpoints
See `API_COMMANDS.md` for detailed curl commands.

## 📋 Available Services

### 1. Enhanced API (Port 5000)
- ✅ AI-powered text search
- ✅ AI-powered image search
- ✅ Product management (CRUD)
- ✅ User authentication
- ✅ Admin panel
- ✅ ML integration

### 2. Simple API (Port 5000)
- ✅ Basic product operations
- ✅ User authentication
- ✅ No ML dependencies
- ✅ Lightweight and fast

### 3. ML API Server (Port 5001)
- ✅ Fashion recognition
- ✅ Image analysis
- ✅ TensorFlow models
- ✅ Fashion-MNIST dataset

## 🔧 Configuration

### Environment Variables
Create `../backend/.env`:
```ini
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/
DB_NAME=manvue
JWT_SECRET=your-secret-key
JWT_ALGORITHM=HS256
```

### Dependencies
Install required packages:
```bash
pip install -r ../backend/requirements.txt
```

## 📊 API Endpoints

### Core Endpoints
- `GET /` - Health check
- `GET /products` - Get all products
- `POST /products` - Add product
- `GET /products/{id}` - Get product by ID
- `PUT /products/{id}` - Update product
- `DELETE /products/{id}` - Delete product

### AI Search
- `POST /products/search` - AI text search
- `POST /products/image-search` - AI image search
- `GET /ml/health` - ML service status

### Authentication
- `POST /register` - User registration
- `POST /login` - User login

### Admin
- `GET /admin/products` - Admin product management

## 🌐 Access Points

- **API**: http://localhost:5000
- **API Docs**: http://localhost:5000/docs
- **Alternative Docs**: http://localhost:5000/redoc
- **Frontend**: http://localhost:8000
- **ML API**: http://localhost:5001 (if running)

## 🛠️ Troubleshooting

### Common Issues

1. **Port 5000 already in use**
   ```bash
   # Kill process using port 5000
   netstat -ano | findstr :5000
   taskkill /PID <PID> /F
   ```

2. **Dependencies missing**
   ```bash
   pip install -r ../backend/requirements.txt
   ```

3. **ML API not responding**
   - Check if ML server is running on port 5001
   - Verify TensorFlow installation
   - Check ML model files in `../backend/ML/models/`

4. **CORS errors**
   - API includes CORS middleware
   - Check browser console for specific errors
   - Verify frontend is served from correct port

### Logs and Debugging

- **API Logs**: Check console output when running API
- **Frontend Logs**: Check browser developer console
- **ML Logs**: Check ML server console output

## 📝 Usage Examples

### Start Enhanced API
```bash
python launch_api.py
# Select option 1
```

### Test All Endpoints
```bash
python test_api.py
```

### Quick API Test
```bash
curl http://localhost:5000/
```

### Add Product via API
```bash
curl -X POST http://localhost:5000/products \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Product", "price": 19.99, "category": "tops"}'
```

## 🔗 Related Files

- **Frontend**: `../frontend/` - Web interface
- **Backend Core**: `../backend/` - Core backend files
- **ML Models**: `../backend/ML/` - Machine learning components
- **Main Launcher**: `../start_manvue.py` - Complete platform launcher

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review `API_COMMANDS.md` for detailed examples
3. Check the main project README.md
4. Verify all dependencies are installed correctly
