from django.core.urlresolvers import reverse
from django.test import Client
from django.utils.encoding import force_text

from tests import DatabaseBackedFinanceTestCase
from tests.builders import BankAccountBuilder
from tests.builders import TransactionBuilder
from tests.builders import TransactionFileBuilder


class TransactionsDownloadTests(DatabaseBackedFinanceTestCase):
    def setUp(self):
        super().setUp()

        account = BankAccountBuilder() \
            .with_test_bank_account_template() \
            .build(persist=True)
        self.transaction = TransactionBuilder() \
            .for_bank_account(account) \
            .build(persist=True)
        client = Client()
        self.expected = TransactionFileBuilder.for_download() \
            .with_transactions([self.transaction]) \
            .build()
        self.response = client.get(reverse('download'))

    def tearDown(self):
        super().tearDown()

    def test_ok(self):
        self.assertEqual(self.response.status_code, 200)
        content = force_text(self.response.content)
        a = content.splitlines()
        self.assertEqual(a[0], self.expected.getvalue().splitlines()[0])
        self.assertEqual(a[1], self.expected.getvalue().splitlines()[1])
        self.assertEqual(len(a), 2)
