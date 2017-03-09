from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView
from django.db.models import Count
from datetime import datetime
from django.core.urlresolvers import reverse

from transactions.models import BankTransaction
from .forms import UploadForm, TransactionFilterForm, TransactionForm, ManualForm, BankAccountForm, AccountTemplateForm
from .models import BankAccount, AccountTemplate
from .src.upload import uploadTransactions
from .src.filter import applyFilter
from .src.graph import makeGraph
import uuid

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
                 'potentialDuplicates': None,
                 'existingCount': output[2],
                 'problems': []})
        else:
            output = uploadTransactions(form, actuallyUpload)
            return render(
                request,
                'transactions/upload-result.html',
                {'totalCount': output[0],
                 'potentialDuplicates': output[1],
                 'existingCount': output[2],
                 'problems': output[3]})
    else:
        form = UploadForm()
        return render(request, 'transactions/upload.html', {'form': form})

def manual(request, id=None):
    existing = BankTransaction.objects.get(pk=id) if id != None else None
    if existing != None and existing.Account.id != -1:
        raise Exception('You sould not be editing an imported transaction')
    if request.method != 'POST':
        form = ManualForm(instance=existing)
        return render(
            request,
            'transactions/manual.html',
            {'form': form, 'addingNewTransaction': id is None})
    else:
        if request.POST.get('delete') == 'true':
            existing.delete()
        else:
            form = ManualForm(request.POST, instance=existing)
            transaction = form.save(commit=False)
            if existing == None:
                transaction.Account = BankAccount.objects.get(pk=-1)
                transaction.DateUploaded = datetime.now()
            transaction.save()
        returnUrl = request.POST.get('return-url')
        return redirect(returnUrl if returnUrl != '' else reverse('home'))

def editAccount(request, id=None):
    bankAccount = BankAccount.objects.get(pk=id) if id != None else None
    if id != None and bankAccount.id < 0:
        raise Exception('You should not be editing a built in account')
    originalHasCustomTemplate = bankAccount is not None and not bankAccount.Template.IsBuiltIn
    customAccountTemplate = bankAccount.Template if originalHasCustomTemplate else None
    if request.method != 'POST':
        templateId = "custom" if originalHasCustomTemplate else\
            (bankAccount.Template.id if bankAccount is not None else "")
        accountForm = BankAccountForm(initial={'template': templateId}, instance=bankAccount)
        templateForm = AccountTemplateForm(instance=customAccountTemplate)
        return render(
            request,
            'transactions/edit_account.html',
            {
                'accountForm': accountForm,
                'addingNewAccount': id is None,
                'templateForm': templateForm
            })
    else:
        if request.POST.get('delete') == 'true':
            template = bankAccount.Template
            bankAccount.delete()
            if not template.IsBuiltIn:
                template.delete()
        else:
            accountForm = BankAccountForm(request.POST, instance=bankAccount)
            resultHasCustomTemplate = request.POST.get('template') == 'custom'
            if resultHasCustomTemplate:
                templateForm = AccountTemplateForm(request.POST, instance=customAccountTemplate)
                customAccountTemplate = templateForm.save(commit=False)
                if customAccountTemplate.Name == '':
                    customAccountTemplate.Name = uuid.uuid4()
                customAccountTemplate.save()

            bankAccount = accountForm.save(commit=False)
            bankAccount.Template = customAccountTemplate if resultHasCustomTemplate\
                else AccountTemplate.objects.get(pk=request.POST.get('template'))
            bankAccount.save()

            if originalHasCustomTemplate and not resultHasCustomTemplate:
                customAccountTemplate.delete()
        return redirect(reverse('accounts'))

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
        context['totalFound'] = len(applyFilter(form))
        if form.isPaged():
            context['page'] = form.getPage()
            totalPages = math.ceil(context['totalFound']/self.pageSize)
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
