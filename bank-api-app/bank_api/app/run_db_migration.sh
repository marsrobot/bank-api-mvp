#!/bin/bash

python3 manage.py drop_db
python3 manage.py create_db
python3 manage.py db init
python3 manage.py db migrate
python3 manage.py add_users
