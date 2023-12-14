import io
import logging

from aiogram import Router
from aiogram import types
from aiogram.types import BufferedInputFile
from aiogram.filters import Command

from config import load_config
from history import SimpleMessageHistory
from gpt_connect import question_processing
from history import UserState
from speechkit_connect import conv_voice_to_text
from speechkit_connect import conv_text_to_voice

LINK_ABOUT = 'https://urfu-iml-2023-14-project-workshop.streamlit.app/%D0%9A%D0%BE%D0%BC%D0%B0%D0%BD%D0%B4%D0%B0'
LINK_HELP = 'https://urfu-iml-2023-14-project-workshop.streamlit.app/%D0%9F%D0%BE%D0%BC%D0%BE%D1%89%D1%8C'

bot_router = Router()
logger = logging.getLogger(__name__)
config = load_config()
user_state = UserState()


@bot_router.message(Command("start"))
async def handle_cmd_start(msg: types.Message):
    logger.log(level=logging.INFO,
               msg=f' --> Мы знакомимся с {msg.from_user.full_name} '
                   f'({msg.from_user.id})')

    user_state.init_user(msg.from_user.id, msg.from_user.full_name)

    await msg.answer(f'{msg.from_user.first_name}, Добро пожаловать!\n'
                     f'Я умный городской гид по городу Екатеринбургу '
                     f'и с радостью помогу ответить на ваши '
                     f'вопросы о достопримечательностях, '
                     f'местах отдыха и питания в Екатеринбурге.\n\n'
                     f'Уточните, пожалуйста, что вас интересует?')


@bot_router.message(Command("help"))
async def handle_cmd_help(msg: types.Message):
    logger.log(level=logging.INFO,
               msg=f' --> Справку запрашивает {msg.from_user.full_name} '
                   f'({msg.from_user.id})')

    user_state.init_user(msg.from_user.id, msg.from_user.full_name)

    await msg.answer(f'Более подробная информация доступна на '
                     f'<a href="{LINK_HELP}">сайте</a> проекта')


@bot_router.message(Command("about"))
async def handle_cmd_about(msg: types.Message):
    logger.log(level=logging.INFO,
               msg=f' --> О нас запрашивает {msg.from_user.full_name} '
                   f'({msg.from_user.id})')

    user_state.init_user(msg.from_user.id, msg.from_user.full_name)

    await msg.answer(f'Более подробная информация доступна на '
                     f'<a href="{LINK_ABOUT}">сайте</a> проекта')


@bot_router.message(Command("voice_out"))
async def handle_cmd_about(msg: types.Message):
    logger.log(level=logging.INFO,
               msg=f' --> {msg.from_user.full_name} '
                   f'({msg.from_user.id}) переключает голос')

    user_state.init_user(msg.from_user.id, msg.from_user.full_name)
    result = user_state.toogle_user_voice_out(msg.from_user.id)

    if result:
        await msg.answer(f'Режим озвучивания включен')
    else:
        await msg.answer(f'Режим озвучивания выключен')


@bot_router.message(Command("clear"))
async def handle_cmd_about(msg: types.Message):
    logger.log(level=logging.INFO,
               msg=f' --> {msg.from_user.full_name} '
                   f'({msg.from_user.id}) сбрасывает контекст')

    user_state.init_user(msg.from_user.id, msg.from_user.full_name)
    user_state.clear_history(msg.from_user.id)

    await msg.answer(f'Контекст сброшен! Приятного общения 😀')


@bot_router.message()
async def handle_voice_message(msg: types.Message):
    logger.log(level=logging.INFO,
               msg=f' --> Мы получили вопрос от '
                   f'{msg.from_user.full_name} '
                   f'({msg.from_user.id})')
    logger.log(level=logging.INFO,
               msg=f' ----> Content Type - {msg.content_type}')

    user_state.init_user(msg.from_user.id, msg.from_user.full_name)

    if msg.content_type != types.ContentType.TEXT \
            and msg.content_type != types.ContentType.VOICE:
        await msg.answer(f'Я не умею обрабатывать сообщения типа {msg.content_type}')
        return

    if msg.text and msg.text[0] == '/':
        logger.log(level=logging.INFO,
                   msg=f' --> Пользователь {msg.from_user.full_name} '
                       f'({msg.from_user.id}) прислал неизвестную команду '
                       f'{msg.text}')
        await msg.answer(f'Я не умею обрабатывать команду {msg.text}')
        return

    question: str = msg.text
    answer: str = ''

    if msg.content_type == types.ContentType.VOICE:
        try:
            # Получение файла голоса
            file_path = (await msg.bot.get_file(msg.voice.file_id)).file_path
            voice_ogg = io.BytesIO()
            await msg.bot.download_file(file_path, voice_ogg)

            question = await conv_voice_to_text(voice_ogg.getbuffer().tobytes(), msg.voice.duration)
        except Exception as e:
            await msg.answer(f'Ошибка программы распознования голоса: {e}')
            return

    logger.log(level=logging.INFO,
               msg=f' ----> {question}')

    try:
        answer = await question_processing(msg.from_user.id,
                                           question,
                                           user_state.get_history(msg.from_user.id))
    except Exception as e:
        await msg.answer(f'Ошибка получения ответа от помощника: {e}')
        return

    user_state.add_history(msg.from_user.id, SimpleMessageHistory(
        role='user',
        message='question'))
    user_state.add_history(msg.from_user.id, SimpleMessageHistory(
        role='assistant',
        message='answer'))

    try:
        if user_state.get_user_voice_out(msg.from_user.id):
            await msg.bot.send_voice(
                chat_id=msg.chat.id,
                voice=BufferedInputFile(
                    await conv_text_to_voice(answer),
                    filename='Ответ.ogg'))
            return
    except Exception as e:
        await msg.answer(f'Ошибка получения аудио ответа: {e}')
        await msg.answer(answer)
        return

    await msg.answer(answer)
