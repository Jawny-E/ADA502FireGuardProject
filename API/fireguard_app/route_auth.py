from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from starlette.status import HTTP_401_UNAUTHORIZED
from .kc.get_token import Keycloak_openid

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(data: LoginRequest):
    try:
        token = Keycloak_openid.token(data.username, data.password)
        return {"access_token": token["access_token"]}
    except Exception as e:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
