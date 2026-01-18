from pydantic import BaseModel, Field, condecimal
from typing import Optional
from uuid import UUID
from datetime import datetime
from enum import Enum

class CampaignStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class CampaignBase(BaseModel):
    title: str = Field(..., min_length=5, max_length=100)
    description: Optional[str] = None
    budget: float = Field(..., gt=0)

class CampaignCreate(CampaignBase):
    pass

class CampaignUpdate(CampaignBase):
    title: Optional[str] = None
    budget: Optional[float] = None
    status: Optional[CampaignStatus] = None

class CampaignResponse(CampaignBase):
    id: UUID
    brand_id: UUID
    status: CampaignStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
