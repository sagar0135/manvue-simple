"""
Authentication Service
Business logic for user authentication and authorization
"""

import hashlib
import secrets
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

# Import database functions
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from backend.database import (
    create_user as db_create_user, get_user_by_email as db_get_user_by_email,
    update_user as db_update_user
)

from ..models.auth_models import UserResponse

# Configure logging
logger = logging.getLogger(__name__)

class AuthService:
    """Service for handling authentication operations"""
    
    def __init__(self):
        self.token_expiry_hours = 24
        self.secret_key = "your-secret-key"  # This should come from environment variables
    
    def _hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password"""
        return self._hash_password(plain_password) == hashed_password
    
    def create_access_token(self, user_email: str) -> str:
        """
        Create a simple access token
        
        Args:
            user_email: User's email address
            
        Returns:
            str: Access token
        """
        # In a real application, you'd use JWT with proper signing
        # For simplicity, we're using a URL-safe token
        return secrets.token_urlsafe(32)
    
    async def create_user(self, user_data: Dict[str, Any]) -> UserResponse:
        """
        Create a new user
        
        Args:
            user_data: User registration data
            
        Returns:
            UserResponse for created user
        """
        try:
            # Hash the password
            hashed_password = self._hash_password(user_data["password"])
            
            # Prepare user data for database
            db_user_data = {
                "email": user_data["email"],
                "password": hashed_password,
                "name": user_data.get("name")
            }
            
            # Create user in database
            user_id = await db_create_user(db_user_data)
            
            return UserResponse(
                id=user_id,
                email=user_data["email"],
                name=user_data.get("name"),
                created_at=datetime.now().isoformat()
            )
        
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            raise
    
    async def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Get user by email address
        
        Args:
            email: User's email address
            
        Returns:
            User data or None if not found
        """
        try:
            return await db_get_user_by_email(email)
        
        except Exception as e:
            logger.error(f"Error getting user by email {email}: {e}")
            raise
    
    async def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Authenticate user with email and password
        
        Args:
            email: User's email address
            password: Plain text password
            
        Returns:
            User data if authentication successful, None otherwise
        """
        try:
            user = await self.get_user_by_email(email)
            if not user:
                return None
            
            if not self._verify_password(password, user["password"]):
                return None
            
            return user
        
        except Exception as e:
            logger.error(f"Error authenticating user {email}: {e}")
            raise
    
    async def get_user_from_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Get user from access token
        
        Args:
            token: Access token
            
        Returns:
            User data if token is valid, None otherwise
        """
        try:
            # In a real application, you'd decode and verify JWT token
            # For this simple implementation, we'll just validate token format
            if not token or len(token) < 10:
                return None
            
            # For demo purposes, return a mock user
            # In reality, you'd store token-user mapping in database or decode JWT
            return None  # This needs proper implementation with token storage
        
        except Exception as e:
            logger.error(f"Error getting user from token: {e}")
            return None
    
    async def update_user_profile(
        self, 
        user_id: str, 
        update_data: Dict[str, Any]
    ) -> bool:
        """
        Update user profile
        
        Args:
            user_id: User ID
            update_data: Data to update
            
        Returns:
            bool: True if successful
        """
        try:
            # Remove sensitive fields that shouldn't be updated directly
            safe_update_data = {
                k: v for k, v in update_data.items() 
                if k not in ["password", "_id", "created_at"]
            }
            
            return await db_update_user(user_id, safe_update_data)
        
        except Exception as e:
            logger.error(f"Error updating user profile {user_id}: {e}")
            raise
    
    async def change_password(
        self, 
        user_id: str, 
        current_password: str, 
        new_password: str
    ) -> bool:
        """
        Change user password
        
        Args:
            user_id: User ID
            current_password: Current password (for verification)
            new_password: New password
            
        Returns:
            bool: True if successful
        """
        try:
            # Get user to verify current password
            user = await db_get_user_by_email("")  # This needs proper user lookup by ID
            if not user:
                return False
            
            # Verify current password
            if not self._verify_password(current_password, user["password"]):
                return False
            
            # Hash new password and update
            hashed_new_password = self._hash_password(new_password)
            return await db_update_user(user_id, {"password": hashed_new_password})
        
        except Exception as e:
            logger.error(f"Error changing password for user {user_id}: {e}")
            raise
    
    def validate_token_format(self, token: str) -> bool:
        """
        Validate token format
        
        Args:
            token: Access token
            
        Returns:
            bool: True if format is valid
        """
        return bool(token and len(token) >= 10 and token.replace("-", "").replace("_", "").isalnum())
