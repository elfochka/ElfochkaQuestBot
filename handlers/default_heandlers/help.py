from telebot.types import Message
from config_data.config import DEFAULT_COMMANDS
from loader import bot
from my_logging import my_log


@bot.message_handler(commands=['help'])
def bot_help(message: Message) -> None:
    """
    Ловим команду help и выдаем описание
    :param message:
    :return: (None)
    """
    try:
        text = [f"Привет, <b>{message.from_user.full_name}</b>!\n"
                f"Добро пожаловать в Quest_bot. 🎉\n"
                f"В этом боте ты можешь проходить различные текстовые квесты.\n"
                "Вот что ты можешь делать:"]

        text += [f'/{command} - {description}' for command, description in DEFAULT_COMMANDS]

        bot.reply_to(message, '\n'.join(text), parse_mode='HTML')
    except Exception as e:
        my_log.logger.exception(e)
