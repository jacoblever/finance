import logging
import os
from io import StringIO

from transactions.models import BankAccountTemplate


class BankAccountTemplateBuilder:
    next_static_id = 1

    def __init__(self):
        self.template = BankAccountTemplate()
        self.template.name = "Test bank account template"
        self.template.is_built_in = False
        self.template.get_date = "datetime.strptime(row['Date'], '%d/%m/%y')"
        self.template.get_description = "row['Description']"
        self.template.get_amount = "float(row['Amount'])"
        self.template.get_current_balance = "float(row['CurrentBalance'])"
        self.template.custom_date_1_name = "Custom Date 1"
        self.template.get_custom_date_1 = "datetime.strptime(row['CustomDate1'], '%d/%m/%y')"
        self.template.custom_text_1_name = "Custom Text 1"
        self.template.get_custom_text_1 = "row['CustomText1']"

    def build(self, persist=False):
        if persist:
            self.template.save()
        else:
            self.template.id = BankAccountTemplateBuilder.next_static_id
            BankAccountTemplateBuilder.next_static_id += 1
        logging.getLogger(__name__).info("BankAccountTemplateBuilder: Created test bank account template with id "
                                         + str(self.template.id))
        return self.template

    @classmethod
    def write_transactions_to_file(cls, stream, transactions):
        stream.write('"Date","Description","CustomDate1","CustomText1","Amount","CurrentBalance","Label","Notes"')
        for transaction in transactions:
            values = [
                transaction.date.__format__("%d/%m/%y"),
                transaction.description,
                transaction.custom_date_1.__format__("%d/%m/%y") if transaction.custom_date_1 is not None else "",
                transaction.custom_text_1,
                str(transaction.amount),
                str(transaction.current_balance),
            ]
            stream.write("\n" + ",".join(values))
        stream.close()

    @classmethod
    def write_transactions_to_download_file(cls, stream, transactions):
        stream.write(
            'TransactionId,Account,AccountId,Date,Description,Amount,Label,Notes,CurrentBalance,CustomDate1,CustomText1')
        for transaction in transactions:
            values = [
                str(transaction.id),
                '"{0}"'.format(transaction.bank_account.name),
                str(transaction.bank_account.id),
                transaction.date.__format__("%d/%m/%y"),
                '"{0}"'.format(transaction.description),
                str(transaction.amount),
                '"{0}"'.format(transaction.transaction_label.name) if transaction.transaction_label is not None else '""',
                '"{0}"'.format(transaction.notes) if transaction.notes is not None else '""',
                str(transaction.current_balance),
                transaction.custom_date_1.__format__("%d/%m/%y") if transaction.custom_date_1 is not None else '',
                '"{0}"'.format(transaction.custom_text_1),
            ]
            stream.write("\n" + ",".join(values))


class IOutput:
    def open(self):
        raise NotImplementedError()

    def delete(self):
        raise NotImplementedError()


class FileOutput(IOutput):
    def __init__(self, file_path):
        self.__file_path = file_path

    def open(self):
        return open(self.__file_path, "w")

    def delete(self):
        os.remove(self.__file_path)


class StringOutput(IOutput):
    def __init__(self):
        self.__writer = StringIO()

    def open(self):
        return self.__writer

    def getvalue(self):

        return self.__writer.getvalue()

    def delete(self):
        self.__writer = None
