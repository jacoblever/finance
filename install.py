from transactions.models import BankAccount, TransactionLabel, BankAccountTemplate

halifax_credit = BankAccount()
halifax_credit.name = 'Halifax Credit'
halifax_credit.account_type = 'CreditCard'
halifax_credit.more_details = ''
halifax_credit.is_active = True
halifax_credit.bank_account_template = BankAccountTemplate.objects.get(pk=-2)
halifax_credit.save()

natwest_current = BankAccount()
natwest_current.name = 'Natwest Current'
natwest_current.account_type = 'CurrentAccount'
natwest_current.more_details = ''
natwest_current.is_active = True
natwest_current.bank_account_template = BankAccountTemplate.objects.get(pk=-3)
natwest_current.save()

TransactionLabel.create('Supermarket').save()
TransactionLabel.create('Drinks').save()
TransactionLabel.create('Food').save()
TransactionLabel.create('Travel').save()
TransactionLabel.create('Coffee').save()
