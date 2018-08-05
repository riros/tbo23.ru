#!/usr/bin/env bash
cd /var/www/tbo23.ru/
sudo git pull
sudo chown nginx:nginx -R /var/www/tbo23.ru/

python3 manage.py collectstatic --noinput
python3 manage.py migrate
#python manage.py thumbnail clear_delete_all
#systemctl restart uwsgi-app@tbo23
systemctl restart uwsgi-app@tbo23.ru
systemctl restart nginx