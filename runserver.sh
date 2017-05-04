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
        -q | --quick )          quick=1
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

    while true; do
        echo "Database ${database_path} does not exist."
        read -p "Would you like to install a database at this location? (yes/no) " yn
        case $yn in
            [Yy]* ) break;;
            [Nn]* ) echo "Cancelled";exit;;
            * ) echo "Please answer yes or no.";;
        esac
    done

    if [ "${database_path}" = "${DEFAULT_DATABASE_PATH}" ];
    then
        # Ensure data directory exists
        mkdir -p data
        ./install_db.sh --path ${DEFAULT_DATABASE_PATH}
    elif [ "${database_path}" = "${TEST_DATABASE_PATH}" ]
    then
        # Ensure data directory exists
        mkdir -p data
        ./install_test_db.sh --path ${TEST_DATABASE_PATH}
    else
        ./install_db.sh --path ${database_path}
    fi
fi

export FINANCE_DATABASE_NAME=${database_path}
if  [[ $quick != 1 ]]; then
    python3 manage.py shell < transactions/src/ensureSetup.py
fi

python3 manage.py runserver
