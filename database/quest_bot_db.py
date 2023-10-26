import pymysql

from config_data import config


def fetch_games_from_db():
    connection = pymysql.connect(
        host=config.DB_HOST,
        user=config.DB_USERNAME,
        password=config.DB_PASSWORD,
        db=config.DB_NAME)
    cursor = connection.cursor()
    cursor.execute("SELECT id, name_short, name FROM games")
    games = cursor.fetchall()
    cursor.close()
    connection.close()
    return games


# Check and add user using pymysql
def check_and_add_user(telegram_id, name, username, language='ru'):
    connection = pymysql.connect(
        host=config.DB_HOST,
        user=config.DB_USERNAME,
        password=config.DB_PASSWORD,
        db=config.DB_NAME)
    cursor = connection.cursor()

    cursor.execute("SELECT id FROM users WHERE telegram_id = %s", (telegram_id,))
    result = cursor.fetchone()

    if result:
        cursor.execute("UPDATE users SET name = %s, username = %s, language = %s WHERE id = %s",
                       (name, username, language, result[0]))
        user_id = result[0]
    else:
        cursor.execute("INSERT INTO users (telegram_id, name, username, language) VALUES (%s, %s, %s, %s)",
                       (telegram_id, name, username, language))
        user_id = cursor.lastrowid

    connection.commit()
    cursor.close()
    connection.close()

    return user_id


# Save the current step of a game for a user using pymysql
def save_current_step(chat_id, game_id, last_step):
    connection = pymysql.connect(
        host=config.DB_HOST,
        user=config.DB_USERNAME,
        password=config.DB_PASSWORD,
        db=config.DB_NAME)
    cursor = connection.cursor()

    # Check if a record already exists for the user and game
    cursor.execute("SELECT id FROM saves WHERE chat_id = %s AND game_id = %s", (chat_id, game_id))
    result = cursor.fetchone()

    if result:
        # Update the last_step if a record already exists
        cursor.execute("UPDATE saves SET last_step = %s WHERE id = %s", (last_step, result[0]))
    else:
        # Insert a new record if it doesn't exist
        cursor.execute("INSERT INTO saves (chat_id, game_id, last_step) VALUES (%s, %s, %s)",
                       (chat_id, game_id, last_step))

    connection.commit()
    cursor.close()
    connection.close()


# Load the current step of a game for a user using pymysql
def load_current_step(chat_id, game_id):
    connection = pymysql.connect(
        host=config.DB_HOST,
        user=config.DB_USERNAME,
        password=config.DB_PASSWORD,
        db=config.DB_NAME)
    cursor = connection.cursor()

    cursor.execute("SELECT last_step FROM saves WHERE chat_id = %s AND game_id = %s", (chat_id, game_id))
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    if result:
        return result[0]
    else:
        return None
