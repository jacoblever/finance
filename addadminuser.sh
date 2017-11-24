#!/usr/bin/env bash
DEFAULT_DATABASE_PATH=./data/default_db.sqlite3
TEST_DATABASE_PATH=./data/test_db.sqlite3

database_path=${DEFAULT_DATABASE_PATH}
quick=0
while [ "$1" != "" ]; do
    case $1 in
        -d | -db | --database ) shift
                                database_path=$1
                                ;;
        -t | --test )           database_path=${TEST_DATABASE_PATH}
                                ;;
        * )                     settings=$1
                                ;;
    esac
    shift
done

if [ -e ${database_path} ]
then
    echo "Using database ${database_path}"
else
    echo "Database does not exist";exit;
fi

export FINANCE_DATABASE_NAME=${database_path}
python3 manage.py createsuperuser --username admin --email jacobianism@gmail.com

