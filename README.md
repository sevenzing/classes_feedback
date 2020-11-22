FSE project
===

## To start django server

1. migrate 

    
    ```bash 
    python3 manage.py createsuperuser
    python3 manage.py migrate
    ```
1. run server using `manage.py`

    ```bash
    python3 manage.py runserver
    ```

## To start bot:

1. Create `.env` file
    
    ```bash
    mv .env.example .env
    ```

1. Enter bot token in `.env` file 
1. Start using `docker`:
```bash
docker-compose up --build
```

Commments:

> djano didn't attach with docker-compose yet 

> bot uses default mysql database, in order to stat the bot you have to create database in `localhost:8080`
