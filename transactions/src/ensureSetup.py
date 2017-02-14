from transactions.models import BankAccount, TransactionLabel, AccountTemplate

def getBuiltInItem(cls, id):
    try:
        return cls.objects.get(pk=id)
    except cls.DoesNotExist:
        newItem = cls()
        newItem.id = id
        return newItem

manualTemplate = getBuiltInItem(AccountTemplate, -1)
manualTemplate.Name = "Manual"
manualTemplate.IsBuiltIn = True
manualTemplate.DateGetter = "datetime.strptime(row['Date'], '%d %b %Y')"
manualTemplate.DescriptionGetter = "row['Description']"
manualTemplate.AmountGetter = "float(row['Amount'])"
manualTemplate.CurrentBalanceGetter = "None"
manualTemplate.OtherDate1Name = None
manualTemplate.OtherDate1Getter = "None"
manualTemplate.OtherString1Name = None
manualTemplate.OtherString1Getter = "None"
manualTemplate.save()

halifax = getBuiltInItem(AccountTemplate, -2)
halifax.Name = "Halifax"
halifax.IsBuiltIn = True
halifax.DateGetter = "datetime.strptime(row['Date'], '%d/%m/%y')"
halifax.DescriptionGetter = "row['Description']"
halifax.AmountGetter = "-float(row['Amount'])"
halifax.CurrentBalanceGetter = "None"
halifax.OtherDate1Name = "Date entered"
halifax.OtherDate1Getter = "datetime.strptime(row['Date entered'], '%d/%m/%y')"
halifax.OtherString1Name = "Reference"
halifax.OtherString1Getter = "row['Reference']"
halifax.save()

natwest = getBuiltInItem(AccountTemplate, -3)
natwest.Name = "Natwest"
natwest.IsBuiltIn = True
natwest.DateGetter = "datetime.strptime(row['Date'], '%d %b %Y')"
natwest.DescriptionGetter = "row['Description']"
natwest.AmountGetter = "float(row['Value'])"
natwest.CurrentBalanceGetter = "float(row['Balance'])"
natwest.OtherDate1Name = None
natwest.OtherDate1Getter = "None"
natwest.OtherString1Name = "Type"
natwest.OtherString1Getter = "row['Type']"
natwest.save()

manual = getBuiltInItem(BankAccount, -1)
manual.AccountHumanName = 'Manual'
manual.AccountType = 'CurrentAccount'
manual.AccountNumber = ''
manual.SortCode = ''
manual.IsActive = True
manual.Template = manualTemplate
manual.save()


transfer = getBuiltInItem(TransactionLabel, -1)
transfer.Name = 'Transfer'
transfer.save()

