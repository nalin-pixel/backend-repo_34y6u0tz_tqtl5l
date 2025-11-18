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
from typing import Optional

# Existing example schemas (kept for reference)
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

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Application-specific schemas
# --------------------------------------------------
class Note(BaseModel):
    """
    Shared notes for students
    Collection name: "note"
    """
    title: str = Field(..., description="Short title for the note")
    content: str = Field(..., description="Note content or summary")
    subject: Optional[str] = Field(None, description="Subject e.g. Math, Science")
    grade: Optional[str] = Field(None, description="Grade or class level e.g. Class 6")
    author: Optional[str] = Field(None, description="Name of the student or teacher who shared it")

class Message(BaseModel):
    """
    Messages sent to volunteer teachers
    Collection name: "message"
    """
    name: str = Field(..., description="Sender name")
    contact: Optional[str] = Field(None, description="How to reach back (phone/email)")
    subject: Optional[str] = Field(None, description="Topic or subject of the help needed")
    body: str = Field(..., description="Message content for the teacher")
    grade: Optional[str] = Field(None, description="Student's grade or class level")
    school: Optional[str] = Field(None, description="School name (optional)")

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
