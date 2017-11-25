import logging
import random
from decimal import Decimal
from datetime import datetime

from transactions.models import Transaction


class TransactionBuilder:
    next_static_id = 1

    def __init__(self):
        self.transaction = Transaction()

        self.transaction.date = self.__random_date__()
        self.transaction.description = self.__random_string__()
        self.transaction.amount = self.__random_decimal__()
        self.transaction.current_balance = self.__random_decimal__()
        self.transaction.date_imported = self.__random_date__()
        self.transaction.custom_date_1 = self.__random_date__()
        self.transaction.custom_text_1 = self.__random_string__()

    def with_date(self, date):
        self.transaction.date = date
        return self

    def with_amount(self, amount):
        self.transaction.amount = amount
        return self

    def with_random_notes(self):
        self.transaction.notes = self.__random_string__()
        return self

    def with_transaction_label(self, transaction_label):
        self.transaction.transaction_label = transaction_label
        return self

    def for_bank_account(self, bank_account):
        self.transaction.bank_account = bank_account
        return self

    def build(self, persist=False):
        if persist:
            assert self.transaction.bank_account is not None
            assert self.transaction.transaction_label is None\
                or self.transaction.transaction_label.id > 0
            self.transaction.save()
        else:
            self.transaction.id = TransactionBuilder.next_static_id
            TransactionBuilder.next_static_id += 1
        logging.getLogger(__name__).info("TransactionBuilder: Created test transaction with id " + str(self.transaction.id))
        return self.transaction

    def __random_string__(self):
        number_of_words = random.randrange(4, 7)
        string = random.choice(TransactionBuilder.words)
        i = 1
        while i < number_of_words:
            string += ' ' + random.choice(TransactionBuilder.words)
            i += 1

        return string

    def __random_date__(self):
        start = datetime.strptime("01/01/09", '%d/%m/%y')
        end = datetime.strptime("01/01/16", '%d/%m/%y')
        return (start + (end - start) * random.random()).date()

    def __random_decimal__(self):
        value = random.randrange(-10000, 10000) / 100
        return Decimal("{:0.2f}".format(value))

    words = [
        'pub',
        'eggs',
        'beer',
        'bank',
        'transfer',
        'pay',
        'holiday',
        'payment',
        'loans',
        'the red lion',
        'the',
        'of',
        'a',
        'test',
        'fee',
        'expense'
    ]
