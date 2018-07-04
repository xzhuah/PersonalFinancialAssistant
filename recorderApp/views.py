from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.



def index(request):
    ## user first enter a series of transactions, display a summary while entering

    ## when user click submit, the form will post the result to the database and redirect user to the reviewer

    ### a dynamic form asking for time, amount, labels, optional description, ...
    # there will be a calendar and default labels selection, personlized label should be allowed. ...
    # The generated label is based on used label which will be passed in as a parameter

    return HttpResponse("This is recorder app")

def add_transactions(request):

    tx_list = request.POST.getlist('txs')


