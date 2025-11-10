"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field
from typing import Optional, List

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class ProductRetailer(BaseModel):
    name: str
    price: float
    url: Optional[str] = None
    is_best: bool = False

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    image: Optional[str] = Field(None, description="Product image URL")
    rating: Optional[float] = Field(None, ge=0, le=5, description="Average rating out of 5")
    specs: Optional[List[str]] = Field(default_factory=list, description="Key specifications")
    retailers: Optional[List[ProductRetailer]] = Field(default_factory=list, description="Retailer options")
    in_stock: bool = Field(True, description="Whether product is in stock")

class Message(BaseModel):
    role: str = Field(..., description="user or assistant")
    content: str
    conversation_id: Optional[str] = None
    related_product_id: Optional[str] = None

class Conversation(BaseModel):
    title: str
    user_id: Optional[str] = None
    last_message_preview: Optional[str] = None

class TrendItem(BaseModel):
    title: str
    category: str
    product_id: Optional[str] = None

# Add your own schemas here:
# --------------------------------------------------

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
