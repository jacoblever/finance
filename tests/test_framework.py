import logging
import unittest

from django.test.utils import setup_test_environment, teardown_test_environment
from django.db import connection


class FinanceTestCase(unittest.TestCase):
    def __init__(self, methodName):
        super().__init__(methodName)
        self.verbosity = 1

    def setUp(self):
        logging.getLogger(__name__).info('%s: set up', type(self).__name__)
        setup_test_environment()

    def tearDown(self):
        teardown_test_environment()
        logging.getLogger(__name__).info('%s: teared down', type(self).__name__)


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
