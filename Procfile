web: cd us_foodscope && gunicorn us_foodscope.wsgi --bind 0.0.0.0:$PORT
release: cd us_foodscope && python manage.py migrate && python manage.py collectstatic --noinput