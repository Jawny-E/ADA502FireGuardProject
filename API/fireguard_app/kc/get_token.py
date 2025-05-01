import os
from keycloak import KeycloakOpenID
from dotenv import load_dotenv

load_dotenv()

KEYCLOAK_URL = os.getenv("Server_url")
KEYCLOAK_REALM = os.getenv("realm")
KEYCLOAK_CLIENT_ID = os.getenv("KeyCloak_client")
KEYCLOAK_CLIENT_SECRET = os.getenv("KeyCloak_secret")


Keycloak_openid = KeycloakOpenID(
    server_url=KEYCLOAK_URL,
    realm_name=KEYCLOAK_REALM,
    client_id=KEYCLOAK_CLIENT_ID,
    client_secret_key=KEYCLOAK_CLIENT_SECRET
)