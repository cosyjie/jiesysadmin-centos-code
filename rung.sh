IP=$(hostname -I | awk -F " " '{printf $1}')

cd /cosyjieserver/jiesysadmin
#python manage.py runserver $IP:8000

gunicorn conf.wsgi -b $IP:8000 -n "jiesysadmin"