from telebot.types import Message

from database.quest_bot_db import check_and_add_user, save_current_step
from keyboards.inline.keyboard import generate_game_menu
from loader import bot
from my_logging import my_log
from states.quest_state import GeneralStates


@bot.message_handler(commands=['start'])
def bot_start(message: Message) -> None:
    check_and_add_user(message.chat.id, message.from_user.first_name, message.from_user.username)
    try:
        markup = generate_game_menu()
        text = [
            f"Привет, <b>{message.from_user.full_name}</b>!\n"
            f"Добро пожаловать в Quest_bot. 🎉\n"
            f"Здесь ты можешь найти увлекательные текстовые квесты.\n"
            "Выбери игру из меню ниже:"
        ]
        bot.send_message(message.chat.id, '\n'.join(text), reply_markup=markup, parse_mode='HTML')
    except Exception as e:
        my_log.logger.exception(e)


@bot.callback_query_handler(func=lambda call: not call.data.startswith('qbgm_'))
def callback_inline(call):

    try:
        if call.message:
            game_id_name = call.data.replace('game-', '')  # Это то, что ты передала в callback_data
            game_id, game_name = game_id_name.split(". ")

            bot.set_state(call.from_user.id, GeneralStates.main, call.message.chat.id)

            with bot.retrieve_data(call.message.chat.id, call.message.chat.id) as data:
                data['game_id'] = game_id

            # Динамически импортируем нужный модуль
            game_module = __import__(f"games.{game_name}.{game_name}", fromlist=[''])

            initial_message, markup = game_module.start_game(0, call.from_user.id)

            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text=initial_message,
                                  reply_markup=markup, parse_mode='HTML')
    except Exception as e:
        my_log.logger.exception(e)
