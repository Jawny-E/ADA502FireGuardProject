from decouple import config
from keycloak import KeycloakOpenID
from fastapi import HTTPException, status, Depends, Request

from .models import User

server_url_env = config("Server_url")  # Use config to read from .env
server_realm = config("realm")        # Use config to read from .env

keycloak_openid = KeycloakOpenID(
    server_url=server_url_env,       # Use the variables read via config
    realm_name=server_realm,         # Use the variables read via config
    client_id=""
)

# Get Token from HTTP Request object of the restapi endpoint
def get_jwttoken(req: Request):
    token = req.headers["Authorization"]
    token = token.split(" ").pop(1)
    print(token)
    return token


async def get_idp_public_key():
    return (
        "-----BEGIN PUBLIC KEY-----\n"
        f"{keycloak_openid.public_key()}"
        "\n-----END PUBLIC KEY-----"
    )


# Decode Token
async def get_payload(token=Depends(get_jwttoken)) -> dict:
    try:
        return keycloak_openid.decode_token(
            token,
            key=await get_idp_public_key(),
            options={
                "verify_signature": True,
                "verify_iss": True,
                "verify_exp": True
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_user_info(payload: dict = Depends(get_payload)) -> User:
    print(payload)
    client_id = payload.get("azp")
    try:
        return User(
            id=payload.get("sub"),
            username=payload.get("preferred_username"),
            first_name=payload.get("given_name"),
            last_name=payload.get("family_name"),
            realm_roles=payload.get("realm_access", {}).get("roles", []),
            client_roles=payload.get("resource_access", {}).get(client_id, {}).get("roles", []),
            locations = payload.get("location", [])
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


def verify_admin_role(user: User = Depends(get_user_info)) -> bool:
    roles: list = user.realm_roles
    roles.extend(user.client_roles)
    print(roles)
    return verify_role(roles, "ADMIN")


def verify_sadmin_role(user: User = Depends(get_user_info)) -> bool:
    roles: list = user.realm_roles
    roles.extend(user.client_roles)
    print(roles)
    return verify_role(roles, "APP_ADMIN")


def verify_user_role(user: User = Depends(get_user_info)) -> bool:
    roles: list = user.realm_roles
    roles.extend(user.client_roles)
    return verify_role(roles, "APP_USER")


def verify_suser_role(user: User = Depends(get_user_info)) -> bool:
    roles: list = user.realm_roles
    roles.extend(user.client_roles)
    return verify_role(roles, "APP_USER")


def verify_role(roles: list, role: str) -> bool:
    try:
        roles.index(role)
        return True
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized action",
            headers={"WWW-Authenticate": "Bearer"}
        )

def verify_user_path(req: Request, user: User = Depends(get_user_info)):
    rpath: str = req.url.path
    print(rpath)
    paths: list = user.locations
    print(paths)
    return verify_path(paths, rpath)

def verify_user_locquery(req: Request, user: User = Depends(get_user_info)):
    rquery: str = req.url.query
    print(rquery)
    if len(rquery) > 0:
        qparam = rquery.split("=").pop(1).split(",")
        print(qparam)
        parameters: list = user.locations
        print(parameters)
        return verify_parameters(parameters, qparam)
    else:
        return False

def verify_path(paths: list, path: str):
    try:
        paths.index(path)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'Not authorized to access this sensor(s): {path} ',
            headers={"WWW-Authenticate": "Bearer"}
        )

def verify_parameters(user_parameters: list, query_parameters: list):
    sparam = set(user_parameters)
    sdiff = [x for x in query_parameters if x not in sparam]
    print(sdiff)
    ssdiff = f' {", ".join(sdiff)}'
    if len(sdiff) == 0:
        sdiff = query_parameters
    try:
        user_parameters.index(sdiff.pop(0))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'Not authorized to access these parameters:{ssdiff} ',
            headers={"WWW-Authenticate": "Bearer"}
        )