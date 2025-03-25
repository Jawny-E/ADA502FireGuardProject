from typing import Union
from fastapi import FastAPI
from Fireguard_API import get_fire_risk

# For å starte serveren : "poetry run uvicorn app:app --reload" i terminal
# Eventuelt uten reload (Om du får problemer når du allerede har startet serveren)
# http://127.0.0.1:8000/docs#/ for å få interaktiv side med dokumentasjon på de ulike funksjonene

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI with Poetry!"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

# Location i stedsnavn, har hardkodet Bergen, Stavanger og Oslo som eks.
# Gir for 1 dag bakover, og 10? dager framover. Fikk ikke lov å velge days_past som 0


@app.get("/locations/{location}")
def fire_risk_endpoint(location: str, days_past: int = 1):
    return get_fire_risk(location, days_past)
