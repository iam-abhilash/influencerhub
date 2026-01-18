from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.security import decode_access_token
# Placeholder for User model schema - normally we'd import simple Pydantic models here
from pydantic import BaseModel
from typing import List

# This tells FastAPI where to look for the token (the 'Authorization' header)
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"/api/v1/login/access-token" # This isn't strictly used since we use Supabase login, but required by FastAPI spec
)

class TokenData(BaseModel):
    id: str
    email: str | None = None
    role: str | None = None

class User(BaseModel):
    id: str
    email: str
    role: str
    is_active: bool = True

def get_current_user(token: Annotated[str, Depends(reusable_oauth2)]) -> TokenData:
    """
    Depedency to validate the JWT from the Authorization header.
    Decodes the token and extracts the user ID (stub).
    """
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Supabase stores the UUID in 'sub'
    user_id: str = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Token missing subject (sub)")
    
    # In a full impl, we would check DB here OR rely on app_metadata claim if custom claims are set up
    # For now, we return basic token data
    # role = payload.get("app_metadata", {}).get("role", "user") 
    
    return TokenData(id=user_id, email=payload.get("email"), role="authenticated") # Defaulting role for now

def get_current_active_user(
    current_user: Annotated[TokenData, Depends(get_current_user)]
) -> TokenData:
    """
    Ensures the user is active (not banned).
    """
    # Logic to check strict 'active' status would go here
    return current_user

def get_current_brand_user(
    current_user: Annotated[TokenData, Depends(get_current_user)]
) -> TokenData:
    """
    RBAC: Enforce that the user is a Brand.
    """
    # In real app: fetch user from DB and check public.users.role == 'brand'
    # For MVP design phase:
    # if current_user.role != 'brand':
    #     raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user
