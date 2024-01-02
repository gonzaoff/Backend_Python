from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter(prefix="/products",
                tags=["products"],
                responses={404:{"message":"No encontrado"}})

oauth2 = OAuth2PasswordBearer(tokenUrl="login")


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
        "password" : "gonzasib",
    },
    "GonzaEsc23" : {
        "username": "GonzaEsc23",
        "full_name" : "Dario Sibolich",
        "email": "gonzaescobar26@gmail.com",
        "disabled": False,
        "password" : "654321",
    },
    "JMay" : {
        "username": "JMay",
        "full_name" : "Jose Maydana",
        "email": "joseMay@gmail.com",
        "disabled": True,
        "password" : "gon123",
    },
}

# Buscador de UsersDB. (Solo contrase;a)
def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

# Buscador de Users. (No expone contrase;a)
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

# Autenticador
async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    
    # Si no autoriza...
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales Invalidas",
            headers={"WWW-Authenticate": "Bearer"})
    
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
    if not form.password == user.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Contrase;a incorrecta")
    
    return {"access_token": user.username, 
            "token_type": "bearer"}

# Usuarios
@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user












