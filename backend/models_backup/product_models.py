"""
Product-related Pydantic models
"""

from pydantic import BaseModel, Field
from typing import List, Optional

class ProductCreateRequest(BaseModel):
    name: str
    title: Optional[str] = None
    price: float
    originalPrice: Optional[float] = None
    category: str
    type: str
    size: List[str] = []
    color: List[str] = []
    brand: Optional[str] = None
    rating: Optional[float] = 4.5
    reviews: Optional[int] = 0
    image_ids: List[str] = []  # GridFS image IDs
    image_urls: List[str] = []  # External image URLs (fallback)
    tags: List[str] = []
    inStock: bool = True
    description: Optional[str] = None
    features: List[str] = []

class Product(ProductCreateRequest):
    """Product model for internal use"""
    pass

class ProductResponse(BaseModel):
    id: str
    name: str
    title: Optional[str] = None
    price: float
    originalPrice: Optional[float] = None
    category: str
    type: str
    size: List[str] = []
    color: List[str] = []
    brand: Optional[str] = None
    rating: Optional[float] = 4.5
    reviews: Optional[int] = 0
    image_ids: List[str] = []
    image_urls: List[str] = []
    image: Optional[str] = None  # Primary image URL for backward compatibility
    tags: List[str] = []
    inStock: bool = True
    description: Optional[str] = None
    features: List[str] = []
    created_at: str
    updated_at: str

class ProductSearchRequest(BaseModel):
    query: str = Field(..., description="Search query")
    category: Optional[str] = Field(None, description="Filter by category")
    limit: int = Field(20, ge=1, le=100, description="Maximum number of results")
    min_price: Optional[float] = Field(None, ge=0, description="Minimum price filter")
    max_price: Optional[float] = Field(None, ge=0, description="Maximum price filter")
    brand: Optional[str] = Field(None, description="Filter by brand")
    in_stock_only: bool = Field(True, description="Show only in-stock products")

class ProductFilterRequest(BaseModel):
    category: Optional[str] = None
    type: Optional[str] = None
    brand: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    sizes: List[str] = []
    colors: List[str] = []
    tags: List[str] = []
    in_stock_only: bool = True
    sort_by: str = "name"  # name, price, rating, created_at
    sort_order: str = "asc"  # asc, desc
    limit: int = Field(50, ge=1, le=100)
    skip: int = Field(0, ge=0)
