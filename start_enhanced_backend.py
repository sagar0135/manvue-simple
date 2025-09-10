#!/usr/bin/env python3
"""
Start Enhanced ManVue Backend with MongoDB
Automatically starts the enhanced backend server with full MongoDB integration
"""

import os
import sys
import subprocess
import time
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'fastapi',
        'uvicorn', 
        'motor',
        'pymongo',
        'python-dotenv',
        'pillow',
        'requests',
        'pydantic'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        logger.error(f"❌ Missing required packages: {', '.join(missing_packages)}")
        logger.info("Install missing packages with:")
        logger.info(f"pip install {' '.join(missing_packages)}")
        return False
    
    logger.info("✅ All required packages are installed")
    return True

def check_mongodb():
    """Check if MongoDB is running"""
    try:
        import pymongo
        # Try to connect to MongoDB
        client = pymongo.MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=3000)
        client.server_info()  # Force connection
        logger.info("✅ MongoDB is running and accessible")
        return True
    except Exception as e:
        logger.warning(f"⚠️ MongoDB connection failed: {e}")
        logger.info("💡 Make sure MongoDB is installed and running:")
        logger.info("   - Windows: Start MongoDB service")
        logger.info("   - macOS: brew services start mongodb/brew/mongodb-community")
        logger.info("   - Linux: sudo systemctl start mongod")
        logger.info("   - Or use MongoDB Atlas (cloud)")
        return False

def setup_environment():
    """Setup environment variables"""
    env_file = Path(".env")
    
    if not env_file.exists():
        logger.info("📝 Creating .env file with default settings...")
        env_content = """# ManVue Enhanced Backend Configuration
MONGO_URI=mongodb://localhost:27017
DB_NAME=manvue_db
PORT=5001
LOG_LEVEL=info

# Optional: MongoDB Atlas connection (uncomment and update)
# MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/
"""
        env_file.write_text(env_content)
        logger.info("✅ Created .env file with default MongoDB configuration")
    else:
        logger.info("✅ .env file already exists")

def start_server():
    """Start the enhanced backend server"""
    backend_dir = Path("backend")
    
    if not backend_dir.exists():
        logger.error("❌ Backend directory not found!")
        return False
    
    # Check for new API structure first
    api_dir = Path("api")
    api_main = api_dir / "main.py"
    
    if api_main.exists():
        logger.info("✅ Using new organized API structure")
        # Change to api directory
        os.chdir(api_dir)
        main_module = "main:app"
    else:
        # Fallback to old structure
        enhanced_main = backend_dir / "enhanced_main.py"
        
        if not enhanced_main.exists():
            logger.error("❌ Neither api/main.py nor backend/enhanced_main.py found!")
            return False
        
        logger.info("⚠️ Using legacy backend structure")
        # Change to backend directory
        os.chdir(backend_dir)
        main_module = "enhanced_main:app"
    
    logger.info("🚀 Starting ManVue Enhanced Backend Server...")
    logger.info("📡 Server will be available at: http://localhost:5001")
    logger.info("📚 API Documentation: http://localhost:5001/docs")
    logger.info("🔄 RedDoc Documentation: http://localhost:5001/redoc")
    logger.info("")
    logger.info("Press Ctrl+C to stop the server")
    logger.info("=" * 60)
    
    try:
        # Start the server
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            main_module,
            "--host", "0.0.0.0",
            "--port", "5001",
            "--reload",
            "--log-level", "info"
        ])
    except KeyboardInterrupt:
        logger.info("\n🛑 Server stopped by user")
    except Exception as e:
        logger.error(f"❌ Server error: {e}")
        return False
    
    return True

def main():
    """Main function"""
    print("=" * 60)
    print("🏪 ManVue Enhanced Backend Starter")
    print("Full-featured backend with MongoDB & Image Storage")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check MongoDB
    mongodb_running = check_mongodb()
    if not mongodb_running:
        response = input("\nMongoDB is not running. Continue anyway? (y/N): ")
        if response.lower() != 'y':
            logger.info("💡 Please start MongoDB and try again")
            sys.exit(1)
    
    # Setup environment
    setup_environment()
    
    # Start server
    logger.info("\n🎯 All checks passed! Starting server...")
    time.sleep(1)
    
    success = start_server()
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()