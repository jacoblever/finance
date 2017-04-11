import uuid
import os
from tests.test_framework import FinanceTestCase
from transactions.src import import_transactions
from transactions.models import BankAccount, Transaction, BankAccountTemplate

class TestImport(FinanceTestCase):

    def setUp(self):
        super().setUp()

        halifax_credit = BankAccount()
        halifax_credit.name = 'Halifax Credit'
        halifax_credit.account_type = 'CreditCard'
        halifax_credit.more_details = ''
        halifax_credit.is_active = True
        halifax_credit.bank_account_template = BankAccountTemplate.objects.get(pk=-2)
        halifax_credit.save()

        self.file_name = "tests/files/" + str(uuid.uuid4()) + ".txt"
        file_ = open(self.file_name, "w")
        file_.write('"Date","Date entered","Reference","Description","Amount","Label","Notes"')
        file_.write('\n24/01/16,24/01/16,99423920,"INTEREST ",0.15,"Loan Interest",')
        file_.close()

    def tearDown(self):
        os.remove(self.file_name)
        super().tearDown()

    def test_import(self):
        file = open(self.file_name, "r")
        import_transactions.import_transactions_core(file, 1, True)

        # self.assertEqual(file.read(), 'hello')
        Transaction.objects.all()
        self.assertEqual(len(Transaction.objects.all()), 1)

    # def test_isupper(self):
    #     self.assertTrue('FOO'.isupper())
    #     self.assertFalse('Foo'.isupper())
    #
    # def test_split(self):
    #     s = 'hello world'
    #     self.assertEqual(s.split(), ['hello', 'world'])
    #     # check that s.split fails when the separator is not a string
    #     with self.assertRaises(TypeError):
    #         s.split(2)
