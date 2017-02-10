from transactions.models import BankAccount, BankTransaction, TransactionLabel
from transactions.forms import TransactionFilterForm
from datetime import datetime

def mathes(transactions, propFunc, formValue):
    if formValue == None or (formValue != None and len(formValue) == 0):
        return transactions
    else:
        # 0 means None (blank)
        return [x for x in transactions if (propFunc(x) in [(int(x) if x != "0" else None) for x in formValue])]

def mathesDate(transactions, condition, formValue):
    if formValue != None and formValue != '':
        parsedDate = datetime.strptime(formValue, '%Y-%m-%d').date()
        return [x for x in transactions if condition(x, parsedDate)]
    else:
        return transactions

def transactionMathesText(transaction, text):
    notes = transaction.Notes
    if notes == None:
        notes = ''
    return (text.lower() in transaction.Description.lower()
            or text.lower() in notes.lower())

def mathesText(transactions, text):
    if text != None and text != '':
        return [x for x in transactions if transactionMathesText(x, text)]
    else:
        return transactions

def applyFilter(form):
    transactions = BankTransaction.objects.all()
    transactions = mathes(transactions, lambda x: x.Label_id, form.getLabel())
    transactions = mathes(transactions, lambda x: x.Account_id, form.getAccount())
    transactions = mathesDate(transactions, lambda x, date: x.Date >= date, form.getDateFrom())
    transactions = mathesDate(transactions, lambda x, date: x.Date <= date, form.getDateTo())
    transactions = mathesText(transactions, form.getText())
    sortedTransactions = sorted(transactions, key=lambda x: x.Date)
    return sortedTransactions
