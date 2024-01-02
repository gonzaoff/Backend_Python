from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class User(BaseModel):
    id: int
    name: str
    surname : str
    age: int
    url: str

users_list = [User(id=1, name="Gonzalo", surname="Escobar", age=22, url="/sibofit"),
        User(id=2, name="Federico", surname="Escobar", age=36, url="/fyge"),
        User(id=3, name="Natalia", surname="Escobar", age=28, url="/natiesc")]

# Creamos un JSON a mano.
@router.get("/usersjson")
async def userjson():
    return [{"name" : "Gonza", "surname" : "Escobar", "age": 22 , "url" : "https://www.instagram.com/sibofit"},
            {"name" : "Fede", "surname" : "Escobar", "age": 29 , "url" : "https://www.instagram.com/fyges"},
            {"name" : "Nati", "surname" : "Escobar", "age": 36 , "url" : "https://www.instagram.com/naesc"}]


# Lista de Usuarios
@router.get("/users/")
async def users():
    return users_list

# Path.
@router.get("/user/{id}")
async def user(id:int):
    return search_user(id)


# Query.
@router.get("/user/")
async def user():
    return search_user(id)

urlquery = "http://127.0.0.1:8000/users?id=1"

# Crear usuarios.
@router.post("/user/", status_code=201)
async def create_user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=409, detail="Usuario existente")

    users_list.append(user)
    return user

# Modificar usuarios completos.
@router.put("/user/")
async def user(user: User):
    
    found = False
    
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:  
            users_list[index] = user
            found = True
            return user

    if not found:
        raise HTTPException(status_code=409, detail="Usuario no modificado")

# Borrando usuarios con path.
@router.delete("/user/{id}")
async def user(id: int):

    found = False
    
    for index, saved_user in enumerate(users_list):
            if saved_user.id == id:  
                del users_list[index]
                found = True
                return {"success" : "Usuario eliminado exitosamente."}
    if not found:
        raise HTTPException(status_code=409, detail="Usuario no eliminado")
# Funcion resumen
def search_user(id:int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error":"No se ha encontrado el usuario"}
    
