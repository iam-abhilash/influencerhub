from sqlalchemy import Boolean, Column, String, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import uuid
from app.models.base import Base
from app.schemas.user import UserRole

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.INFLUENCER, nullable=False)
    
    # 1-to-1 relationships
    brand_profile = relationship("Brand", back_populates="user", uselist=False)
    influencer_profile = relationship("Influencer", back_populates="user", uselist=False)

class Brand(Base):
    __tablename__ = "brands"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    company_name = Column(String, nullable=False)
    industry = Column(String)
    website = Column(String)
    verified = Column(Boolean, default=False)

    user = relationship("User", back_populates="brand_profile")
    campaigns = relationship("Campaign", back_populates="brand")

class Influencer(Base):
    __tablename__ = "influencers"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    username = Column(String, nullable=False)
    bio = Column(String)
    niche = Column(JSONB) # Stored as JSON array ["tech", "ai"]
    metrics = Column(JSONB, default={}) 
    wallet_address = Column(String)

    user = relationship("User", back_populates="influencer_profile")
