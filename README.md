# django-blog
Simple blog example using Django. Adaptive design via Bootstrap. Simple comments, pagination, tags filtering, text search, SEO friendly, sidebar.

Clone repository, inside magic-link-test-task directory create and activate your virtual envienvironment, Run:
```
pip install -r requirements.txt
```
Create .env file
```
SECRET_KEY=INSERT_YOUR_DJANGO_SECRET_KEY_HERE
```
Run
```
python manage.py migrate
python manage.py loaddata data.json
python manage.py collectstatic
python manage.py runserver
```
