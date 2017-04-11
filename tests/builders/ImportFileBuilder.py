import os
import uuid

from tests.builders.TransactionBuilder import *
from tests.builders.BankAccountTemplateBuilder import *


class ImportFile:
    def __init__(self, file_path, transactions):
        self.file_path = file_path
        self.transactions = transactions

    def open(self):
        return open(self.file_path, "r")

    def delete_file(self):
        os.remove(self.file_path)


class ImportFileBuilder:
    def __init__(self):
        self.count = 1
        self.file_name = "tests/files/" + str(uuid.uuid4()) + ".txt"

    def number_of_transactions(self, count):
        self.count = count

    def build(self):
        transactions = []
        i = 0
        while i < self.count:
            transactions.append(TransactionBuilder().build(persist=False))
            i += 1
        BankAccountTemplateBuilder.write_transactions_to_file(self.file_name, transactions)
        return ImportFile(self.file_name, transactions)
