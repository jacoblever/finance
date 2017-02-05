import csv
from io import TextIOWrapper
from transactions.models import BankAccount, BankTransaction, TransactionLabel
from datetime import datetime
from decimal import Decimal

def uploadTransactions(form, actuallyUpload):
    TransactionIdCol = 'TransactionId'
    AccountIdCol = 'AccountId'
    
    text = TextIOWrapper(form.getFile().file, encoding='ISO-8859-1')
    spamreader = csv.DictReader(text)
    duplicates = BankTransaction.objects.none()
    duplicatesSoFar = list(BankTransaction.objects.none())
    labels = TransactionLabel.objects.all()
    account = BankAccount.objects.get(pk=form.getAccount()) if form.getAccount() != '' else None
    now = datetime.now()
    problems = []

    existingCount = 0
    count = 0
    for row in spamreader:
        count += 1
        transaction = BankTransaction()
        existingTransaction = False
        if TransactionIdCol in row and row[TransactionIdCol] != "":
            id = int(row[TransactionIdCol])
            transaction = BankTransaction.objects.get(pk=id)
            newTemp = BankTransaction()
            populateBankTransactionInfo(newTemp, row, getReimportAccount())
            if transaction.Account.id != int(row['AccountId']):
                problems.append(str(id) + ": Account id changed " + str(transaction.Account.id) + " != " + row['AccountId'])
            for problem in checkBankTransactionInfoConsistency(transaction, newTemp):
                problems.append(str(id) + ": " + problem)
            existingTransaction = True
            existingCount += 1
        else:           
            transaction.Account = account
            transaction.DateUploaded = now
            if account == None:
                problems.append("Could not parse transaction: Please select an account")
            else:
                try:
                    populateBankTransactionInfo(transaction, row, account)
                except Exception as e:
                    problems.append("Could not parse transaction: '" + str(e) + "'")

        populateMetaTransactionInfo(transaction, row, labels)

        if actuallyUpload:
            if len(problems) > 0:
                raise Exception("Cannot save if there are problems")
            transaction.save()
        else:
            if not existingTransaction:
                duplicates = duplicates | BankTransaction.objects.all().filter(
                    Date = transaction.Date,
                    Description = transaction.Description,
                    Amount = transaction.Amount,
                    CurrentBalance = transaction.CurrentBalance,
                    OtherDate1 = transaction.OtherDate1,
                    OtherString1 = transaction.OtherString1,
                    )
            if count % 50 == 0:
                duplicatesSoFar = duplicatesSoFar + list(duplicates)
                duplicates = BankTransaction.objects.none()
    
    duplicatesSoFar = duplicatesSoFar + list(duplicates)
    return (count, list(duplicatesSoFar), existingCount, problems)

def checkBankTransactionInfoConsistency(t1, t2):
    problems = []
    test(problems, t1, t2, lambda x: x.Date.strftime('%m/%d/%Y'))
    test(problems, t1, t2, lambda x: x.Description)
    test(problems, t1, t2, lambda x: x.Amount)
    test(problems, t1, t2, lambda x: x.CurrentBalance)
    test(problems, t1, t2, lambda x: None if x.OtherDate1 == None else x.OtherDate1.strftime('%m/%d/%Y'))
    test(problems, t1, t2, lambda x: x.OtherString1)
    return problems

def test(problems, t1, t2, lam):
    if lam(t1) != lam(t2):
        problems.append("'" + str(lam(t1))  + "' != '" + str(lam(t2) + "'"))

def getReimportAccount():
    account = BankAccount()

    account.ColumnDate = "datetime.strptime(row['Date'], '%d %b %Y')"
    account.ColumnDescription = "row['Description']"
    account.ColumnAmount = "Decimal(row['Amount'])"
    account.ColumnCurrentBalance = "None if row['CurrentBalance'] == '' else Decimal(row['CurrentBalance'])"
    account.ColumnOtherDate1 = "None if row['OtherDate1'] == '' else datetime.strptime(row['OtherDate1'], '%d %b %Y')"
    account.ColumnOtherString1 = "row['OtherString1']"

    return account

def populateBankTransactionInfo(transaction, row, account):
    transaction.Date = eval(account.ColumnDate)
    transaction.Description = eval(account.ColumnDescription)
    transaction.Amount = eval(account.ColumnAmount)
    transaction.CurrentBalance = eval(account.ColumnCurrentBalance)
    transaction.OtherDate1 = eval(account.ColumnOtherDate1)
    transaction.OtherString1 = eval(account.ColumnOtherString1)

def populateMetaTransactionInfo(transaction, row, labels):
    LabelCol = 'Label'
    NotesCol = 'Notes'

    transaction.Notes = ''
    
    if LabelCol in row:
        labelText = row[LabelCol]
        if(labelText != None and labelText != ''):
            label = next((x for x in labels if x.Name == labelText), None)
            if(label != None):
                transaction.Label = label
            else:
                transaction.Notes = labelText

    if NotesCol in row:
        notes = row[NotesCol]
        if(notes != None and notes != ''):
            if(transaction.Notes != None and transaction.Notes != ''):
                transaction.Notes = transaction.Notes + ', ' + notes
            else:
                transaction.Notes = notes

