release: python manage.py migrate
release: python manage.py loaddata data.json
web: gunicorn blog.wsgi --log-file -