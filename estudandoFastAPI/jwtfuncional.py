from datetime import datetime, timedelta

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel


SECRETE_KEY = "442567fd20d291739b6ebc884005e557"
ALGORITH = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440

fake_user_db = {
    "alexandre": {
        "id": "23f35d6d-c72c-49fc-bcf0-948c08ce3e6b",
        "username": "alexandre",
        "full_name": "alexandre jastrow",
        "email":"alexandre@gmail.com",
        "password_hash": "$2b$12$oqo/UKJ0qLjt0jy22i7YUetkvXPGVxkYTGPQgPMDtBHDrOc0Yz19a",
        "disabled": False
    }
}

#schema
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    username: str
    email: str
    full_name: str | None = None
    disable: bool | None = None
    
class UserInDB(User):
    password_hash: str


pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

def verify_password(plain_password: str, password_hash: str) -> bool:
    return pwd_context.verify(plain_password, password_hash)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def get_user(db, username: str):
    if(username in db):
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(db, username: str, password: str) -> bool | UserInDB:
    user = get_user(db, username)
    
    if not user:
        return False
    
    if not verify_password(password, user.password_hash):
        return False

    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRETE_KEY, algorithm=ALGORITH)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_schema)) -> User | HTTPException:
    credential_exeption = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validade credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, SECRETE_KEY, algorithms=[ALGORITH])

        username: str = payload.get("sub")
        if username is None:
            raise credential_exeption
        token_data = TokenData(username=username)

    except JWTError:
        raise credential_exeption
    
    user = get_user(fake_user_db, username=token_data.username)

    if user is None:
        raise credential_exeption
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disable:
        raise HTTPException(status_code=400, detail="Inative user")
    return current_user


@app.post("/token", response_model=Token)
async def login_access_token(form_data: OAuth2PasswordRequestForm = Depends()):

    user = authenticate_user(fake_user_db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers ={
                "WWW-Authenticate":"Bearer"
            }
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@app.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]
