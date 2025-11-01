web: gunicorn main:app
worker1: celery -A tasks.celery worker --loglevel=info -Q queue1
worker2: celery -A tasks.celery worker --loglevel=info -Q queue2
