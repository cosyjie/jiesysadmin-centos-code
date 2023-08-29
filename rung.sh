systemctl stop jiesysadmin.service

IP=$(hostname -I | awk -F " " '{printf $1}')

/root/.pyenv/versions/3.10.12/envs/jiesysadmin310/bin/gunicorn -b $IP:8000 --chdir  '/cosyjieserver/jiesysadmin' --reload -n 'jiesysadmin' -t 1800 conf.wsgi