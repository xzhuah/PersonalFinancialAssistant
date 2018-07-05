from __future__ import unicode_literals

from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from db_layer.stdDBIO import stdDBIO
from db_layer.obj_prototype import Transaction
from django.template import loader, RequestContext
from django.http import Http404
from db_layer.dbconnector import CONNECTOR_READWRITE
import time
import datetime
from reviewerApp.templatetags.filters import style
from pyecharts import Line, Bar, Overlap,Bar3D,ThemeRiver


import math

from pyecharts import Line3D

REMOTE_HOST = "https://pyecharts.github.io/assets/js"

# Create your views here.

io = stdDBIO("960911nbrNBR",mode=CONNECTOR_READWRITE)

all_transaction = [] # act as a buffer
def pullData():
    global io,all_transaction
    io.setDB(Transaction.dbname)
    io.setCollection(Transaction.collection)

    all_objects = io.readObjs()
    # print(all_objects)

    # all_transaction = list(map(lambda ob:Transaction(**(ob['content']),id=str(ob["_id"])),all_objects))
    all_transaction = []
    [all_transaction.append(Transaction(**(ob['content']), id=str(ob["_id"]))) for ob in all_objects]

    # [print(t,t.id) for t in all_transaction]

    # all_tags = reduce(lambda x, y: x.obj["tags"].union(y.obj["tags"]), all_transaction)

    all_transaction = sorted(all_transaction,
                             key=lambda k: k.obj["timestamp"], reverse=True)
def index(request):

    # by default, the page will shows user a graph with the transaction activity in recent
    # user can change the visualization method
    # user can choose to enter the recorder app to input new transaction
    # user will be able to delete their old transactions and update them by entering new ones

    # the password will be stored in cookie later

    pullData()

    template = loader.get_template('index.html')

    context_list = []
    for obj in all_transaction:
        context_list.append({
            "key":obj.id,
            "value":{
                "timestamp":obj.get_time(),
                "amount":obj.obj["amount"],
                "tags":obj.obj["tags"],
                "description":obj.obj["description"]
            }
        })


    context = {
        'all_transaction': context_list,
    }


    #return render_to_response('index.html',context)
    return HttpResponse(template.render(context,request))

def list_cata(request,catagory):
    if len(all_transaction)==0:
        pullData()


    template = loader.get_template('cata_list.html')

    context_list = []
    for obj in all_transaction:
        if catagory in obj.obj["tags"]:
            context_list.append({
                "key": obj.id,
                "value": {
                    "timestamp": obj.get_time(),
                    "amount": obj.obj["amount"],
                    "tags": obj.obj["tags"],
                    "description": obj.obj["description"]
                }
            })

    context = {
        'all_transaction': context_list,
        "filtered":"filtered"
    }

    # return render_to_response('index.html',context)
    return HttpResponse(template.render(context, request))


def cata_fin(request):
    if len(all_transaction)==0:
        pullData()
    cataViz = AggregateByCategory()
    context = {
        "Viz": cataViz.render_embed(),
        "host": REMOTE_HOST,
        "script_list": cataViz.get_js_dependencies(),
        "title":"Category Summary"
    }
    template = loader.get_template('viz_template.html')
    return HttpResponse(template.render(context, request))
def AggregateByCategory():

    bar = Bar()
    catas = list(style.keys())
    static = {}

    static_num = {}
    for tx in all_transaction:
        for tag in tx.obj["tags"]:
            if tag not in static:
                static[tag] = 0
                static[tag+"-"] = 0
                static_num[tag] = 0
            if tx.obj["amount"]>=0:
                static[tag] += tx.obj["amount"]
            else:
                static[tag+"-"] -= tx.obj["amount"]

            static_num[tag]+=1
    catas_value = []
    catas_value_minus = []
    catas_num = []
    for cata in catas:
        catas_value_minus.append(static[cata+"-"])
        catas_value.append(static[cata])
        catas_num.append(static_num[cata])
    bar.add("gain", catas, catas_value,mark_line=["average"],xaxis_interval=0, xaxis_rotate=30, yaxis_rotate=30,yaxis_formatter="$")
    bar.add("cost", catas, catas_value_minus, mark_line=["average"], xaxis_interval=0, xaxis_rotate=30, yaxis_rotate=30,yaxis_formatter="$")

    line = Line()
    line.add("tx_number", catas, catas_num,mark_line=["average"])
    #bar.add("number",catas,catas_num,mark_line=["average"],mark_point=["max","min"])
    overlap = Overlap(width='100%', height='100%')
    overlap.add(bar)
    overlap.add(line, yaxis_index=1, is_add_yaxis=True)
    return overlap

def dyna_fin(request):
    if len(all_transaction)==0:
        pullData()
    dynamViz = categorical_dynamic_change()
    context = {
        "Viz": dynamViz.render_embed(),
        "script_list": dynamViz.get_js_dependencies(),
        "host": REMOTE_HOST,
        "title": "Monthly Dynamic"
    }
    template = loader.get_template('viz_template.html')
    return HttpResponse(template.render(context, request))
