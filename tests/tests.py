from test_framework import *
setup_environment()

from tests.test_cases.TestImport import TestImport

test_cases = [
    TestImport,
]

suite = unittest.TestSuite()
for test_case in test_cases:
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(test_case))
unittest.TextTestRunner(verbosity=2).run(suite)
