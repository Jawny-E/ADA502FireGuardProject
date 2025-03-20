from decouple import config
from keycloak import KeycloakOpenID
from fastapi import HTTPException, status, Depends, Request

from kc.models import User

