import os
from dotenv import set_key

bot_token = os.environ.get('BOT_TOKEN')

db_host = os.environ.get('DB_HOST')
db_name = os.environ.get('DB_NAME')
db_user = os.environ.get('DB_USERNAME')
db_password = os.environ.get('DB_PASSWORD')

set_key('.env', 'BOT_TOKEN', bot_token)

set_key('.env', 'DB_HOST', db_host)
set_key('.env', 'DB_NAME', db_name)
set_key('.env', 'DB_USERNAME', db_user)
set_key('.env', 'DB_PASSWORD', db_password)
