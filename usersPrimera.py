from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# Conociendo decoradores y metodo de uso.
@app.get("/user1")
async def user1():
    return "Hola Users"


# Primer intento de base de datos
@app.get("/userjson")
async def userjson():
    return [{"name" : "Gonza", "surname" : "Escobar", "age": 22 , "url" : "https://www.instagram.com/sibofit"},
            {"name" : "Fede", "surname" : "Escobar", "age": 29 , "url" : "https://www.instagram.com/fyges"},
            {"name" : "Nati", "surname" : "Escobar", "age": 36 , "url" : "https://www.instagram.com/naesc"}]


# Segundo intento
# Definiendo el tipo de cada variable en una clase.
class User(BaseModel):
    name: str
    surname : str
    age: int
    url: str

primera_users_list = [User(name="Gonzalo", surname="Escobar", age=22, url="/sibofit"),
        User(name="Federico", surname="Escobar", age=36, url="/fyge"),
        User(name="Natalia", surname="Escobar", age=28, url="/natiesc")]

@app.get("/users")
async def users():
    return primera_users_list


# Tercer intento de base de datos. 
# Definiendo el tipo de cada variable en una clase. Campturando ID's
class User(BaseModel):
    id: int
    name: str
    surname : str
    age: int
    url: str

users_list = [User(id=1, name="Gonzalo", surname="Escobar", age=22, url="/sibofit"),
        User(id=2, name="Federico", surname="Escobar", age=36, url="/fyge"),
        User(id=3, name="Natalia", surname="Escobar", age=28, url="/natiesc")]

@app.get("/users")
async def users():
    return users_list

# Usando Path.
@app.get("/user/{id}")
async def user(id:int):
    return search_user(id)


# Cuarto intento de base de datos. 
# Usando Query.
@app.get("/user/")
async def user():
    return search_user(id)

urlquery = "http://127.0.0.1:8000/users?id=1"


# @app.post("/users/")
# async def create_user(user: User):
#     if type(search_user(user.id)) == User:
#         return {"error":"El usuario ya existe."}
#     else:
#         users_list.append(user)
#         return {"success": "Usuario creado exitosamente"}



# Funcion resumen
def search_user(id:int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return vars(list(users)[0])  # Convierte el objeto User a un diccionario
    except:
        return {"error":"No se ha encontrado el usuario"}