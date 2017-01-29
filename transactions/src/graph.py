import csv
from io import TextIOWrapper
from transactions.models import BankAccount, BankTransaction, TransactionLabel
from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect
from datetime import timedelta
from itertools import groupby

def makeGraph(request):
    dayString = request.GET.get('day')
    day = 0
    if(dayString != None and dayString != ''):
        day = int(dayString)
    
    transactions = BankTransaction.objects.all()
    labels = list(TransactionLabel.objects.all())

    dates = [(x, (x.Date - timedelta(days=x.Date.weekday()-day))) for x in transactions]
    
    string = 'date\t' + '\t'.join([x.__str__() for x in labels])
    sortedDates = sorted(dates, key=lambda x: x[1])
    for date, items in groupby(sortedDates, key=lambda x: x[1]):
        a = list(items)
        string = string + '\n' + date.__str__()
        for label in labels:
            amounts = [-x[0].Amount for x in a if x[0].Label == label]
#            string = string + '\t' + sum(amounts).__str__()
            string = string + '\t' + sum(amounts).__str__()
    return HttpResponse(string)
