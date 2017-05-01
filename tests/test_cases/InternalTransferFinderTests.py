from datetime import datetime

from tests import FinanceTestCase
from tests.builders import TransactionBuilder
from transactions.src.InternalTransferFinder import InternalTransferFinder


class InternalTransferFinderTests:
    class WhenThereAreTwoTransactionsForOppositeAmountsOnTheSameDay(FinanceTestCase):
        def setUp(self):
            super().setUp()
            date = datetime.strptime("30/04/17", '%d/%m/%y')
            transactions = [
                TransactionBuilder()
                    .with_date(date)
                    .with_amount(10)
                    .build(persist=False),
                TransactionBuilder()
                    .with_date(date)
                    .with_amount(-10.00)
                    .build(persist=False),
                TransactionBuilder()
                    .with_date(date)
                    .with_amount(11.01)
                    .build(persist=False)
            ]
            self.matches = InternalTransferFinder(transactions).find()

        def test_that_one_group_is_found(self):
            self.assertEqual(1, len(self.matches))

        def test_that_the_group_has_two_items(self):
            self.assertEqual(2, len(self.matches[0]))

        def test_that_one_transaction_has_amount_10(self):
            self.assertEqual(10, self.matches[0][0].amount)

        def test_that_one_transaction_has_amount_minus_10(self):
            self.assertEqual(-10, self.matches[0][1].amount)

    class WhenThereAreTwoTransactionsForOppositeAmountsOnDifferentDays(FinanceTestCase):
        def setUp(self):
            super().setUp()
            transactions = [
                TransactionBuilder()
                    .with_date(datetime.strptime("30/04/17", '%d/%m/%y'))
                    .with_amount(10.01)
                    .build(persist=False),
                TransactionBuilder()
                    .with_date(datetime.strptime("29/04/17", '%d/%m/%y'))
                    .with_amount(-10.01)
                    .build(persist=False)
            ]
            self.matches = InternalTransferFinder(transactions).find()

        def test_that_no_groups_are_found(self):
            self.assertEqual(0, len(self.matches))

    class WhenThereAreTwoTransactionsForDifferentAmountsOnTheSameDay(FinanceTestCase):
        def setUp(self):
            super().setUp()
            transactions = [
                TransactionBuilder()
                    .with_date(datetime.strptime("30/04/17", '%d/%m/%y'))
                    .with_amount(10.01)
                    .build(persist=False),
                TransactionBuilder()
                    .with_date(datetime.strptime("30/04/17", '%d/%m/%y'))
                    .with_amount(-10.02)
                    .build(persist=False)
            ]
            self.matches = InternalTransferFinder(transactions).find()

        def test_that_no_groups_are_found(self):
            self.assertEqual(0, len(self.matches))

    class WhenThereAreTwoTransactionsForTheSameAmountOnTheSameDay(FinanceTestCase):
        def setUp(self):
            super().setUp()
            transactions = [
                TransactionBuilder()
                    .with_date(datetime.strptime("30/04/17", '%d/%m/%y'))
                    .with_amount(10.01)
                    .build(persist=False),
                TransactionBuilder()
                    .with_date(datetime.strptime("30/04/17", '%d/%m/%y'))
                    .with_amount(10.01)
                    .build(persist=False)
            ]
            self.matches = InternalTransferFinder(transactions).find()

        def test_that_no_groups_are_found(self):
            self.assertEqual(0, len(self.matches))
