#!/usr/bin/env bash
cd /var/www/tbo23.ru/
sudo git pull
sudo chown www-data:www-data -R /var/www/tbo23.ru

python3 manage.py collectstatic --noinput
python3 manage.py migrate
#python manage.py thumbnail clear_delete_all
#systemctl restart uwsgi-app@lanzeva
systemctl restart uwsgi
systemctl restart nginx
sudo chown www-data:www-data -R /var/www/tbo23.ru
