from pymongo import MongoClient

# IMPORTANTE deberias refactorizar la conexion para que se pueda cerra

def getDatabase():
    client = MongoClient("mongodb://127.0.0.1:27017/?connectTimeoutMS=6000")
    return client['panGo']
