from transactions.models import BankAccount, TransactionLabel, AccountTemplate

halifaxCredit = BankAccount()
halifaxCredit.AccountHumanName = 'Halifax Credit'
halifaxCredit.AccountType = 'CreditCard'
halifaxCredit.AccountNumber = ''
halifaxCredit.SortCode = ''
halifaxCredit.IsActive = True
halifaxCredit.Template = AccountTemplate.objects.get(pk=-2)
halifaxCredit.save()

natwestCurrent = BankAccount()
natwestCurrent.AccountHumanName = 'Natwest Current'
natwestCurrent.AccountType = 'CurrentAccount'
natwestCurrent.AccountNumber = ''
natwestCurrent.SortCode = ''
natwestCurrent.IsActive = True
natwestCurrent.Template = AccountTemplate.objects.get(pk=-3)
natwestCurrent.save()

TransactionLabel.create('Supermarket').save()
TransactionLabel.create('Drinks').save()
TransactionLabel.create('Food').save()
TransactionLabel.create('Travel').save()
TransactionLabel.create('Coffee').save()
