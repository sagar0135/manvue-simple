# MANVUE - Men's Fashion Store

A modern, feature-rich e-commerce platform for men's fashion with AI-powered recommendations and advanced shopping features.

## Project Structure

```
manvue-simple/
├── frontend/                 # Frontend application
│   ├── index.html           # Main HTML file
│   ├── css/                 # Stylesheets
│   │   └── style.css
│   ├── js/                  # JavaScript files
│   │   └── script.js
│   ├── data/                # Product data files
│   │   ├── products.js      # Main products file
│   │   ├── tshirts.js       # T-shirts data (12+ products)
│   │   ├── shirts.js        # Shirts data (12+ products)
│   │   ├── bottoms.js       # Bottoms data (12+ products)
│   │   ├── jackets.js       # Jackets data (12+ products)
│   │   └── accessories.js   # Accessories data (12+ products)
│   └── assets/              # Images and other assets
└── backend/                 # Backend services
    └── ML/                  # Machine Learning components
        ├── api/             # ML API server
        ├── models/          # Trained models
        ├── data/            # Training data
        ├── notebooks/       # Jupyter notebooks
        └── utils/           # ML utilities

```

## Features

### Frontend Features
- **Responsive Design**: Mobile-first approach with desktop optimization
- **Product Categories**: T-shirts, Shirts, Bottoms, Jackets, Accessories
- **Advanced Filtering**: By category, price, brand, size, color
- **Shopping Cart**: Add/remove items, quantity management
- **Wishlist**: Save favorite products
- **User Authentication**: Login/register system
- **Home Button**: MANVUE logo acts as home navigation
- **Payment Methods**: Visa, MasterCard, PayPal integration
- **Social Media**: Facebook, Instagram, Pinterest, YouTube, Twitter, LinkedIn

### Backend Features
- **AI-Powered Recommendations**: Machine learning for personalized suggestions
- **Visual Search**: Image recognition for product matching
- **Style Quiz**: Personalized style assessment
- **3D Virtual Try-On**: Advanced visualization
- **Voice Commands**: Hands-free navigation
- **Real-time Chat**: AI assistant for customer support

### Product Data
Each category contains 12+ products with:
- Detailed descriptions
- Multiple color options
- Size availability
- Customer ratings and reviews
- High-quality product images
- Brand information
- Pricing and discounts

## Getting Started

1. **Frontend Development**:
   ```bash
   cd frontend
   # Open index.html in a web browser or use a local server
   python -m http.server 8000  # Python server
   # OR
   npx serve .  # Node.js serve
   ```

2. **Backend Services**:
   ```bash
   cd backend/ML
   pip install -r requirements.txt
   python start_ml_server.py
   ```

## File Organization Benefits

### Frontend (/frontend)
- **Separation of Concerns**: HTML, CSS, JS, and data are organized separately
- **Modular Product Data**: Each category has its own file for easy maintenance
- **Scalability**: Easy to add new categories or products
- **Development Efficiency**: Clear structure for team collaboration

### Backend (/backend)
- **ML Services**: Isolated machine learning components
- **API Architecture**: RESTful API design
- **Data Management**: Organized training data and models
- **Microservices Ready**: Easy to scale individual components

## Key Improvements Made

1. **Project Structure**: Separated frontend and backend for better organization
2. **Product Data**: Created separate files for each category with 10+ products each
3. **Navigation**: Made MANVUE logo a clickable home button
4. **Payment Methods**: Added visual representations of Visa, MasterCard, and PayPal
5. **Social Media**: Enhanced footer with proper social media links
6. **File References**: Updated all paths to match new structure

## Technologies Used

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Backend**: Python, Flask/FastAPI
- **ML**: TensorFlow, scikit-learn, OpenCV
- **3D Graphics**: Three.js
- **Responsive**: CSS Grid, Flexbox
- **Icons**: Unicode emojis, SVG icons

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes in the appropriate frontend or backend directory
4. Test thoroughly
5. Submit a pull request

## License

© 2025 MANVUE. All rights reserved.