
# modulo de conexion MongoDB: pip install pymongo

from pymongo import MongoClient

# Base de datos local
# db_client = MongoClient().local

#  Base de datos online
db_client = MongoClient(
    "mongodb+srv://GonzaSib340:<password>/?retryWrites=true&w=majority"
    ).test

##prime

