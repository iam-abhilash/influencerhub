from datetime import datetime
from typing import Any, Union
from jose import jwt, JWTError
from app.core.config import settings

ALGORITHM = "HS256"

def decode_access_token(token: str) -> Union[dict[str, Any], None]:
    """
    Decodes a JWT token and validates its signature.
    Returns the payload if valid, None otherwise.
    """
    try:
        # Supabase JWTs are signed with the project secret
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET, 
            algorithms=[ALGORITHM],
            audience="authenticated" # Supabase specific audience
        )
        return payload
    except JWTError:
        return None
