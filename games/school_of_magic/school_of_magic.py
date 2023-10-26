import pandas as pd

from database.quest_bot_db import load_current_step, save_current_step
from keyboards.inline.keyboard import generate_game_markup, generate_game_menu
from loader import bot
from my_logging import my_log


def read_story():
    try:
        df = pd.read_excel("./games/school_of_magic/school_of_magic_story.xlsx")
        story_dict = df.to_dict(orient="index")
        return story_dict
    except Exception as e:
        my_log.logger.exception(e)


def start_game(step, tg_user_id, user_choice=None):
    with bot.retrieve_data(tg_user_id, tg_user_id) as data:
        game_id = data['game_id']
    try:
        saved_step = load_current_step(tg_user_id, game_id)
        if saved_step is not None:
            step = saved_step

        story = read_story()

        if step not in story:
            text = 'Конец игры. Спасибо за участие! 🌟\nПоиграем еще?'
            markup = generate_game_markup(None, "qbgm_schoolofmagic_")
            return text, markup

        current_step = story[step]
        text = f"<i>Шаг</i> <u>{str(current_step['current_step'])}</u>\n" \
               f"<b>{current_step.get('Text', 'Нет текста для этого шага')}</b>"

        actions = current_step.get('Actions', 'Конец игры')

        if actions == "Конец игры":
            text += '\nИгра закончена! 🌟\nПоиграем еще?'
            markup = generate_game_markup(None, "qbgm_schoolofmagic_")
            return text, markup

        markup = generate_game_markup(actions, "qbgm_schoolofmagic_")  # передаем префикс

        return text, markup
    except Exception as e:
        my_log.logger.exception(e)


@bot.callback_query_handler(func=lambda call: call.data.startswith('qbgm_schoolofmagic_'))
def callback_inline(call):
    try:
        if call.message:
            with bot.retrieve_data(call.message.chat.id, call.message.chat.id) as data:
                game_id = data['game_id']
            step = call.data.replace('qbgm_schoolofmagic_', '')  # Убираем префикс
            if step == 'refresh':
                step = 0
            else:
                step = int(step)
            save_current_step(call.from_user.id, game_id, step)
            text, markup = start_game(step, call.from_user.id)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text,
                                  reply_markup=markup, parse_mode='HTML')
    except Exception as e:
        my_log.logger.exception(e)
