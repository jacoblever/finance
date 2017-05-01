import unittest

from django.test.utils import setup_test_environment, teardown_test_environment
from django.db import connection


class FinanceTestCase(unittest.TestCase):
    def __init__(self, methodName):
        super().__init__(methodName)
        self.verbosity = 1

    def setUp(self):
        setup_test_environment()
        # So calls to print appear on a new line
        print("")

    def tearDown(self):
        teardown_test_environment()


class DatabaseBackedFinanceTestCase(FinanceTestCase):
    def __init__(self, methodName):
        super().__init__(methodName)
        self.verbosity = 1

    def setUp(self):
        super().setUp()
        connection.creation.create_test_db(self.verbosity)
        # todo the import here actually runs the ensureSetup script!
        from transactions.src import ensureSetup

    def tearDown(self):
        connection.creation.destroy_test_db('', self.verbosity)
        super().tearDown()
