import logging
import uuid

from .TransactionBuilder import TransactionBuilder
from .BankAccountTemplateBuilder import BankAccountTemplateBuilder, FileOutput, StringOutput, IOutput


class TransactionFileBuilder:
    def __init__(self):
        self.transactions = None
        self.file_name = "tests/files/" + str(uuid.uuid4()) + ".txt"
        self.writer = None

    @classmethod
    def for_import(cls):
        builder = TransactionFileBuilder()
        builder.writer = BankAccountTemplateBuilder.write_transactions_to_file
        return builder

    @classmethod
    def for_download(cls):
        builder = TransactionFileBuilder()
        builder.writer = BankAccountTemplateBuilder.write_transactions_to_download_file
        return builder

    def with_transactions(self, transactions):
        self.transactions = transactions
        return self

    def with_random_transactions(self, count):
        self.transactions = self.__generate_transactions__(count)
        return self

    def build(self, persist_to_file: bool = False) -> IOutput:
        assert self.transactions is not None
        if persist_to_file:
            output = FileOutput(self.file_name)
        else:
            output = StringOutput()
        stream = output.open()
        self.writer(stream, self.transactions)
        logging.getLogger(__name__).info("TransactionFileBuilder: Created test file with "
                                         + str(len(self.transactions)) + " transaction(s)")
        if persist_to_file:
            stream.close()
        return output

    def __generate_transactions__(count):
        i = 0
        while i < count:
            yield TransactionBuilder().build()
            i += 1
