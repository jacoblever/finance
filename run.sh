if  [[ $1 != "-q" ]]; then
    python3 manage.py shell < transactions/src/ensureSetup.py
fi
python3 manage.py runserver

