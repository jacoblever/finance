from tests import DatabaseBackedFinanceTestCase
from tests.builders import BankAccountBuilder
from tests.builders import TransactionFileBuilder
from transactions.src import import_transactions


class WhenImportingTheSameTransactionTwice(DatabaseBackedFinanceTestCase):
    def setUp(self):
        super().setUp()
        self.account_id = BankAccountBuilder().with_test_bank_account_template().build(persist=True).id
        self.import_file = TransactionFileBuilder().for_import()\
            .with_random_transactions(count=1)\
            .build()

        import_transactions.import_transactions_core(
            self.import_file.open(),
            self.account_id,
            actually_import=True)

        self.import_result = import_transactions.import_transactions_core(
            self.import_file.open(),
            self.account_id,
            actually_import=False)

    def tearDown(self):
        self.import_file.delete()
        super().tearDown()

    def test_that_one_transaction_is_found(self):
        self.assertEqual(1, self.import_result[0])

    def test_that_a_duplicate_is_detected(self):
        self.assertEqual(1, len(self.import_result[1]))

    def test_that_zero_existing_transactions_are_found(self):
        self.assertEqual(0, self.import_result[2])

    def test_that_zero_problems_are_found(self):
        self.assertEqual(0, len(self.import_result[3]))
