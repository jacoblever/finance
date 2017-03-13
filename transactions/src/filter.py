from transactions.models import BankAccount, Transaction, TransactionLabel
from transactions.forms import TransactionFilterForm
from datetime import datetime


def matches(transactions, prop_func, form_value):
    if form_value == None or (form_value != None and len(form_value) == 0):
        return transactions
    else:
        # 0 means None (blank)
        return [x for x in transactions if (prop_func(x) in [(int(x) if x != "0" else None) for x in form_value])]


def matches_date(transactions, condition, form_value):
    if form_value != None and form_value != '':
        parsed_date = datetime.strptime(form_value, '%Y-%m-%d').date()
        return [x for x in transactions if condition(x, parsed_date)]
    else:
        return transactions


def transaction_matches_text(transaction, text):
    notes = transaction.notes
    if notes == None:
        notes = ''
    return (text.lower() in transaction.description.lower()
            or text.lower() in notes.lower())


def matches_text(transactions, text):
    if text != None and text != '':
        return [x for x in transactions if transaction_matches_text(x, text)]
    else:
        return transactions


def apply_filter(form):
    transactions = Transaction.objects.all()
    transactions = matches(transactions, lambda x: x.transaction_label_id, form.get_label())
    transactions = matches(transactions, lambda x: x.bank_account_id, form.get_account())
    transactions = matches_date(transactions, lambda x, date: x.date >= date, form.get_date_from())
    transactions = matches_date(transactions, lambda x, date: x.date <= date, form.get_date_to())
    transactions = matches_text(transactions, form.get_text())
    sorted_transactions = sorted(transactions, key=lambda x: x.date)
    return sorted_transactions
