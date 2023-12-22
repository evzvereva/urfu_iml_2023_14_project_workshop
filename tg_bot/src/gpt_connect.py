import requests
import logging
import json

from history import SimpleMessageHistory
from config import load_config

logger = logging.getLogger(__name__)
config = load_config()


async def question_processing(user_id: int,
                              question: str,
                              history_list: list[SimpleMessageHistory]) -> str:
    """
    Обработка запроса к GPT модели
    """
    if not question:
        raise Exception(f'Вопрос не может быть пустым')

    logging.log(logging.INFO,
                msg=f' ----> Поступил вопрос к ChatGPT: {question}')

    # Заполнение параметров запроса
    url: str = 'https://api.kavlab.ru/chat'
    params: dict = dict()
    params['api_key'] = config.custom_gpt_config.api_key
    params['prompt'] = question
    params['history'] = list()

    # Обработка истории
    for h in history_list:
        params['history'].append({
            'role': h.role,
            'content': h.message
        })

    response = requests.post(url=url, json=params)
    logging.log(logging.INFO,
                msg=f' ----> ChatGPT вернул {response.status_code}: {response.text}')

    if response.status_code != 200:
        raise Exception(f'{response.status_code}: {response.text}')

    result_dict = json.loads(response.text)
    return str(result_dict['answer'])
