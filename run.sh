#!/bin/bash
while ! pg_isready -h "db"; do
    sleep 1
done
yes | python manage.py makemigrations
python manage.py migrate
yes | python manage.py makemigrations IFPRAcessoMain
python manage.py migrate IFPRAcessoMain
cat <<EOF | python manage.py shell
from django.contrib.auth import get_user_model

User = get_user_model()  # get the currently active user model,

User.objects.filter(username='admin').exists() or \
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
EOF
python manage.py runserver 0.0.0.0:8000