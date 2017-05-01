import sys
import os
import unittest
from os.path import abspath, dirname
from django.core.wsgi import get_wsgi_application

project_dir = abspath(dirname(dirname(__file__)))
sys.path.insert(0, project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'finance.settings'
get_wsgi_application()

from tests.test_cases.WhenImportingTransactions import WhenImportingTransactions
from tests.test_cases.WhenImportingTheSameTransactionTwice import WhenImportingTheSameTransactionTwice
from tests.test_cases.InternalTransferFinderTests import InternalTransferFinderTests

test_cases = [
    WhenImportingTransactions,
    WhenImportingTheSameTransactionTwice
]

test_groups = [
    InternalTransferFinderTests
]

def get_tests(cls):
    results = []
    for attrname in dir(cls):
        obj = getattr(cls, attrname)
        if isinstance(obj, type):
            results.append(obj)
    return results

for group in test_groups:
    test_cases.extend(get_tests(group))

suite = unittest.TestSuite()
for test_case in test_cases:
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(test_case))
unittest.TextTestRunner(verbosity=2).run(suite)
