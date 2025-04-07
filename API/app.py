from fastapi import FastAPI
from Fireguard_API import get_fire_risk, get_fire_risk_trends


# For å starte serveren : "poetry run uvicorn app:app --reload" i terminal
# Eventuelt uten reload (Om du får problemer når du allerede har startet serveren)
# http://127.0.0.1:8000/docs#/ for å få interaktiv side med dokumentasjon på de ulike funksjonene

app = FastAPI()


EXCLUDE_PATHS = {"/", "/openapi.json", "/docs", "/docs/oauth2-redirect", "/redoc"}


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
