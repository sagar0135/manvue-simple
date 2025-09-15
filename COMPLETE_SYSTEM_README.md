# 🛍️ ManVue Complete E-Commerce System

A comprehensive e-commerce platform with AI-powered chatbot, voice commands, product management, user authentication, and payment processing.

## 🚀 Features

### 🛒 **E-Commerce Core**
- **Auto-Generated Product Pages**: Dynamic HTML generation with responsive design
- **Shopping Cart System**: Add/remove items, quantity management, persistent storage
- **Wishlist Functionality**: Save favorite items for later
- **Product Search & Filtering**: Advanced search with category, price, and color filters
- **Responsive Design**: Mobile-first approach with beautiful UI/UX

### 🤖 **AI Chatbot Integration**
- **Voice Recognition**: Speak to search and interact with products
- **Product Recommendations**: AI-powered suggestions based on user preferences
- **Natural Language Processing**: Understand complex queries and commands
- **Real-time Product Display**: Show products directly in chat interface
- **Cart Integration**: Add items to cart through voice commands

### 🔐 **User Authentication & Security**
- **User Registration/Login**: Secure account creation and management
- **MongoDB Integration**: Persistent user data storage
- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: SHA-256 encryption for user passwords
- **Session Management**: Secure user sessions

### 💳 **Payment Processing**
- **Stripe Integration**: Secure payment processing
- **Multiple Payment Methods**: Credit/debit cards support
- **Order Management**: Complete order tracking and history
- **Payment Security**: PCI-compliant payment handling
- **Order Confirmation**: Email notifications and order tracking

### 🎤 **Voice Commands**
- **Hands-Free Shopping**: Voice-activated product search
- **Voice Navigation**: Navigate through categories and products
- **Voice Cart Management**: Add/remove items using voice commands
- **Accessibility**: Enhanced accessibility for all users

## 📁 Project Structure

```
manvue-simple/
├── api/                          # Backend API Services
│   ├── auth_payment_api.py      # Authentication & Payment API
│   └── requirements.txt         # Python dependencies
├── chatbot/                      # AI Chatbot System
│   ├── chatbot_server.py        # FastAPI chatbot server
│   ├── enhanced_chatbot_integration.js  # Frontend chatbot
│   └── frontend/                # Chatbot UI components
├── frontend/                     # Main Website
│   ├── products/                # Auto-generated product pages
│   ├── css/                     # Stylesheets
│   │   ├── style.css           # Main styles
│   │   └── cart-checkout.css   # Cart & checkout styles
│   ├── js/                      # JavaScript modules
│   │   ├── script.js           # Main frontend logic
│   │   └── cart-system.js      # Cart & checkout system
│   ├── data/                    # Product data
│   │   └── sample_products.json # Product database
│   └── index.html              # Main homepage
├── product_generator.py         # Auto-generates product HTML
├── start_manvue_system.py      # Complete system startup
└── .env                        # Environment configuration
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js (for frontend development)
- MongoDB (local or cloud)
- Stripe account (for payments)

### 1. Clone and Setup
```bash
git clone <repository-url>
cd manvue-simple
```

### 2. Install Dependencies
```bash
# Install Python dependencies
pip install -r api/requirements.txt

# Install additional packages
pip install fastapi uvicorn pymongo stripe python-dotenv
```

### 3. Environment Configuration
Create a `.env` file in the root directory:
```env
# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017

# JWT Configuration
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production

# Stripe Configuration
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key_here
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key_here

