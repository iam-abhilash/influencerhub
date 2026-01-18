import pytest
from fastapi import HTTPException
# In a real scenario, we'd mock the DB and User models
# For now, we test the logic of a hypothetical RBAC enforcer

def mock_get_current_brand_user(user_role: str):
    if user_role != "brand":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return True

class TestRBAC:
    def test_brand_access_allowed(self):
        assert mock_get_current_brand_user("brand") is True

    def test_influencer_access_denied(self):
        with pytest.raises(HTTPException) as excinfo:
            mock_get_current_brand_user("influencer")
        assert excinfo.value.status_code == 403

    def test_anon_access_denied(self):
        with pytest.raises(HTTPException) as excinfo:
            mock_get_current_brand_user("anon")
        assert excinfo.value.status_code == 403
