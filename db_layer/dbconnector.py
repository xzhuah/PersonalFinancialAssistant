import pymongo
from .security import decrypt_obj,getKey
CONNECTOR_READONLY = 0x12345678
CONNECTOR_READWRITE = 0x87654321

def getClient(password="",username="",type = CONNECTOR_READONLY,loginFull = ""):
    if loginFull!="":
        try:
            client = pymongo.MongoClient(loginFull)
            info = client.server_info()

        except Exception as err:
            print(err)
            raise err
        return client
    try:
        if type == CONNECTOR_READONLY:
            login = decrypt_obj(getKey(password),"readMode.pkl")
            client = pymongo.MongoClient("mongodb+srv://{0}:{1}@cluster0-jghyh.mongodb.net/test?retryWrites=true".format(login["user"],login["code"]))
        elif type == CONNECTOR_READWRITE:
            login = decrypt_obj(getKey(password),"writeMode.pkl")
            client = pymongo.MongoClient("mongodb+srv://{0}:{1}@cluster0-jghyh.mongodb.net/test?retryWrites=true".format(login["user"],login["code"]))
        return client
    except Exception as e:
        print("Login Failed",e)
        client = pymongo.MongoClient(
            "mongodb+srv://{0}:{1}@cluster0-jghyh.mongodb.net/test?retryWrites=true".format(username,
                                                                                            password))
        return client



