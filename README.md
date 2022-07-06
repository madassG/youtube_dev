# Project for monitoring YT channels

Deployment Build (now temporary unavailable :/):
```bash
    docker-compose up --build
```
---

Local test build:
1) Set up your .env.prod and .env.prod.db files
2) Run the following commands:
```bash
    virtualenv env
    source env/bin/activate
    python app/manage.py migrate
```

Create your superuser
```bash
    python app/manage.py createsuperuser
```
<sub>Follow the instructions then</sub>

Start local server
```bash
    python app/manage.py runserver
```

Also, you need to start celery beat and worker

```bash
    cd app
    celery -A config.celery.app beat -l INFO
    celery -A config.celery.app worker -l INFO
```
<sub>(**Important**) Before doing this check if redis is ready</sub>