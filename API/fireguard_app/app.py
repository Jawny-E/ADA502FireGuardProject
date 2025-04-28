# The main application controlling the FastAPI
from fastapi import FastAPI, Depends, status
from .Fireguard_API import get_fire_risk, get_fire_risk_trends
from .kc.auth import *

# For å starte serveren : "poetry run uvicorn app:app --reload" i terminal
# Eventuelt uten reload (Om du får problemer når du allerede har startet serveren)
# http://127.0.0.1:8000/docs#/ for å få interaktiv side med dokumentasjon på de ulike funksjonene

app = FastAPI()

EXCLUDE_PATHS = {"/", "/openapi.json", "/docs", "/docs/oauth2-redirect", "/redoc"}

# Base URL
@app.get("/")
async def list_routes():
    routes = {}
    for route in app.routes:
        if hasattr(route, "methods") and route.path not in EXCLUDE_PATHS:
            formatted_methods = [f"Method: {method}" for method in route.methods]
            routes[route.path] = formatted_methods
    return {"Available Endpoints": routes}


@app.get("/locations/{location}")
def fire_risk_endpoint(location: str, days_past: int = 7, weatherdata: bool = False):
    return get_fire_risk(location, days_past, weatherdata)


@app.get("/locations/{location}/trends")
def fire_risk__trends_endpoint(location: str):
    return get_fire_risk_trends(location)


@app.get('/api/v1/admin')
def protected_admin(admin: bool = Depends(verify_admin_role)):
    return {"message": "This is a protected resource for ADMIN role."}


@app.get('/api/v1/admin/service')
def protected_sadmin(admin: bool = Depends(verify_sadmin_role)):
    return {"message": "This is a protected resource for APP_ADMIN role."}


@app.get('/api/v1/protected')
def protected_user(user: bool = Depends(verify_user_role)):
    return {"message": "This is a protected resource for USER role."}


@app.get('/api/v1/protected/service')
def protected_suser(user: bool = Depends(verify_suser_role)):
    return {"message": "This is a protected resource for APP_USER role."}


@app.get('/api/v1/public', status_code=status.HTTP_200_OK)
def public_user():
    return {"message": "This is a public resource for everyone."}


@app.get("/api/v1/")
def protected_user_query(user: bool = Depends(verify_user_locquery)):
    return {"message": "This is a protected resource for any user that is registered on a location."}


@app.get("/api/v1/{location}")
def protected_user_loc(location: str, user: bool = Depends(verify_user_path)):
    return {"message": f'This is a protected resource for any user that is registered on location = {location}.'}
