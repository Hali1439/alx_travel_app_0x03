# Web service: runs Django with Gunicorn
web: gunicorn alx_travel_app.wsgi --log-file -

# Worker: runs Celery for background tasks
worker: celery -A alx_travel_app worker --loglevel=info
