from django.contrib import admin

from transactions.models import BankAccount, BankTransaction, TransactionLabel, AccountTemplate

admin.site.register(BankAccount)
admin.site.register(BankTransaction)
admin.site.register(TransactionLabel)
admin.site.register(AccountTemplate)
