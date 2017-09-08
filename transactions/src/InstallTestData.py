import random

from decimal import Decimal

from tests.builders import TransactionBuilder
from transactions.models import BankAccount, TransactionLabel, BankAccountTemplate, Transaction

current_account = BankAccount()
current_account.name = 'Current Account'
current_account.account_type = 'CurrentAccount'
current_account.more_details = ''
current_account.is_active = True
current_account.bank_account_template = BankAccountTemplate.objects.get(pk=-3)
current_account.save()

credit_card = BankAccount()
credit_card.name = 'Credit Card'
credit_card.account_type = 'CreditCard'
credit_card.more_details = ''
credit_card.is_active = True
credit_card.bank_account_template = BankAccountTemplate.objects.get(pk=-2)
credit_card.save()

savings_account = BankAccount()
savings_account.name = 'Savings'
savings_account.account_type = 'CurrentAccount'
savings_account.more_details = ''
savings_account.is_active = True
savings_account.bank_account_template = BankAccountTemplate.objects.get(pk=-3)
savings_account.save()

TransactionLabel.create('Drinks').save()
TransactionLabel.create('Food').save()
TransactionLabel.create('Travel').save()
TransactionLabel.create('Eggs').save()
TransactionLabel.create('Rent').save()
TransactionLabel.create('Utilities').save()

transaction_labels = [x for x in list(TransactionLabel.objects.all()) if not x.is_built_in()]


def create_transactions(account, quantity, labels):
    i = 0
    transactions = []
    while i < quantity:
        builder = TransactionBuilder() \
            .for_bank_account(account)
        if i % 3 == 0 or i % 3 == 1:
            builder.with_random_notes()
        if i % 5 == 0 or i % 5 == 1 or i % 5 == 2:
            builder.with_transaction_label(random.choice(labels))
        transactions.append(builder.build())
        i += 1
    Transaction.objects.bulk_create(transactions)


create_transactions(credit_card, 4000, transaction_labels)
create_transactions(current_account, 4000, transaction_labels)
create_transactions(savings_account, 2000, transaction_labels)


def create_transfer_transaction(account1, account2, amount, labels):
    builder1 = TransactionBuilder() \
        .for_bank_account(account1)
    if random.randrange(2) == 1:
        builder1.with_random_notes()
    if random.randrange(3) == 1:
        builder1.with_transaction_label(random.choice(labels))
    first = builder1.build()
    yield first
    builder2 = TransactionBuilder() \
        .for_bank_account(account2) \
        .with_amount(-first.amount) \
        .with_date(first.date)
    if random.randrange(2) == 1:
        builder2.with_random_notes()
    if random.randrange(3) == 1:
        builder2.with_transaction_label(random.choice(labels))
    yield builder2.build()


def random_decimal():
    value = random.randrange(10000) / 100
    return Decimal("{:0.2f}".format(value))


internalTransfer = TransactionLabel.objects.get(pk=-1)
transactions = []
i = 0
while i < 100:
    accounts = random.sample({current_account, credit_card, savings_account}, 2)
    pair = list(create_transfer_transaction(accounts[0], accounts[1], random_decimal(), transaction_labels))
    if i % 2 == 0:
        pair[0].transaction_label = internalTransfer
        pair[1].transaction_label = internalTransfer
    transactions.extend(pair)
    i += 1

Transaction.objects.bulk_create(transactions)
