from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView
from django.db.models import Count
from datetime import datetime
from django.core.urlresolvers import reverse

from transactions.models import Transaction
from .forms import ImportForm, TransactionFilterForm, TransactionForm, ManualForm, BankAccountForm, AccountTemplateForm
from .models import BankAccount, BankAccountTemplate
from .src.import_transactions import import_transactions
from .src.filter import apply_filter
from .src.graph import make_graph
import uuid

import urllib
import math
from datetime import datetime


def import_(request):
    if request.method == 'POST':
        form = ImportForm(request.POST, request.FILES)
        actually_import = request.POST.get('actually-import') == 'true'
        if actually_import:
            output = import_transactions(form, actually_import)
            return render(
                request,
                'transactions/import-result.html',
                {'total_count': output[0],
                 'potential_duplicates': None,
                 'existing_count': output[2],
                 'problems': []})
        else:
            output = import_transactions(form, actually_import)
            return render(
                request,
                'transactions/import-result.html',
                {'total_count': output[0],
                 'potential_duplicates': output[1],
                 'existing_count': output[2],
                 'problems': output[3]})
    else:
        form = ImportForm()
        return render(request, 'transactions/import.html', {'form': form})


def manual(request, id_=None):
    existing = Transaction.objects.get(pk=id_) if id_ != None else None
    if existing != None and existing.bank_account.id != -1:
        raise Exception('You sould not be editing an imported transaction')
    if request.method != 'POST':
        form = ManualForm(instance=existing)
        return render(
            request,
            'transactions/manual.html',
            {'form': form, 'adding_new_transaction': id_ is None})
    else:
        if request.POST.get('delete') == 'true':
            existing.delete()
        else:
            form = ManualForm(request.POST, instance=existing)
            transaction = form.save(commit=False)
            if existing == None:
                transaction.bank_account = BankAccount.objects.get(pk=-1)
                transaction.date_imported = datetime.now()
            transaction.save()
        return_url = request.POST.get('return-url')
        return redirect(return_url if return_url != '' else reverse('home'))


def edit_account(request, id_=None):
    bank_account = BankAccount.objects.get(pk=id_) if id_ != None else None
    if id_ != None and bank_account.id < 0:
        raise Exception('You should not be editing a built in account')
    original_has_custom_template = bank_account is not None and not bank_account.bank_account_template.is_built_in
    custom_account_template = bank_account.bank_account_template if original_has_custom_template else None
    if request.method != 'POST':
        template_id = "custom" if original_has_custom_template else\
            (bank_account.bank_account_template.id if bank_account is not None else "")
        account_form = BankAccountForm(initial={'template': template_id}, instance=bank_account)
        template_form = AccountTemplateForm(instance=custom_account_template)
        return render(
            request,
            'transactions/edit_account.html',
            {
                'account_form': account_form,
                'adding_new_account': id_ is None,
                'template_form': template_form
            })
    else:
        if request.POST.get('delete') == 'true':
            template = bank_account.bank_account_template
            bank_account.delete()
            if not template.is_built_in:
                template.delete()
        else:
            account_form = BankAccountForm(request.POST, instance=bank_account)
            result_has_custom_template = request.POST.get('template') == 'custom'
            if result_has_custom_template:
                template_form = AccountTemplateForm(request.POST, instance=custom_account_template)
                custom_account_template = template_form.save(commit=False)
                if custom_account_template.name == '':
                    custom_account_template.name = uuid.uuid4()
                custom_account_template.save()

            bank_account = account_form.save(commit=False)
            bank_account.bank_account_template = custom_account_template if result_has_custom_template\
                else BankAccountTemplate.objects.get(pk=request.POST.get('template'))
            bank_account.save()

            if original_has_custom_template and not result_has_custom_template:
                custom_account_template.delete()
        return redirect(reverse('accounts'))


class TransactionsView(ListView):
    template_name="transactions/index.html"

    def __init__(self):
        self.pageSize = 50
    
    def get_filter_form(self):
        return TransactionFilterForm(self.request.GET)

    def get_queryset(self):
        form = TransactionFilterForm(self.request.GET)
        filtered = apply_filter(form)

        if(form.is_paged()):
            page = form.get_page()
            start = (page-1)*self.pageSize
            end = start + self.pageSize
            filtered = filtered[start:end]
        
        return [[x, TransactionForm(prefix=x.id, instance=x)]
                for x
                in filtered]

    def get_context_data(self, **kwargs):
        context = super(TransactionsView, self).get_context_data(**kwargs)
        form = TransactionFilterForm(self.request.GET)
        accounts = form.get_account()
        if accounts != None and len(accounts) == 1:
            context['single_account'] = BankAccount.objects.get(pk=accounts[0])
        else:
            context['single_account'] = None

        context['bulk_form'] = TransactionForm()
        context['total_found'] = len(apply_filter(form))
        if form.is_paged():
            context['page'] = form.get_page()
            total_pages = math.ceil(context['total_found']/self.pageSize)
            context['pages'] = range(1, total_pages + 1)
        return context

    
class TransactionsDownloadView(TransactionsView):
    template_name="transactions/download.html"

    def get(self, request, *args, **kwargs):
        response = super(TransactionsView, self).get(request,*args,**kwargs)
        response['Content-Disposition'] = 'attachment; filename="data.csv"'
        return response


def save_labels(request):
    if request.method == 'POST':
        ids = request.POST.getlist('id')
        for id in ids:
            form = TransactionForm(
                request.POST,
                prefix=id,
                instance=Transaction.objects.get(pk=id))
            form.save();
        return redirect("../")
    else:
        return HttpResponse('Error: This should be a POST request')


class PastImportsView(ListView):
    template_name="transactions/past-imports.html"
    
    def get_filter_form(self):
        return TransactionFilterForm(self.request.GET)

    def get_queryset(self):
        return [
            (
                x['date_imported'].strftime('%H:%M:%S - %d %B %Y'),
                x['count'],
                x['date_imported'].strftime("%Y-%m-%d_%H:%M:%S.%f")
            )
            for x
            in Transaction.objects.all().values('date_imported').annotate(count=Count('id')).order_by('-date_imported')
            ]


def delete_past_import(request):
    if request.method == 'POST':
        to_delete = datetime.strptime(request.POST.get('datetime'), '%Y-%m-%d_%H:%M:%S.%f')
        Transaction.objects.all().filter(date_imported=to_delete).delete()
        return HttpResponse('Done')
    else:
        return HttpResponse('Error: This should be a POST request')


def graph(request):
    return make_graph(request)
