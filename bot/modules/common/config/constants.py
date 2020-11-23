import os

BOT_TOKEN = os.getenv('BOT_TOKEN', '')

BOT_ADMIN = int(os.getenv('BOT_ADMIN', ''))

BOT_ADMIN_ALIAS = os.getenv('BOT_ADMIN_ALIAS', '')

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'info')

DATABASE_URL = os.environ.get('DATABASE_URL', '')

redis = {
    'host': 'redis',
    'port': 5432,

}

mongo = {
    'host': 'mongodb://root:password@mongo:27017/'
}

TIME_ZONE = 'Etc/GMT-3'

SERVER_API_URL = f'http://surveys:80/surveys/api/{BOT_TOKEN}/'
