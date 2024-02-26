import io
import logging
from speechkit import Session, ShortAudioRecognition, SpeechSynthesis

from config import load_config

logger = logging.getLogger(__name__)
config = load_config()


async def conv_voice_to_text(voice: bytes, duration: int) -> str:
    """
    Обработка конвертации голоса в текст через Yandex SpeechKit
    """

    if duration > 30:
        raise Exception('Я не могу отвечать на слишком длинные вопросы')

    if not voice:
        raise Exception('Запись голоса не может быть пустой')

    # Создание сессии
    session = Session.from_api_key(
        api_key=config.speechkit_config.api_key,
        folder_id=config.speechkit_config.cloud_folder
    )

    # Получение текста по голосу
    recogn = ShortAudioRecognition(session)
    text = recogn.recognize(
        io.BytesIO(voice),
        format='oggopus',
        sample_rate_hertz='48000',
        lang='auto')

    logger.log(logging.INFO, msg=f' --> Распознан текст: {text}')

    if not text:
        raise Exception("Голос не распознан")

    return text


async def conv_text_to_voice(text) -> bytes:
    """
    Обработка конвертации текста в голос
    """

    if not text:
        raise Exception('Текст не может быть пустым')

    # Создание сессии
    session = Session.from_api_key(
        api_key=config.speechkit_config.api_key,
        folder_id=config.speechkit_config.cloud_folder
    )

    # Получение голосового сообщения из текста
    synthesis = SpeechSynthesis(session)
    out_bytes = synthesis.synthesize_stream(
        text=text,
        voice='oksana',
        format='oggopus')

    logger.log(logging.INFO, msg=f' --> Озвучен текст: {text}')

    if not out_bytes:
        raise Exception("Текст не озвучен")

    return out_bytes
