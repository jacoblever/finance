import argparse

#!/usr/bin/env bash
DEFAULT_DATABASE_PATH = "./data/default_db.sqlite3"
TEST_DATABASE_PATH = "./data/test_db.sqlite3"

database_path = DEFAULT_DATABASE_PATH

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--database", help="database to use")
parser.add_argument("-t", "--test", help="test mode",
                    action="store_true")
parser.add_argument("-q", "--quick", help="quick mode",
                    action="store_true")
args = parser.parse_args()

if args.database:
	database_path = args.database
if args.test:
	database_path = TEST_DATABASE_PATH
quick = 1 if args.quick else 0

import os.path
if os.path.isfile(database_path):
	print("Using database {0}".format(database_path))
else:
	print("Database {0} does not exist.".format(database_path))
	answer = input("Would you like to install a database at this location? (yes/no)")
	if answer == "yes":
		if database_path == DEFAULT_DATABASE_PATH:
			# Ensure data directory exists
			if not os.path.exists("data"):
				os.makedirs("data")
			#./install_db.sh --path ${DEFAULT_DATABASE_PATH}
			print("TODO: Call install DB")
		elif database_path == TEST_DATABASE_PATH:
			# Ensure data directory exists
			if not os.path.exists("data"):
				os.makedirs("data")
			#./install_test_db.sh --path ${TEST_DATABASE_PATH}
		else:
			#./install_db.sh --path ${database_path}
			pass
	elif answer == "no":
		print("Cancelled")
		exit()
	else:
		exit()

FINANCE_DATABASE_NAME = database_path

if quick != 1:
	pass
	#manage.py shell < transactions/src/ensureSetup.py

execfile('manage.py runserver')