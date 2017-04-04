import csv
from io import TextIOWrapper
from transactions.models import BankAccount, Transaction, TransactionLabel
from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect
from datetime import timedelta
from itertools import groupby


def make_graph(request):
    day_string = request.GET.get('day')
    day = 0
    if(day_string != None and day_string != ''):
        day = int(day_string)
    
    transactions = Transaction.objects.all()
    labels = list([x for x in TransactionLabel.objects.all() if not x.is_built_in()])

    dates = [(x, (x.date - timedelta(days=x.date.weekday()-day))) for x in transactions]
    
    string = 'date\t' + '\t'.join([x.__str__() for x in labels])
    sorted_dates = sorted(dates, key=lambda x: x[1])
    for date, items in groupby(sorted_dates, key=lambda x: x[1]):
        a = list(items)
        string = string + '\n' + date.__str__()
        for label in labels:
            amounts = [-x[0].amount for x in a if x[0].transaction_label == label]
            string = string + '\t' + sum(amounts).__str__()
    return HttpResponse(string)
