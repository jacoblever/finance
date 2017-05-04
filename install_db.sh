#!/usr/bin/env bash

function usage
{
    echo "usage: install_db [[-p <path_to_db> ] | [-h]]"
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

if [ -z ${path} ]
then
    usage
    exit 1
fi

if [ -e ${path} ]
then
    while true; do
        echo "Database already exists!"
        read -p "This will permanently delete all data in ${path} and CANNOT be undone. (yes/no) " yn
        case $yn in
            [Yy]* ) break;;
            [Nn]* ) echo "Cancelled";exit;;
            * ) echo "Please answer yes or no.";;
        esac
    done
fi

echo "Installing database at ${path}..."
export FINANCE_DATABASE_NAME=${path}
rm -f ${path}
rm -f ./transactions/migrations/0001_initial.py
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py shell < transactions/src/ensureSetup.py
echo "Database installed"
