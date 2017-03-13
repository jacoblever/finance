from django.contrib import admin

from transactions.models import BankAccount, Transaction, TransactionLabel, BankAccountTemplate

admin.site.register(BankAccount)
admin.site.register(Transaction)
admin.site.register(TransactionLabel)
admin.site.register(BankAccountTemplate)
