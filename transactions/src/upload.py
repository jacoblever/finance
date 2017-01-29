import csv
from io import TextIOWrapper
from transactions.models import BankAccount, BankTransaction, TransactionLabel
from datetime import datetime

def uploadTransactions(form, actuallyUpload):
    text = TextIOWrapper(form.getFile().file, encoding='utf-8')
    spamreader = csv.DictReader(text)
    duplicates = BankTransaction.objects.none()
    duplicatesSoFar = list(BankTransaction.objects.none())
    labels = TransactionLabel.objects.all()
    account = BankAccount.objects.get(pk=form.getAccount())
    now = datetime.now()

    count = 0
    for row in spamreader:
        count += 1
        transaction = BankTransaction()
        transaction.Account = account
        
        transaction.Date = eval(account.ColumnDate)
        transaction.Description = eval(account.ColumnDescription)
        transaction.Amount = eval(account.ColumnAmount)
        transaction.CurrentBalance = eval(account.ColumnCurrentBalance)

        if 'Label' in row:
            labelText = row['Label']
            if(labelText != None and labelText != ''):
                label = next((x for x in labels if x.Name == labelText), None)
                if(label != None):
                    transaction.Label = label
                else:
                    transaction.Notes = labelText

        if 'Notes' in row:
            notes = row['Notes']
            if(notes != None and notes != ''):
                if(transaction.Notes != None and transaction.Notes != ''):
                    transaction.Notes = transaction.Notes + ', ' + notes
                else:
                    transaction.Notes = notes


        transaction.OtherDate1 = eval(account.ColumnOtherDate1)
        transaction.OtherString1 = eval(account.ColumnOtherString1)
        transaction.DateUploaded = now
        
        if(actuallyUpload):
            transaction.save()
        else:
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
    return (count, list(duplicatesSoFar))
