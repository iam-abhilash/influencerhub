from pydantic import BaseModel, EmailStr, Field, HttpUrl
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    BRAND = "brand"
    INFLUENCER = "influencer"

# Shared properties
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    role: UserRole

class UserResponse(UserBase):
    id: UUID
    role: UserRole
    created_at: datetime
    
    class Config:
        from_attributes = True

# --- Brand Schemas ---
class BrandBase(BaseModel):
    company_name: str = Field(..., min_length=2, max_length=100)
    industry: str
    website: Optional[HttpUrl] = None

class BrandCreate(BrandBase):
    pass

class BrandUpdate(BrandBase):
    company_name: Optional[str] = None
    industry: Optional[str] = None
    
class BrandResponse(BrandBase):
    user_id: UUID
    verified: bool

# --- Influencer Schemas ---
class InfluencerBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=30)
    bio: Optional[str] = Field(None, max_length=500)
    niche: List[str] = []
    wallet_address: Optional[str] = Field(None, pattern="^0x[a-fA-F0-9]{40}$")

class InfluencerCreate(InfluencerBase):
    pass

class InfluencerUpdate(InfluencerBase):
    metrics: Optional[Dict[str, Any]] = None

class InfluencerResponse(InfluencerBase):
    user_id: UUID
    metrics: Dict[str, Any] = {}
