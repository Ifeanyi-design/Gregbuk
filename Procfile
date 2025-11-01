web: bash -c "celery -A tasks.celery worker --loglevel=info & gunicorn main:app --bind 0.0.0.0:$PORT"
