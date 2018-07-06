# we will not provide any query function on the database, each query will return all result in one collection
from .dbconnector import *
from .security import *
import time
from bson.objectid import ObjectId

default_encryp_password = "zhudbencode1996"
class stdDBIO:

    def __init__(self,password="",content_password = default_encryp_password,mode = CONNECTOR_READONLY, username = "",mongodbToken=""):
        try:
            self.client = getClient(password=password,type=mode,username=username,loginFull=mongodbToken)
        except Exception as e:
            raise e
        # you can reach to your own client by the following if you have your own username and password
        #self.client = pymongo.MongoClient(
           # "mongodb+srv://{0}:{1}@cluster0-jghyh.mongodb.net/test?retryWrites=true".format(username,
                                                                                           # password))
        self.setDB("Test")
        self.setCollection("Test")
        self.content_password = content_password

        self.loginTime = time.time()
        self.operation = {}

        if mode == CONNECTOR_READONLY:
            self.operation["Privilege"] = "ReadOnly"
        elif mode == CONNECTOR_READWRITE:
            self.operation["Privilege"] = "ReadWrite"
        else:
            self.operation["Privilege"] = "Confused"

        self.operation["read"] = 0
        self.operation["insert"] = 0
        self.operation["drop"] = 0
        self.operation["delete"] = 0
        self.operation["update"] = 0

        print("Init standard database IO object")

    # we use a context manager here to record each legal login event
    def __enter__(self):

        print("set up context manager")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        record_obj = {"loginTime":self.loginTime,"logoutTime":time.time()}
        for key in self.operation:
            record_obj[key] = self.operation[key]
        self.setDB("LoginRecorder")
        self.setCollection("History")
        self.collection.insert_one(record_obj)
        self.client.close()
        print("context manager close successfully")

    def setDB(self,db_name):
        self.db=self.client[db_name]
        self.setCollection("Test")

    def getAllCollection(self):
        return self.db.collection_names()

    def setCollection(self,collectionName):
        self.collection=self.db[collectionName]

    def writeObj(self,obj):
        self.collection.insert_one({"content":e_obj(self.content_password,obj)})
        self.operation["insert"] += 1

    def writeObjs(self,obj_list):
        encrpted = []
        for obj in obj_list:
            encrpted.append({"content":e_obj(self.content_password,obj)})
        self.collection.insert_many(encrpted)
        self.operation["insert"]+=len(obj_list)

    def readObjs(self):
        query = list(self.collection.find({}))
        result = []
        for q in query:
            # you can use different encode password, but only those encoded with your password can be returned
            try:
                q["content"]=d_obj(self.content_password,q["content"])
                result.append(q)
            except:
                #result.append({"_id":q["_id"]})
                continue # it will only return those successfully decrypted so that the db is shareable

        self.operation["read"] += len(result)
        return result

    def readObjs_seq(self):
        for q in self.collection.find({}):
            self.operation["read"] += 1
            try:
                yield d_obj(self.content_password,q["content"])
            except:
                #yield {"_id":q["_id"]}
                continue


    def dropCollection(self):
        try:
            self.collection.drop()
            self.operation["drop"] += 1
            self.setCollection("Test")
        except Exception as e:
            print(e)


    def deleteWithObid(self,oid):
        if isinstance(oid, str):
            oid = ObjectId(oid)
        try:
            self.collection.delete_one({"_id": oid})
            self.operation["delete"]+=1
        except Exception as e:
            print(e)


    def updateWithObid(self,oid,newObj):
        self.collection.delete_one({"_id": oid})
        self.writeObj(newObj)
        self.operation["update"] += 1


if __name__=="__main__":
    pass


    #     # io.setDB("encode")
    #     #
    #     # for c in io.getAllCollection():
    #     #     print(c)
    #     #
    #     # for obj in io.readObjs():
    #     #     print(obj)
    #
    #     # try:
    #     #     io.writeObj({"value":"testing"})
    #     # except:
    #     #     print("not allowed")
    #     #print(io.readObjs())
    #
