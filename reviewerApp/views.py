from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from db_layer.stdDBIO import stdDBIO
from db_layer.obj_prototype import Transaction
from django.template import loader
from db_layer.dbconnector import CONNECTOR_READWRITE
import time
import datetime
from django.urls import reverse
from functools import reduce
from django.template import RequestContext

# Create your views here.

io = stdDBIO("960911nbrNBR",mode=CONNECTOR_READWRITE)
all_tags = set()
def index(request):
    global io,all_tags
    # by default, the page will shows user a graph with the transaction activity in recent
    # user can change the visualization method
    # user can choose to enter the recorder app to input new transaction
    # user will be able to delete their old transactions and update them by entering new ones

    # the password will be stored in cookie later

    io.setDB(Transaction.dbname)
    io.setCollection(Transaction.collection)

    all_objects = io.readObjs()
    print(all_objects)

    all_transaction = list(map(lambda ob:Transaction(**(ob['content']),id=ob["_id"]),all_objects))

    [print(t,t.id) for t in all_transaction]



    ###
    test = [
            {"amount":5,"timestamp":int(time.time()),
             "tags":set(["tips"]),"description":"get tips"},

            {"amount": -50, "timestamp": int(time.time()),
             "tags": set(["drink,food"]), "description": "buy beer"}
           ]

    [all_transaction.append(Transaction(**ob)) for ob in test]
    ###

    #all_tags = reduce(lambda x, y: x.obj["tags"].union(y.obj["tags"]), all_transaction)
    for tx in all_transaction:
        all_tags = all_tags.union(tx.obj["tags"])

    all_transaction = sorted(all_transaction,
                             key=lambda k:k.obj["timestamp"],reverse=True)

    template = loader.get_template('index.html')
    context = {
        'all_transaction': all_transaction,
    }

    return HttpResponse(template.render(context,request))


def recorder(request):
    return render(request, 'recorder.html')

def add_txs(request):
    global io, all_tags
    times = request.POST.getlist("time",[])

    amount=request.POST.getlist("amount",[])
    pay_gain = request.POST.getlist("Pay",[])
    tags = request.POST.getlist("tags",[])
    description = request.POST.getlist("description",[])
    print(request.POST,times,amount,tags,description)
    result = []
    for i,t in enumerate(times):
        try:
            result.append({
                "timestamp":int(time.mktime(datetime.datetime.strptime(t, "%Y-%m-%d").timetuple())),
                "amount":-int(amount[i]) if request.POST["Pay"+str(i)]=="pay" else int(amount[i]),
                "tags":set(tags[i].split(";")),
                "description":description[i]
            })
        except Exception as e:
            print(e)
            continue

    txs = list(map(lambda x:Transaction(**x),result))
    io.setDB(Transaction.dbname)
    io.setCollection(Transaction.collection)
    [io.writeObj(tx.obj) for tx in txs]

    print(txs)
    return HttpResponseRedirect('../review/')
    #return  render_to_response('test.html',{"attr":txs},RequestContext(request))

