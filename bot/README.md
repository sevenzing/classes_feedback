My personal template for telegram bot
====


## Modules
+ Default module
    + /start, /help, /cancel

+ Admin module
    + /restart


## Requirements
+ [docker](https://www.docker.com/get-started)
+ [docker-compose](https://docs.docker.com/compose/install/)

## How to start
1. Setup `.evn` file 
    + Create `.env` file in root directory: `mv .env.example .env`
    + Fill the file using your telegram token, admin alias, etc

2. Start the bot using docker:
```bash
$ ./docker-compose up --build
```
