#!/bin/bash
while ! pg_isready -h "127.0.0.1"; do
    sleep 1
done
yes | python3 manage.py makemigrations
python3 manage.py migrate
yes | python3 manage.py makemigrations ifpracessomain
python3 manage.py migrate ifpracessomain
cat <<EOF | python3 manage.py shell
from django.contrib.auth import get_user_model

User = get_user_model()  # get the currently active user model,

User.objects.filter(username='admin').exists() or \
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
EOF
python3 manage.py runserver 0.0.0.0:8000
