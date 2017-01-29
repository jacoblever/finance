from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView
from django.db.models import Count

from transactions.models import BankTransaction
from .forms import UploadForm, TransactionFilterForm, TransactionForm
from .models import BankAccount
from .src.upload import uploadTransactions
from .src.filter import applyFilter
from .src.graph import makeGraph

import urllib
import math
from datetime import datetime

def upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        actuallyUpload = request.POST.get('actually-upload') == 'true'
        if(actuallyUpload):
            output = uploadTransactions(form, actuallyUpload)
            return render(
                request,
                'transactions/upload-result.html',
                {'totalCount': output[0],
                 'potentialDuplicates': None})
        else:
            output = uploadTransactions(form, actuallyUpload)
            return render(
                request,
                'transactions/upload-result.html',
                {'totalCount': output[0],
                 'potentialDuplicates': output[1]})
    else:
        form = UploadForm()
        return render(request, 'transactions/upload.html', {'form': form})

class TransactionsView(ListView):
    template_name="transactions/index.html"

    def __init__(self):
        self.pageSize = 50
    
    def getFilterForm(self):
        return TransactionFilterForm(self.request.GET)
    def get_queryset(self):
        form = TransactionFilterForm(self.request.GET)
        filtered = applyFilter(form)

        if(form.isPaged()):
            page = form.getPage()
            start = (page-1)*self.pageSize
            end = start + self.pageSize
            filtered = filtered[start:end]
        
        return [[x, TransactionForm(prefix=x.id, instance=x)]
                for x
                in filtered]

    def get_context_data(self, **kwargs):
        context = super(TransactionsView, self).get_context_data(**kwargs)
        form = TransactionFilterForm(self.request.GET)
        accounts = form.getAccount()
        if accounts != None and len(accounts) == 1:
            context['singleAccount'] = BankAccount.objects.get(pk=accounts[0])
        else:
            context['singleAccount'] = None

        context['bulkForm'] = TransactionForm()

        if form.isPaged():
            context['page'] = form.getPage()
            totalPages = math.ceil(len(applyFilter(form))/self.pageSize)
            context['pages'] = range(1, totalPages + 1)
        return context

    
class TransactionsDownloadView(TransactionsView):
    template_name="transactions/download.html"

    def get(self, request, *args, **kwargs):
        response = super(TransactionsView, self).get(request,*args,**kwargs)
        response['Content-Disposition'] = 'attachment; filename="data.csv"'
        return response

def saveLabels(request):
    if request.method == 'POST':
        ids = request.POST.getlist('id')
        for id in ids:
            form = TransactionForm(
                request.POST,
                prefix=id,
                instance=BankTransaction.objects.get(pk=id))
            form.save();
        return redirect("../")
    else:
        return HttpResponse('Error: This should be a POST request')

class PastUploadsView(ListView):
    template_name="transactions/past-uploads.html"
    
    def getFilterForm(self):
        return TransactionFilterForm(self.request.GET)
    def get_queryset(self):
        return [
            (
                x['DateUploaded'].strftime('%H:%M:%S - %d %B %Y'),
                x['count'],
                x['DateUploaded'].strftime("%Y-%m-%d_%H:%M:%S.%f")
            )
            for x
            in BankTransaction.objects.all().values('DateUploaded').annotate(count=Count('id')).order_by('-DateUploaded')
        ];

def deletePastUploads(request):
    if request.method == 'POST':
        toDelete = datetime.strptime(request.POST.get('datetime'), '%Y-%m-%d_%H:%M:%S.%f')
        BankTransaction.objects.all().filter(DateUploaded=toDelete).delete()
        return HttpResponse('Done')
    else:
        return HttpResponse('Error: This should be a POST request')

def graph(request):
    return makeGraph(request)
