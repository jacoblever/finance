rm ./db.sqlite3
rm ./transactions/migrations/0001_initial.py
python3 manage.py makemigrations
python3 manage.py migrate

python3 manage.py shell < transactions/src/ensureSetup.py
python3 manage.py shell < install.py

if  [[ $1 != "-q" ]]; then
    python3 manage.py createsuperuser --username admin --email jacobianism@gmail.com
fi

python3 manage.py runserver

