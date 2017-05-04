#!/usr/bin/env bash

function usage
{
    echo "usage: install_test_db [[-p <path_to_db> ] | [-h]]"
}

path=
while [ "$1" != "" ]; do
    case $1 in
        -p | --path )           shift
                                path=$1
                                ;;
        -h | --help )           usage
                                exit
                                ;;
        * )                     usage
                                exit 1
    esac
    shift
done

export FINANCE_DATABASE_NAME=${path}

./install_db.sh --path ${FINANCE_DATABASE_NAME}

python3 manage.py shell < transactions/src/InstallTestData.py

if  [[ $1 != "-q" ]]; then
    python3 manage.py createsuperuser --username admin --email admin@localhost
fi
