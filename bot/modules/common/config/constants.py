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

TIME_ZONE = 'Etc/GMT-3'
