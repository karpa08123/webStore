from bson.objectid import ObjectId

def clearFormat(data): # Limpia el formato para recibirlo como una unica coleccion
    flag1 = dict(zip(*[iter(data)]*2))
    for i in data:
       flag1 = dict(i)
    return flag1

def createOneDoc(db,collection,data): #Crear registro
    return db[collection].insert_one(data)

def createMultiDoc(db,collection,data):
    return db[collection].insert_many(data)

def readDoc(db,collection,query): # Lee registros
    return list(db[collection].find(query))

def readDocById(db,collection,productId): # Lee registros
    return list(db[collection].find({'_id':ObjectId(productId)}))

def updateDoc(db,collection,filter,newValues):
    return db[collection].update_many(filter, {'$set':newValues})

def deleteOneDoc(db,collection,filter):
    return db[collection].delete_one(filter)