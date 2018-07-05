import random
from db_layer.dbconnector import CONNECTOR_READWRITE
from db_layer.obj_prototype import Transaction
from db_layer.stdDBIO import stdDBIO
from reviewerApp.templatetags.filters import style
def gen_randamData(num):
    result = []
    tags = list(style.keys())
    description = ["","important things","a kind of waste","well paid off","I have to do that","Never do that again"]
    for i in range(num):
        result.append({
            "timestamp": random.randint(1530724905-365*24*3600,1530724905),
            "amount": random.randint(-500,500),
            "tags": set([random.choice(tags)]),
            "description": random.choice(description)
        })
    return result

def addSampleToDB(samples):
    io = stdDBIO("960911nbrNBR", mode=CONNECTOR_READWRITE)
    io.setDB(Transaction.dbname)
    io.setCollection(Transaction.collection)
    for s in samples:
        io.writeObj(s)

if __name__=="__main__":
    pass

    addSampleToDB(gen_randamData(100))
