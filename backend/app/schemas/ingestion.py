from pydantic import BaseModel, HttpUrl, Field, field_validator
from typing import Optional, List, Dict, Any
from enum import Enum

class Platform(str, Enum):
    INSTAGRAM = "instagram"
    YOUTUBE = "youtube"
    LINKEDIN = "linkedin"

class IngestionSource(str, Enum):
    MANUAL_CSV = "manual_csv"
    API_SYNC = "api_sync"
    SELF_REPORTED = "self_reported"

class NormalizedInfluencerData(BaseModel):
    """
    Unified schema after processing raw data from any source.
    """
    username: str
    platform: Platform
    platform_id: str  # External ID (e.g., YouTube Channel ID)
    display_name: Optional[str] = None
    follower_count: int = Field(0, GE=0)
    engagement_rate: Optional[float] = None # 0.0 to 1.0 (e.g. 0.05 = 5%)
    profile_url: HttpUrl
    tags: List[str] = []
    
    # Raw metrics snapshot for historical tracking
    raw_metrics_snapshot: Dict[str, Any] = {}

class CSVIngestionRow(BaseModel):
    """
    Schema for validating MVP CSV uploads.
    """
    handle: str
    platform: Platform
    followers: int
    url: HttpUrl
    niche_tags: str # Comma separated
    
    @field_validator('niche_tags')
    def split_tags(cls, v):
        if isinstance(v, str):
            return [t.strip() for t in v.split(',')]
        return v
