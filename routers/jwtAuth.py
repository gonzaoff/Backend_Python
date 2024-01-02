from os import access
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET_KEY = "e9e438aabcd27a07b3b1ba2c273d2db812f744d02c334f778bed0a6de8055a1f"

# ESTO FALTA ROUTEARLO!!!
# ESTO FALTA ROUTEARLO!!!
# ESTO FALTA ROUTEARLO!!!
# ESTO FALTA ROUTEARLO!!!


router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

# Modelo de BD
class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool


class UserDB(User):
    password: str


users_db = {
    "sibofit" : {
        "username": "sibofit",
        "full_name" : "Gonzalo Escobar",
        "email": "gonza-09-10@gmail.com",
        "disabled": False,
        "password" : "$2a$12$ec23IZMKKcnnhjoTTxjd..nQc9TNfm9y7MAtmDzaWnCIuvF9MjLSK",
    },
    "GonzaEsc23" : {
        "username": "GonzaEsc23",
        "full_name" : "Dario Sibolich",
        "email": "gonzaescobar26@gmail.com",
        "disabled": False,
        "password" : "$2a$12$bXm1Gyf3Fg2K.FblUmXOIeMVwiq2aPy5U30X4YdCKJWHMSdJL3n9a",
    },
    "JMay" : {
        "username": "JMay",
        "full_name" : "Jose Maydana",
        "email": "joseMay@gmail.com",
        "disabled": True,
        "password" : "$2a$12$rgzJXU6fRWesIuBK8L9Creb0s5kMkRyz4gw3s0JepvCmYr9XroJ62",
    },
}

"""
"password" : "gonzasib",
"password" : "654321",
"password" : "gon123",
"""

# Buscador de Users. (No expone contrase;a)
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    
# Buscador de UsersDB. (Solo contrase;a)
def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
async def auth_user(token:str = Depends(oauth2)):
    
    exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales Invalidas",
            headers={"WWW-Authenticate": "Bearer"})
    
    try:
        username = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception
        
    except JWTError:
        # Si no autoriza...
        raise exception

    # Si todo sale bien...
    return search_user(username)
    
    
# Autenticador
async def current_user(user: User = Depends(auth_user)):

    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario Inactivo")
    
    return user


# LogIn
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    
    # Si el usuario no existe...
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Usuario incorrecto")
    
    user = search_user_db(form.username)
    
    # Si la contrase;a es incorrecta
    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Contrase;a incorrecta")
    
    access_token = {"sub" : user.username,
                    "exp" : datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)}
    
    return {"access_token": jwt.encode(access_token,SECRET_KEY,algorithm=ALGORITHM), 
            "token_type": "bearer"}

# Mis Datos.
@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
