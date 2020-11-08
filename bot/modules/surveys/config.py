import os
PLAIN_TEXT_MAX_LENGTH = 1024

EMAIL_PASSWORD= str(os.getenv('EMAIL_PASSWORD'))

EMAIL_LOGIN = str(os.getenv('EMAIL_LOGIN'))

EMAIL_MESSAGE = '''Hello! Your requested registration via telegram to Innopolis Feedback app!<br>Your code for access to bot is: %s<br>Please, enter it to the bot. Best wishes!'''