def categorical_dynamic_change():

    result = {}
    attr = []
    for tx in all_transaction:
        key = tx.get_year()+"-"+tx.get_month()

        if key not in result:
            attr.append(key)
            result[key]={}
            for tag in style.keys():
                result[key][tag] = 0

        for tag in tx.obj["tags"]:

            result[key][tag] += abs(tx.obj["amount"])


    attr.reverse()

    res = {}

    for t in attr:
        for tag in style.keys():
            if tag not in res:
                res[tag]=[]

            res[tag].append(result[t][tag])


    bar = Bar(width='100%', height='100%')
    cata = list(style.keys())
    for i in range(len(cata)):
        color = 1/(i+0.000000000001)
        bar.add(cata[i], attr, res[cata[i]], is_stack=True,is_label_show=False, is_datazoom_show=True,yaxis_formatter="$")
    return bar


def week_fin(request):
    if len(all_transaction)==0:
        pullData()
    weekViz = weekday_analysis()
    context = {
        "Viz": weekViz.render_embed(),
        "script_list": weekViz.get_js_dependencies(),
        "host": REMOTE_HOST,
        "title": "Week3D"
    }
    template = loader.get_template('viz_template.html')
    return HttpResponse(template.render(context, request))
def weekday_analysis():
    x_axis = list(style.keys())
    y_axis = [
         "Sunday","Saturday", "Friday", "Thursday", "Wednesday", "Tuesday", "Monday"
    ]
    y_axis.reverse()
    range_color = ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf',
                   '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
    result = {}
    for weekday in y_axis:
        result[weekday]={}
        for tag in x_axis:
            result[weekday][tag]=0

    for tx in all_transaction:
        weekday = y_axis[datetime.datetime.fromtimestamp(tx.obj["timestamp"]).weekday()]
        for tag in tx.obj["tags"]:
            result[weekday][tag]+=abs(tx.obj["amount"])
    data=[]
    max_value=0
    for i,weekday in enumerate(y_axis):
        for j,tag in enumerate(x_axis):
            if result[weekday][tag]>max_value:
                max_value=result[weekday][tag]
            data.append([i,j,result[weekday][tag]])



    bar3d = Bar3D("You can see how much you spent on each category on each weekday", width="100%", height="100%")
    bar3d.add("", x_axis, y_axis, [[d[1], d[0], d[2]] for d in data],
              is_visualmap=True, visual_range=[0,max_value],
              visual_range_color=range_color, grid3d_width=200, grid3d_depth=80,grid3d_shading='lambert',xaxis_interval=10, xaxis_rotate=30, yaxis_rotate=30)
    return bar3d



    # cell = [yindex,xindex,value]


def timeRiverAnalysis():
    data=[]
    buffer={}
    for tx in all_transaction:
        time = tx.get_time().replace("-", "/")
        if time not in buffer:
            buffer[time] = {}
        for tag in tx.obj["tags"]:
            if tag not in buffer[time]:
                buffer[time][tag] = 0
            buffer[time][tag] += abs(tx.obj["amount"])
    for time in buffer:
        for tag in buffer[time]:
            data.append([time,buffer[time][tag],tag])
    print(data)


    tr = ThemeRiver("how you dynamically spend money one each category")
    tr.add(list(style.keys()), data, is_label_show=True)
    #tr.add(['DQ', 'TY', 'SS', 'QG', 'SY', 'DD'], data, is_label_show=True)
    #tr.render()

    return tr

def engel_fin(request):
    if len(all_transaction)==0:
        pullData()
    engelViz = EngelIndex()
    context = {
        "Viz": engelViz.render_embed(),
        "script_list": engelViz.get_js_dependencies(),
        "host": REMOTE_HOST,
        "title": "Engel Index"
    }
    template = loader.get_template('viz_template.html')
    return HttpResponse(template.render(context, request))

def EngelIndex():
    food_paid = {}
    total_paid = {}
    all_time = []
    for tx in all_transaction:
        if tx.obj["amount"]>0:
            continue
        time = tx.get_year()+"-"+tx.get_month()
        if time not in food_paid:
            food_paid[time]=0
            total_paid[time] = 0
            all_time.append(time)

        total_paid[time] += abs(tx.obj["amount"])
        if "food" in tx.obj["tags"]:
            food_paid[time]+= abs(tx.obj["amount"])

    data = []
    all_time.reverse()
    for t in all_time:
        data.append(round(food_paid[t]/total_paid[t],3))

    line = Line("Engel Index",width="100%",height="100%")

    line.add("Food/Total Pay", all_time,data, is_smooth=True,
             is_label_show=True)

    line.add("Very Rich",all_time,[0.3 for d in data],is_smooth=True)
    line.add("Rich", all_time, [0.4 for d in data],is_smooth=True)
    line.add("Well off", all_time, [0.5 for d in data],is_smooth=True)
    line.add("Just Enough", all_time, [0.6 for d in data], is_smooth=True)

    return line




def recorder(request):
    return render(request, 'recorder.html')

def delete_tx(request):
    global io
    if request.method == "POST":
        io.deleteWithObid(request.POST["oid"])
        #print(oid)
        return HttpResponseRedirect('../')
    else:
        #print(oid)
        raise Http404("Page Does not exist!")
def add_txs(request):
    global io
    if request.method=="POST":

        times = request.POST.getlist("time",[])
        amount=request.POST.getlist("amount",[])
        tags = request.POST.getlist("tags",[])
        description = request.POST.getlist("description",[])
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
        return HttpResponseRedirect('../')
    else:
        raise Http404("Page Does not exist!")
    #return  render_to_response('test.html',{"attr":txs},RequestContext(request))

def intro_page(request):
    template = loader.get_template('intro.html')
    return HttpResponse(template.render({}, request))