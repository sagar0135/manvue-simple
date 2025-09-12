"""
Authentication API Routes
Handles user registration, login, and authentication
"""

from fastapi import APIRouter, HTTPException
import logging

# Import our models and services
from ..models.auth_models import User, UserResponse, LoginResponse, RegisterRequest, LoginRequest
from ..services.auth_service import AuthService

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/auth", tags=["Authentication"])

# Initialize auth service
auth_service = AuthService()

@router.post("/register", response_model=UserResponse)
async def register(request: RegisterRequest):
    """Register a new user"""
    try:
        # Check if user already exists
        existing_user = await auth_service.get_user_by_email(request.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Create user
        user = await auth_service.create_user(request.dict())
        return user
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error registering user: {e}")
        raise HTTPException(status_code=500, detail="Registration failed")

@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """Login user"""
    try:
        # Authenticate user
        user = await auth_service.authenticate_user(request.email, request.password)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Create access token
        token = auth_service.create_access_token(user["email"])
        
        return LoginResponse(
            access_token=token,
            token_type="bearer",
            user=UserResponse(
                id=user["_id"],
                email=user["email"],
                name=user.get("name"),
                created_at=user["created_at"].isoformat()
            )
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error logging in user: {e}")
        raise HTTPException(status_code=500, detail="Login failed")

@router.get("/me", response_model=UserResponse)
async def get_current_user(token: str):
    """Get current user information"""
    try:
        # Verify token and get user
        user = await auth_service.get_user_from_token(token)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        return UserResponse(
            id=user["_id"],
            email=user["email"],
            name=user.get("name"),
            created_at=user["created_at"].isoformat()
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting current user: {e}")
        raise HTTPException(status_code=500, detail="Failed to get user information")

@router.post("/logout")
async def logout():
    """Logout user (client-side token removal)"""
    return {"message": "Successfully logged out"}

@router.post("/refresh")
async def refresh_token(token: str):
    """Refresh access token"""
    try:
        # Verify current token and create new one
        user = await auth_service.get_user_from_token(token)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        new_token = auth_service.create_access_token(user["email"])
        
        return {
            "access_token": new_token,
            "token_type": "bearer"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error refreshing token: {e}")
        raise HTTPException(status_code=500, detail="Token refresh failed")
