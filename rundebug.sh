systemctl stop jiesysadmin.service
IP=$(hostname -I | awk -F " " '{printf $1}')
cd /cosyjieserver/jiesysadmin
python manage.py runserver $IP:8000