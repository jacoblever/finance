from test_framework import *

setup_environment()

from tests.test_cases.WhenImportingTransactions import WhenImportingTransactions
from tests.test_cases.WhenImportingTheSameTransactionTwice import WhenImportingTheSameTransactionTwice

test_cases = [
    WhenImportingTransactions,
    WhenImportingTheSameTransactionTwice,
]

suite = unittest.TestSuite()
for test_case in test_cases:
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(test_case))
unittest.TextTestRunner(verbosity=2).run(suite)
