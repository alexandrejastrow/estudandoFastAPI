from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordRequestForm, HTTPBasicCredentials

from securityModels import Token, ACCESS_TOKEN_EXPIRE_MINUTES, User

from authenticate import (
    authenticate_user, 
    create_access_token, 
    get_current_active_user, 
    get_current_user,
    security,
    simple_auth
    )

from fakeDB import fake_users_db

from datetime import timedelta


route = APIRouter()


#rota de login retorna um class Token
@route.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": form_data.scopes},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@route.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@route.get("/users/me/items")
async def read_own_items(
    current_user: User = Security(get_current_active_user, scopes=["items"])
):
    return [{"item_id": "Foo", "owner": current_user.username}]


@route.get("/status")
async def read_system_status(current_user: User = Depends(get_current_user)):
    return {"status": "ok"}


@route.get('/users/me2')
async def read_user2(credential: HTTPBasicCredentials = Depends(security)):

    return {"username": credential.username, "password": credential.password}

@route.get('/users/me3')
async def read_user2(username: str = Depends(simple_auth)):

    return {"username": username}