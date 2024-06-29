# ticket_police_tracker_API

Police ticket tracker API project

## creating a Django project

runt the followed command:

> docker-compose run --rm app sh -c "django-admin startproject app ."

## Applying Django migrations with command

runt the followed command:

> docker-compose run --rm app sh -c "python manage.py wait_for_db && python manage.py migrate"

## run the server in dev mode

To run the server run the followed command:

> docker-compose up -d

## running the flake8

To run flake8 into docker container run the followed command:

> docker-compose run --rm app sh -c "flake8"

## running the test into container

To run the test into a container run the followed command:

> docker-compose run --rm app sh -c "python manage.py test"
