from tests.test_framework import FinanceTestCase
from tests.builders.BankAccountBuilder import *
from tests.builders.ImportFileBuilder import *
from transactions.src import import_transactions
from transactions.models import Transaction

class TestImport(FinanceTestCase):

    def setUp(self):
        super().setUp()
        self.account_id = BankAccountBuilder().with_test_bank_account_template().build().id
        self.import_file = ImportFileBuilder().build()

    def tearDown(self):
        self.import_file.delete_file()
        super().tearDown()

    def test_import(self):
        import_transactions.import_transactions_core(
            self.import_file.open(),
            self.account_id,
            actually_import=True)

        transactions = Transaction.objects.all()
        self.assertEqual(len(transactions), 1)
        self.assertEqual(
            transactions[0].current_balance,
            self.import_file.transactions[0].current_balance)

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
