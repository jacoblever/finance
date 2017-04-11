from tests.test_framework import FinanceTestCase
from tests.builders.BankAccountBuilder import *
from tests.builders.ImportFileBuilder import *
from transactions.src import import_transactions
from transactions.models import Transaction

class WhenImportingTransactions(FinanceTestCase):

    def setUp(self):
        super().setUp()
        self.account_id = BankAccountBuilder().with_test_bank_account_template().build().id
        self.import_file = ImportFileBuilder().build()

        self.import_result = import_transactions.import_transactions_core(
            self.import_file.open(),
            self.account_id,
            actually_import=True)

    def tearDown(self):
        self.import_file.delete_file()
        super().tearDown()

    def test_that_one_transaction_is_found(self):
        self.assertEqual(1, self.import_result[0])

    def test_that_zero_duplicates_are_found(self):
        self.assertEqual(0, len(self.import_result[1]))

    def test_that_zero_existing_transactions_are_edited(self):
        self.assertEqual(0, self.import_result[2])

    def test_that_zero_problems_are_found(self):
        self.assertEqual(0, len(self.import_result[3]))

    def test_one_transaction_is_imported(self):
        self.assertEqual(1, len(Transaction.objects.all()))

    def test_the_transaction_has_the_correct_date(self):
        self.assertPropertyEqual(lambda x: x.date)

    def test_the_transaction_has_the_correct_description(self):
        self.assertPropertyEqual(lambda x: x.description)

    def test_the_transaction_has_the_correct_amount(self):
        self.assertPropertyEqual(lambda x: x.amount)

    def test_the_transaction_has_the_correct_current_balance(self):
        self.assertPropertyEqual(lambda x: x.current_balance)

    def test_the_transaction_has_the_correct_custom_date_1(self):
        self.assertPropertyEqual(lambda x: x.custom_date_1)

    def test_the_transaction_has_the_correct_custom_text_1(self):
        self.assertPropertyEqual(lambda x: x.custom_text_1)

    def test_the_transaction_has_the_correct_bank_account(self):
        self.assertEqual(
            self.account_id,
            Transaction.objects.all()[0].bank_account.id)

    def assertPropertyEqual(self, property):
        self.assertEqual(
            property(self.import_file.transactions[0]),
            property(Transaction.objects.all()[0]))

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
