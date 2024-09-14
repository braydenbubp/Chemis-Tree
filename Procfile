web: conda run -n myenv python manage.py runserver 0.0.0.0:$PORT
web: gunicorn chemapp.wsgi
web: gunicorn tutorial.wsgi
release: python manage.py makemigrations; python manage.py migrate;
