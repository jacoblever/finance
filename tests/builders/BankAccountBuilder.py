import logging
from .BankAccountTemplateBuilder import BankAccountTemplateBuilder
from transactions.models import BankAccount, BankAccountTemplate


class BankAccountBuilder:
    next_static_id = 1

    def __init__(self):
        self.account = BankAccount()
        self.account.name = "Test bank account"
        self.account.account_type = "CreditCard"
        self.account.more_details = 'Some other info'
        self.account.is_active = True
        self.useTemplateBuilder = False

    def with_bank_account_template_id(self, id_):
        self.account.bank_account_template = BankAccountTemplate.objects.get(pk=id_)
        return self

    def with_test_bank_account_template(self):
        self.useTemplateBuilder = True
        return self

    def build(self, persist=False):
        if self.useTemplateBuilder:
            builder = BankAccountTemplateBuilder()
            self.account.bank_account_template = builder.build(persist)
        assert self.account.bank_account_template != None
        if persist:
            self.account.save()
        else:
            self.account.id = BankAccountBuilder.next_static_id
            BankAccountBuilder.next_static_id += 1
        logging.getLogger(__name__).info("BankAccountBuilder: Created test bank account with id "+ str(self.account.id))
        return self.account
