from bd import getDatabase
from bson.objectid import ObjectId
import crud

db = getDatabase()
collection = "producto"

idOnWeb = "6738b34e3ee590aec042f807"
testFlag = crud.readDoc(db,collection,{})


for i in range(0,len(testFlag),1):
    if (i%4)==0:
        print('')
    print(testFlag[i]['_id'])