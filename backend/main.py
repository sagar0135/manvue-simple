#!/usr/bin/env python3
"""
ManVue Enhanced API - Main Application
Organized API structure with MongoDB and ML integration
"""

import os
import sys
import uvicorn
import logging
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Add parent directories to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

# Import configuration
from core.config import get_settings, get_environment_settings

# Import routers
from routes import images, products, auth, ml

# Import database connection test
try:
    from backend.database import test_connection
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False
    logging.warning("Database module not available")

# Get settings
settings = get_environment_settings()

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    docs_url=settings.docs_url,
    redoc_url=settings.redoc_url,
    debug=settings.debug
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=settings.allowed_methods,
    allow_headers=settings.allowed_headers,
)

# Application state
app_start_time = datetime.now()

# Include routers
app.include_router(images.router, prefix="/api")
app.include_router(products.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(ml.router, prefix="/api")

# Root endpoints
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "description": settings.app_description,
        "docs_url": f"{settings.api_base_url}{settings.docs_url}",
        "redoc_url": f"{settings.api_base_url}{settings.redoc_url}",
        "features": [
            "MongoDB Integration",
            "GridFS Image Storage", 
            "ML-Powered Fashion Recognition",
            "RESTful API Design",
            "Automatic Documentation"
        ],
        "endpoints": {
            "images": f"{settings.api_base_url}/api/images",
            "products": f"{settings.api_base_url}/api/products", 
            "auth": f"{settings.api_base_url}/api/auth",
            "ml": f"{settings.api_base_url}/api/ml"
        }
    }

@app.get("/health")
async def health_check():
    """Enhanced health check with service status"""
    try:
        # Check database connection
        db_connected = False
        if DATABASE_AVAILABLE:
            try:
                db_connected = await test_connection()
            except Exception as e:
                logger.warning(f"Database health check failed: {e}")
        
        # Check ML service availability
        try:
            from services.ml_service import MLService
            ml_service = MLService()
            ml_available = ml_service.is_available()
        except Exception as e:
            logger.warning(f"ML service check failed: {e}")
            ml_available = False
        
        # Calculate uptime
        uptime = str(datetime.now() - app_start_time)
        
        # Determine overall status
        overall_status = "healthy"
        if not db_connected:
            overall_status = "degraded"
        if not db_connected and not DATABASE_AVAILABLE:
            overall_status = "unhealthy"
        
        return {
            "status": overall_status,
            "timestamp": datetime.now().isoformat(),
            "uptime": uptime,
            "version": settings.app_version,
            "services": {
                "database": {
                    "status": "connected" if db_connected else "disconnected",
                    "available": DATABASE_AVAILABLE
                },
                "ml": {
                    "status": "available" if ml_available else "unavailable",
                    "enabled": settings.ml_enabled
                }
            },
            "environment": {
                "debug": settings.debug,
                "log_level": settings.log_level
            }
        }
    
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "error",
                "message": f"Health check failed: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
        )

@app.get("/api/info")
async def api_info():
    """API information and available endpoints"""
    return {
        "api_name": settings.app_name,
        "version": settings.app_version,
        "description": settings.app_description,
        "endpoints": {
            "images": {
                "upload": "POST /api/images/upload",
                "upload_base64": "POST /api/images/upload-base64", 
                "get": "GET /api/images/{file_id}",
                "metadata": "GET /api/images/{file_id}/metadata",
                "list": "GET /api/images",
                "delete": "DELETE /api/images/{file_id}"
            },
            "products": {
                "list": "GET /api/products",
                "get": "GET /api/products/{product_id}",
                "create": "POST /api/products",
                "update": "PUT /api/products/{product_id}",
                "delete": "DELETE /api/products/{product_id}",
                "search": "GET /api/products/search/text",
                "by_category": "GET /api/products/category/{category}",
                "featured": "GET /api/products/featured/trending"
            },
            "auth": {
                "register": "POST /api/auth/register",
                "login": "POST /api/auth/login",
                "me": "GET /api/auth/me",
                "logout": "POST /api/auth/logout",
                "refresh": "POST /api/auth/refresh"
            },
            "ml": {
                "predict": "POST /api/ml/predict",
                "similarity": "POST /api/ml/similarity",
                "status": "GET /api/ml/status",
                "colors": "POST /api/ml/analyze-colors",
                "categorize": "POST /api/ml/categorize",
                "categories": "GET /api/ml/categories"
            }
        },
        "documentation": {
            "swagger": f"{settings.api_base_url}{settings.docs_url}",
            "redoc": f"{settings.api_base_url}{settings.redoc_url}"
        }
    }

# Exception handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Custom 404 handler"""
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "message": f"The requested endpoint {request.url.path} was not found",
            "suggestions": [
                f"Check the API documentation at {settings.docs_url}",
                "Verify the endpoint URL is correct",
                "Make sure you're using the correct HTTP method"
            ]
        }
    )

@app.exception_handler(500)
async def server_error_handler(request, exc):
    """Custom 500 handler"""
    logger.error(f"Internal server error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            "timestamp": datetime.now().isoformat()
        }
    )

# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Initialize the application on startup"""
    logger.info(f"🚀 Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"🌐 Server will be available at: {settings.api_base_url}")
    logger.info(f"📚 API Documentation: {settings.api_base_url}{settings.docs_url}")
    logger.info(f"🔄 RedDoc Documentation: {settings.api_base_url}{settings.redoc_url}")
    
    # Test database connection
    if DATABASE_AVAILABLE:
        try:
            db_connected = await test_connection()
            if db_connected:
                logger.info("✅ Database connection established")
            else:
                logger.warning("⚠️ Database connection failed - some features may not work")
        except Exception as e:
            logger.error(f"❌ Database connection error: {e}")
    else:
        logger.warning("⚠️ Database module not available")
    
    # Check ML service
    try:
        from services.ml_service import MLService
        ml_service = MLService()
        if ml_service.is_available():
            logger.info("✅ ML services available")
        else:
            logger.warning("⚠️ ML services not available")
    except Exception as e:
        logger.warning(f"⚠️ ML service check failed: {e}")
    
    logger.info("=" * 60)
    logger.info("🎯 ManVue Enhanced API Server started successfully!")
    logger.info("=" * 60)

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("🛑 Shutting down ManVue Enhanced API Server...")
    logger.info("👋 Goodbye!")

# Main execution
if __name__ == "__main__":
    # Start server with uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level.lower(),
        access_log=True
    )
