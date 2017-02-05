from transactions.models import BankAccount, TransactionLabel

def getManualAccount():
    try:
        return BankAccount.objects.get(pk=-1)
    except BankAccount.DoesNotExist:
        newItem = BankAccount()
        newItem.id = -1
        return newItem

manual = getManualAccount()
manual.AccountHumanName = 'Manual2'
manual.AccountType = 'CurrentAccount'
manual.AccountNumber = ''
manual.SortCode = ''
manual.IsActive = True

manual.ColumnDate = "datetime.strptime(row['Date'], '%d %b %Y')"
manual.ColumnDescription = "row['Description']"
manual.ColumnAmount = "float(row['Amount'])"
manual.ColumnCurrentBalance = "None"
manual.OtherDate1Name = None
manual.ColumnOtherDate1 = "None"
manual.OtherString1Name = None
manual.ColumnOtherString1 = "None"

manual.save()

def getTransferLabel():
    try:
        return TransactionLabel.objects.get(pk=-1)
    except TransactionLabel.DoesNotExist:
        newItem = TransactionLabel()
        newItem.id = -1
        return newItem

transfer = getTransferLabel()
transfer.Name = 'Transfer'
transfer.save()
