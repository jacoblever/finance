import random
import uuid
from decimal import Decimal
from datetime import datetime

from transactions.models import Transaction


class TransactionBuilder:
    def __init__(self):
        self.transaction = Transaction()

        self.transaction.date = self.__random_date__()
        self.transaction.description = self.__random_string__()
        self.transaction.amount = self.__random_decimal__()
        self.transaction.current_balance = self.__random_decimal__()
        self.transaction.date_imported = self.__random_date__()
        self.transaction.custom_date_1 = self.__random_date__()
        self.transaction.custom_text_1 = self.__random_string__()

    def build(self, persist=True):
        if persist:
            assert self.transaction.bank_account is not None
            self.transaction.save()
            print("TransactionBuilder: Created test transaction with id " + str(self.transaction.id))
        return self.transaction

    def __random_string__(self):
        return str(uuid.uuid4())

    def __random_date__(self):
        start = datetime.strptime("01/01/01", '%d/%m/%y')
        end = datetime.strptime("01/01/16", '%d/%m/%y')
        return (start + (end - start) * random.random()).date()

    def __random_decimal__(self):
        value = random.randrange(10000) / 100
        return Decimal("{:0.2f}".format(value))
