from fastapi.security import (
    HTTPBasicCredentials,
    HTTPBasic,
    SecurityScopes
)
from fastapi import HTTPException, status, Depends, Security

import secrets

from fakeDB import get_user, fake_users_db

from hashCrypt import verify_password, get_password_hash

from datetime import datetime, timedelta

from jose import JWTError, jwt

from pydantic import ValidationError

from securityModels import (
    ALGORITHM,
    SECRET_KEY,
    oauth2_scheme,
    TokenData,
    User
    )


security = HTTPBasic()


def simple_auth(credential: HTTPBasicCredentials = Depends(security)):
    username = secrets.compare_digest(credential.username, "eu")
    password =  secrets.compare_digest(credential.password, 'nois')
    if not (username and password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    return credential.username


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = f'Bearer'
    

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )

    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception

        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)

    except (JWTError, ValidationError):
        raise credentials_exception
    
    user = get_user(fake_users_db, username=token_data.username)
    
    if user is None:
        raise credentials_exception

    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user

def simple_auth(credential: HTTPBasicCredentials = Depends(security)):
    username = secrets.compare_digest(credential.username, "eu")
    password =  secrets.compare_digest(credential.password, 'nois')
    if not (username and password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    return credential.username

async def get_current_active_user(
    current_user: User = Security(get_current_user, scopes=["me"])
):
    
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user