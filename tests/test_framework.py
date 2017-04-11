import sys
import os
import unittest
from os.path import abspath, dirname
from django.test.utils import setup_test_environment, teardown_test_environment
from django.db import connection
from django.core.wsgi import get_wsgi_application


def setup_environment():
    project_dir = abspath(dirname(dirname(__file__)))
    sys.path.insert(0, project_dir)

    os.environ['DJANGO_SETTINGS_MODULE'] = 'finance.settings'
    get_wsgi_application()


class FinanceTestCase(unittest.TestCase):
    def __init__(self, methodName):
        super().__init__(methodName)
        self.verbosity = 1

    def setUp(self):
        # settings.DEBUG = False
        setup_test_environment()
        connection.creation.create_test_db(self.verbosity)
        # todo the import here actually runs the ensureSetup script!
        from transactions.src import ensureSetup

    def tearDown(self):
        connection.creation.destroy_test_db('', self.verbosity)
        teardown_test_environment()
