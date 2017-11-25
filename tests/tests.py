import logging
import sys
import inspect
import os
import unittest
from os.path import abspath, dirname
from django.core.wsgi import get_wsgi_application

project_dir = abspath(dirname(dirname(__file__)))
sys.path.insert(0, project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'finance.settings'
get_wsgi_application()

import tests.test_cases

suite = unittest.TestSuite()
logging.basicConfig(
    filename='logs/tests.log',
    format='%(asctime)s: %(levelname)s - %(message)s',
    level=logging.DEBUG,
    datefmt='%m/%d/%Y %I:%M:%S %p')

def get_test_cases():
    for name, cls in inspect.getmembers(tests.test_cases):
        if inspect.isclass(cls):
            yield cls
            for attrname in dir(cls):
                obj = getattr(cls, attrname)
                if isinstance(obj, type):
                    yield obj


for test_case in get_test_cases():
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(test_case))
unittest.TextTestRunner(verbosity=2).run(suite)
