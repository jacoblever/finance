from transactions.models import BankAccount, BankTransaction, TransactionLabel
from transactions.forms import TransactionFilterForm
from datetime import datetime

def mathes(transactions, propFunc, formValue):
    if(formValue == None or (formValue != None and len(formValue) == 0)):
        return transactions
    else:
        return [x for x in transactions if (propFunc(x) in [int(x) for x in formValue])]

def mathesDate(transactions, condition, formValue):
    if(formValue != None and formValue != ''):
        parsedDate = datetime.strptime(formValue, '%Y-%m-%d').date()
        return [x for x in transactions if condition(x, parsedDate)]
    else:
        return transactions

def mathesText(transaction, text):
    notes = transaction.Notes
    if(notes == None):
        notes = ''
    return (text.lower() in transaction.Description.lower()
            or text.lower() in notes.lower())

def applyFilter(form):
    transactions = BankTransaction.objects.all()
    transactions = mathes(transactions, lambda x: x.Label_id, form.getLabel())
    transactions = mathes(transactions, lambda x: x.Account_id, form.getAccount())
    transactions = mathesDate(transactions, lambda x, date: x.Date >= date, form.getDateFrom())
    transactions = mathesDate(transactions, lambda x, date: x.Date <= date, form.getDateTo())
    text = form.getDescription()
    if text != None and text != '':
        transactions = [x for x in transactions if mathesText(x, text)]
    sortedTransactions = sorted(transactions, key=lambda x: x.Date)
    return sortedTransactions
