from fastapi import APIRouter, Depends, HTTPException, Request
from .kc.get_token import Keycloak_openid

router = APIRouter()

def get_current_user(request: Request):
    auth = request.headers.get("Authorization")
    if not auth:
        raise HTTPException(status_code=401, detail="Missing token")

    token = auth.split(" ")[1]
    try:
        user_info = Keycloak_openid.userinfo(token)
        return user_info
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/api/v1/protected")
def protected_route(user: dict = Depends(get_current_user)):
    return {"message": f"Hello {user['preferred_username']}! You are authorized."}
