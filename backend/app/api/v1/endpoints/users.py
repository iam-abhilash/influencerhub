from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.core.database import get_db
from app.models.user import User, Brand, Influencer
from app.schemas import user as user_schema
from typing import Any

router = APIRouter()

@router.post("/onboard/brand", response_model=user_schema.BrandResponse)
def onboard_brand(
    *,
    db: Session = Depends(get_db),
    brand_in: user_schema.BrandCreate,
    current_user: deps.TokenData = Depends(deps.get_current_user)
) -> Any:
    """
    Create a Brand Profile for the current user.
    """
    # 1. Check if profile already exists
    if db.query(Brand).filter(Brand.user_id == current_user.id).first():
        raise HTTPException(status_code=400, detail="Brand profile already exists")

    # 2. Create DB Object
    db_brand = Brand(
        user_id=current_user.id,
        company_name=brand_in.company_name,
        industry=brand_in.industry,
        website=str(brand_in.website) if brand_in.website else None,
        verified=False
    )
    
    # 3. Commit
    db.add(db_brand)
    db.commit()
    db.refresh(db_brand)
    return db_brand

@router.post("/onboard/influencer", response_model=user_schema.InfluencerResponse)
def onboard_influencer(
    *,
    db: Session = Depends(get_db),
    influencer_in: user_schema.InfluencerCreate,
    current_user: deps.TokenData = Depends(deps.get_current_user)
) -> Any:
    """
    Create an Influencer Profile.
    """
    if db.query(Influencer).filter(Influencer.user_id == current_user.id).first():
        raise HTTPException(status_code=400, detail="Influencer profile already exists")

    db_inf = Influencer(
        user_id=current_user.id,
        username=influencer_in.username,
        bio=influencer_in.bio,
        niche=influencer_in.niche,
        wallet_address=influencer_in.wallet_address
    )
    
    db.add(db_inf)
    db.commit()
    db.refresh(db_inf)
    
    # Convert niche list to JSON compatible format if needed, but SQLAlchemy handles JSONB natively
    return db_inf

@router.get("/me", response_model=user_schema.UserResponse)
def read_user_me(
    db: Session = Depends(get_db),
    current_user: deps.TokenData = Depends(deps.get_current_user),
) -> Any:
    """
    Get current user details.
    """
    user = db.query(User).filter(User.id == current_user.id).first()
    # Mocking the response since we haven't synced 'users' table with Supabase Auth user yet
    # In a real Supabase setup, the User is in auth.users, and we might proxy it or have a trigger
    # For MVP, we assume the public.users table is populated.
    if not user:
         raise HTTPException(status_code=404, detail="User found in Auth but not in public.users")
    return user
