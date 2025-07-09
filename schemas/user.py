from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# Base fields shared by all user schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    medical_history: Optional[List[str]] = []
    allergies: Optional[List[str]] = []
    medications: Optional[List[str]] = []

# For user registration
class UserCreate(UserBase):
    password: str  # plain password, not hashed

# For login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# For returning user data in API responses (without password)
class UserResponse(UserBase):
    id: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True  # enables reading from ORM or Mongo-like objects
        schema_extra = {
            "example": {
                "id": "507f1f77bcf86cd799439011",
                "email": "user@example.com",
                "username": "johndoe",
                "full_name": "John Doe",
                "age": 30,
                "gender": "male",
                "weight": 70.5,
                "height": 175.0,
                "medical_history": ["diabetes", "hypertension"],
                "allergies": ["penicillin"],
                "medications": ["metformin", "lisinopril"],
                "is_active": True,
                "is_verified": False,
                "created_at": "2025-07-09T12:00:00Z",
                "updated_at": "2025-07-09T12:00:00Z"
            }
        }

# For updating user profile
class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    medical_history: Optional[List[str]] = None
    allergies: Optional[List[str]] = None
    medications: Optional[List[str]] = None
