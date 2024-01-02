from fastapi import FastAPI

# Routers (recursos en otras carpetas)
from routers import basicAuth, products,users, jwtAuth, usersDB

# StaticFiles (llama recursos estaticos)
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Routers (recursos en otras carpetas)
app.include_router(products.router)
app.include_router(users.router)
app.include_router(usersDB.router)
app.include_router(jwtAuth.router)
app.include_router(basicAuth.router)

# StaticFiles (llama recursos estaticos)
app.mount("/static",StaticFiles(directory="static"),name="static")


@app.get("/")
async def root():
    return "Hola FastApi!"

@app.get("/url/")
async def url():
    return { "url_ig":"https://instagram.com/sibofit" }

# Documentacion con Swagger: http://127.0.0.1:8000/docs
# Documentacion con Redocly: http://127.0.0.1:8000/redoc

# Ejecutar servidor: uvicorn main:app --reload
# Ejecutar base de datos local: mongod --dbpath "directorio/base/de/datos"

# Operaciones para el servidor con decorador
# @app.post() "Creador"
# @app.get() "Lector"
# @app.put() "Actualizador"
# @app.delete() "Eliminador"