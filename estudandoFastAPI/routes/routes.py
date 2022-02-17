from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from infra import crud, schemas
from fastapi import APIRouter
from infra.database import get_db

Routers = APIRouter(
)


@Routers.post("/users/", response_model=schemas.User, tags=['users'])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    #procura se ja tem user com email
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    #cria novo usuario
    return crud.create_user(db=db, user=user)


@Routers.get("/users/", response_model=list[schemas.User], tags=['users'])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@Routers.get("/users/{user_id}", response_model=schemas.User, tags=['users'])
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@Routers.post("/users/{user_id}/items/", response_model=schemas.Item, tags=['users'])
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    #verifica se o usuario existe
    db_user = crud.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    #cria
    return crud.create_user_item(db=db, item=item, user_id=user_id)
