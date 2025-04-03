from pydantic import BaseModel

class User(BaseModel):
    id: str
    username: str
    firts_name: str
    last_name: str
    realm_roles: list
    client_roles: list
    locations: list