# API Configuration
API_HOST=0.0.0.0
API_PORT=8001
CHATBOT_PORT=5055
FRONTEND_PORT=3000
```

### 4. Generate Product Pages
```bash
python product_generator.py
```

### 5. Start the Complete System
```bash
python start_manvue_system.py
```

## 🎯 Usage Guide

### For Customers

#### 🛒 **Shopping Experience**
1. **Browse Products**: Use the main website or voice commands
2. **Search**: Type or speak your search queries
3. **View Details**: Click on products for detailed information
4. **Add to Cart**: Use buttons or voice commands
5. **Checkout**: Secure payment through Stripe

#### 🎤 **Voice Commands**
- "Search for blue shirts"
- "Show me jackets under £100"
- "Add this to my cart"
- "What's in my wishlist?"
- "Help me find formal wear"

#### 🤖 **Chatbot Interaction**
- Click the chatbot icon to open
- Ask questions about products, sizing, shipping
- Get personalized recommendations
- Voice-enabled interaction

### For Developers

#### 🔧 **API Endpoints**

**Authentication:**
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user

**Products:**
- `GET /api/products` - Get all products
- `GET /api/products/{id}` - Get specific product
- `GET /api/products/search?q={query}` - Search products

**Cart & Orders:**
- `POST /api/cart/add` - Add item to cart
- `GET /api/cart` - Get user's cart
- `POST /api/orders` - Create order
- `GET /api/orders` - Get user's orders

**Payments:**
- `POST /api/payment/process` - Process payment
- `POST /api/payment/confirm/{id}` - Confirm payment

#### 🛠️ **Customization**

**Adding New Products:**
1. Add product data to `frontend/data/sample_products.json`
2. Run `python product_generator.py`
3. Product pages will be auto-generated

**Customizing Chatbot:**
1. Modify `chatbot/chatbot_server.py` for backend logic
2. Update `chatbot/enhanced_chatbot_integration.js` for frontend
3. Add new voice commands in the voice processing functions

**Styling:**
1. Main styles: `frontend/css/style.css`
2. Cart/checkout: `frontend/css/cart-checkout.css`
3. Product pages: Auto-generated with responsive design

## 🔧 Technical Details

### **Backend Architecture**
- **FastAPI**: High-performance web framework
- **MongoDB**: NoSQL database for user data and orders
- **Stripe**: Payment processing and subscription management
- **JWT**: Secure authentication tokens
- **WebSockets**: Real-time chatbot communication

### **Frontend Architecture**
- **Vanilla JavaScript**: No framework dependencies
- **Responsive CSS**: Mobile-first design approach
- **Web Speech API**: Voice recognition and synthesis
- **Local Storage**: Cart and wishlist persistence
- **Fetch API**: Modern HTTP client for API calls

### **Security Features**
- **Password Hashing**: SHA-256 encryption
- **JWT Tokens**: Secure session management
- **CORS Protection**: Cross-origin request security
- **Input Validation**: Pydantic models for data validation
- **HTTPS Ready**: SSL/TLS encryption support

## 🚀 Deployment

### **Production Setup**
1. **Environment Variables**: Set production values in `.env`
2. **Database**: Use MongoDB Atlas or production MongoDB
3. **Stripe**: Switch to live API keys
4. **HTTPS**: Configure SSL certificates
5. **Domain**: Set up custom domain and DNS

### **Docker Deployment** (Optional)
```dockerfile
# Dockerfile example
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8001
CMD ["python", "start_manvue_system.py"]
```

## 📊 Performance Features

- **Lazy Loading**: Images and content load on demand
- **Caching**: Local storage for cart and user data
- **Optimized Images**: Responsive image sizing
- **Minified Assets**: Compressed CSS and JavaScript
- **CDN Ready**: Static asset delivery optimization

## 🔍 Testing

### **Manual Testing**
1. **Product Search**: Test various search queries
2. **Cart Functionality**: Add/remove items, quantity changes
3. **User Registration**: Create accounts and login
4. **Payment Flow**: Test with Stripe test cards
5. **Voice Commands**: Test voice recognition features
6. **Chatbot**: Test AI responses and product recommendations

### **Test Cards (Stripe)**
- **Success**: 4242 4242 4242 4242
- **Decline**: 4000 0000 0000 0002
- **3D Secure**: 4000 0025 0000 3155

## 🐛 Troubleshooting

### **Common Issues**

**MongoDB Connection:**
```bash
# Start MongoDB locally
mongod --dbpath /path/to/your/db
```

**Port Conflicts:**
```bash
# Check port usage
netstat -an | grep :8001
# Kill process if needed
kill -9 <PID>
```

**Voice Recognition:**
- Ensure HTTPS or localhost
- Check microphone permissions
- Use supported browsers (Chrome, Edge)

**Payment Issues:**
- Verify Stripe API keys
- Check webhook endpoints
- Test with Stripe test cards

## 📈 Future Enhancements

- **Machine Learning**: Advanced product recommendations
- **AR Try-On**: Virtual fitting room
- **Multi-language**: Internationalization support
- **Mobile App**: React Native or Flutter app
- **Analytics**: User behavior tracking
- **Inventory Management**: Real-time stock updates
- **Social Features**: User reviews and ratings
- **Loyalty Program**: Points and rewards system

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the troubleshooting section
- Review the API documentation at `/docs`

---

**🎉 Enjoy your ManVue shopping experience!**
