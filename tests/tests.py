import unittest
import os
from os.path import abspath, dirname
import uuid
import sys

project_dir = abspath(dirname(dirname(__file__)))
sys.path.insert(0, project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'finance.settings'

from django.conf import settings
from django.db import connection
from django.test import TestCase
from django.test.utils import setup_test_environment, teardown_test_environment
from django.core.wsgi import get_wsgi_application



os.environ['DJANGO_SETTINGS_MODULE'] = 'finance.settings'
application = get_wsgi_application()

from transactions.src import import_transactions
from transactions.models import BankAccount, Transaction, TransactionLabel, BankAccountTemplate


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "finance.settings")


class TestHelper:
    def __init__(self):
        self.verbosity = 1

    def set_up(self):
        # settings.DEBUG = False
        setup_test_environment()
        connection.creation.create_test_db(self.verbosity)
        # todo the import here actually runs the ensureSetup script!
        from transactions.src import ensureSetup

    def tear_down(self):
        connection.creation.destroy_test_db('', self.verbosity)
        teardown_test_environment()


class TestImports(unittest.TestCase):

    def setUp(self):
        self.helper = TestHelper()
        self.helper.set_up()

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

        self.helper.tear_down()

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


#unittest.main()
suite = unittest.TestLoader().loadTestsFromTestCase(TestImports)
unittest.TextTestRunner(verbosity=2).run(suite)