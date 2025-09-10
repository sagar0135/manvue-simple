# 🚀 ManVue - AI-Powered Fashion E-commerce Platform

A comprehensive, production-ready e-commerce platform with AI-powered search, product management, and modern web technologies.

## ✨ Features

### 🤖 AI-Powered Search
- **Text Search**: Intelligent product search with ML-enhanced relevance
- **Image Search**: Upload images to find similar products using AI
- **Voice Search**: Speech-to-text search functionality
- **Visual Recognition**: Fashion item detection and categorization

### 🛠️ Product Management
- **Admin Panel**: Complete CRUD operations for products
- **Real-time Updates**: Instant product updates across the platform
- **Category Management**: Organized product categorization
- **Image Upload**: Support for product image management

### 🎨 Modern UI/UX
- **Responsive Design**: Works perfectly on all devices
- **Interactive Elements**: Smooth animations and transitions
- **Shopping Cart**: Full cart functionality with persistence
- **User Authentication**: Secure login and registration system

### 🔧 Technical Features
- **FastAPI Backend**: High-performance async API
- **ML Integration**: TensorFlow-based fashion recognition
- **RESTful API**: Clean, documented API endpoints
- **CORS Support**: Cross-origin resource sharing enabled

## 🚀 Quick Start

### Option 1: One-Command Startup (Recommended)
```bash
python start_manvue.py
```
This will:
- ✅ Check dependencies
- ✅ Start backend server (port 5000)
- ✅ Start frontend server (port 8000)
- ✅ Open browser automatically
- ✅ Show API documentation

### Option 2: API-Only Setup
```bash
cd api
python launch_api.py
```
This provides:
- 🚀 Interactive API launcher
- 🧪 Built-in API testing
- 📋 Command reference
- 🔧 Service management

### Option 3: Manual Setup

#### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python enhanced_main.py
```

#### Frontend Setup
```bash
cd frontend
python -m http.server 8000
```

## 📁 Project Structure

```
manvue-simple/
├── 🚀 start_manvue.py           # One-command startup script
├── 📋 README.md                 # This file
├── 📁 api/                      # API management and commands
│   ├── launch_api.py           # Interactive API launcher
│   ├── test_api.py             # API testing suite
│   ├── enhanced_main.py        # Enhanced API with ML features
│   ├── simple_main.py          # Simple API without ML
│   ├── API_COMMANDS.md         # Complete API reference
│   ├── start_api.bat           # Windows API launcher
│   ├── start_api.sh            # Unix/Linux/Mac API launcher
│   └── README.md               # API folder documentation
├── backend/
│   ├── main.py                 # Original backend structure
│   ├── database.py             # Database connection
│   ├── auth.py                 # Authentication utilities
│   ├── products.py             # Product operations
│   ├── requirements.txt        # Python dependencies
│   ├── .env                    # Environment variables
│   └── ML/                     # Machine Learning components
│       ├── api/ml_server.py    # ML API server
│       ├── models/             # Trained ML models
│       ├── data/               # Training data
│       └── notebooks/          # Jupyter notebooks
└── frontend/
    ├── index.html              # Main application page
    ├── js/script.js            # Enhanced JavaScript with ML integration
    ├── css/style.css           # Modern responsive styling
    ├── data/                   # Product data files
    └── assets/                 # Images and static assets
```

## 🔧 API Endpoints

### Core Endpoints
- `GET /` - API health check and information
- `GET /products` - Get all products
- `POST /products` - Add new product
- `GET /products/{id}` - Get specific product
- `PUT /products/{id}` - Update product
- `DELETE /products/{id}` - Delete product

### AI Search Endpoints
- `POST /products/search` - AI-powered text search
- `POST /products/image-search` - AI-powered image search
- `GET /ml/health` - ML service status

### Authentication
- `POST /register` - User registration
- `POST /login` - User login

### Admin
- `GET /admin/products` - Admin product management

## 🎯 Usage Examples

### AI Text Search
```javascript
// Search for products using AI
const results = await fetch('/products/search', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        query: 'comfortable cotton shirt',
        category: 'tops'
    })
});
```

### AI Image Search
```javascript
// Search using image upload
const results = await fetch('/products/image-search', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        image: 'data:image/jpeg;base64,...',
        include_similar: true
    })
});
```

### Product Management
```javascript
// Add new product
const newProduct = await fetch('/products', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        title: 'New T-Shirt',
        price: 29.99,
        category: 'tops',
        image_url: 'https://example.com/image.jpg'
    })
});
```

## 🛠️ Admin Panel

Access the admin panel by:
1. Opening the website
2. Clicking "🛠️ Admin" in the mobile navigation
3. Or navigating to the admin section

**Admin Features:**
- ➕ Add new products
- ✏️ Edit existing products
- 🗑️ Delete products
- 📊 View all products
- 🔄 Real-time updates

## 🤖 ML Integration

The platform includes advanced ML capabilities:

### Fashion Recognition
- **Model**: Convolutional Neural Network (CNN)
- **Dataset**: Fashion-MNIST + custom data
- **Accuracy**: 90%+ on test set
- **Categories**: 10 fashion types optimized for men's clothing

### Search Enhancement
- **Text Embeddings**: Semantic search capabilities
- **Image Analysis**: Visual similarity matching
- **Confidence Scoring**: Accurate prediction confidence
- **Fallback Support**: Graceful degradation when ML unavailable

## 🔧 Configuration

### Environment Variables
Create `backend/.env`:
```ini
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/
DB_NAME=manvue
JWT_SECRET=your-secret-key
JWT_ALGORITHM=HS256
```

### API Configuration
- **Backend Port**: 5000
- **Frontend Port**: 8000
- **ML API Port**: 5001 (optional)

## 📊 Performance

- **Backend**: FastAPI with async operations
- **Frontend**: Optimized JavaScript with lazy loading
- **ML**: TensorFlow models with GPU acceleration support
- **Database**: MongoDB with connection pooling

## 🚀 Deployment

### Local Development
```bash
python start_manvue.py
```

### Production Deployment
1. Set up MongoDB Atlas
2. Configure environment variables
3. Deploy backend to cloud platform
4. Deploy frontend to CDN
5. Set up ML model serving

## 📝 Next Steps

This platform provides a solid foundation for:
- **E-commerce**: Complete shopping experience
- **AI Integration**: Advanced search and recommendations
- **Scalability**: Ready for production deployment
- **Customization**: Easy to extend and modify

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.