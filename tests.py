from bd import getDatabase
from bson.objectid import ObjectId
import crud

db = getDatabase()
collection = "producto"

idOnWeb = "6738b34e3ee590aec042f807"
testFlag = crud.readDoc(db,collection,{})


from datetime import datetime

#Día actual

#Fecha actual
now = datetime.now()


print(now)
