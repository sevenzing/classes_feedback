FSE project
===

## To start django server

1. migrate 

```console
$ python manage.py createsuperuser
$ python manage.py migrate
```

1. run server using `manage.py`

```console
$ python manage.py runserver
```

## To start bot:

1. Create `.env` file
    
```console
$ mv .env.example .env
```

1. Enter bot token in `.env` file 
1. Start using `docker`:
```console
$ docker-compose up --build
```
