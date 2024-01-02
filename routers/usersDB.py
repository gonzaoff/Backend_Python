from fastapi import APIRouter, HTTPException,status
from db.models.user import User
from db.schemas.user import user_schema, users_schema
from db.client import db_client
from bson import ObjectId


router = APIRouter(prefix="/userdb",
                   tags=["userdb"],
                   responses={status.HTTP_404_NOT_FOUND: {"message" : "No encontrado."}})

urlquery = "http://127.0.0.1:8000/userdb?id=1"

# Obtener todos los usuarios
@router.get("/", response_model=list[User])
async def users():
    return users_schema(db_client.users.find())

# Obtener usuarios por id
@router.get("/{id}")
async def user(id: str):
    return search_user("_id", ObjectId(id))

# Obtener usuarios por id
@router.get("/")
async def user(id: str):
    return search_user("_id", ObjectId(id))
    



# Crear usuarios.
@router.post("/",
             response_model=User,
             status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    
    # Si el email ingresado es igual a algun email encontrado en User, lanza excepcion.
    if type(search_user("email", user.email)) == User:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El usuario ya existe")

    # Genera una var que contiene el usuario en modo diccionario
    user_dict = dict(user)
    # Elimina el campo ID del dic porque MDB ya lo asigna.
    del user_dict["id"]

    # Usa el diccionario para insertar un nuevo usuario y un id.
    id = db_client.users.insert_one(user_dict).inserted_id

    # Usa la funcion para buscar por ID
    newUser = user_schema(db_client.users.find_one({"_id" : id}))
    
    return User(**newUser)



# Modificar usuarios completos.
@router.put("/",
            response_model=User,
            status_code=status.HTTP_202_ACCEPTED)
async def user(user: User):
    
    # Genera una var que contiene el usuario en modo diccionario
    user_dict = dict(user)
    # Elimina el campo ID del dic porque MDB ya lo asigna.
    del user_dict["id"]
    
    try:
        db_client.users.find_one_and_replace({"_id" : ObjectId(user.id)}, user_dict)
    except:
        return HTTPException(status_code=status.HTTP_409_CONFLICT,
                             detail="Usuario no modificado")

    return search_user("_id", ObjectId(user.id))


# Borrando usuarios con path.
@router.delete("/{id}",
               status_code=status.HTTP_204_NO_CONTENT)
async def user(id: str):

    found = db_client.users.find_one_and_delete({"_id" : ObjectId(id)})
    
    if not found:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Usuario no eliminado")
  
  
                            
# Funcion buscador por "campo", "clave"
def search_user(field:str, key):
    
    try:
        user = user_schema(db_client.users.find_one({field : key}))
        return User(**user)
    except:
        return {"error":"usuario no encontrado"}