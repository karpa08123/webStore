from bd import GetDatabase
from bson.objectid import ObjectId
import crud

db = GetDatabase()
collection = "producto"

idOnWeb = "6738b34e3ee590aec042f807"
#arti = crud.ReadDoc(db,collection,{'_id':'ObjectId('+idOnWeb+')'})
#arti = crud.ReadDoc(db,collection,{'_id':"ObjectId('67377e582b8385850b42f808')"})
#arti = crud.ReadDoc(db,collection,{'_id':ObjectId(idOnWeb)})
arti = crud.ReadDocById(db,collection,idOnWeb)
arti = crud.ClearFormat(arti)
#arti = crud.ReadDoc(db,collection,{'nombre':'cosoLoco'})
#arti = crud.ReadDoc(db,collection,{'nombre':'testName'})
print(arti)
#arti = crud.ClearFormat(arti)
#print(arti)