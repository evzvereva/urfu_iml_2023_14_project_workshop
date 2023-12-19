import requests
import service
from domain import api
from pydantic import BaseModel

logger = service.getLogger(__name__)

system_template = 'Ты - справочник по городу Екатеринбург. \
Помоги найти короткий ответ. Поиск только по Екатеринбургу.'

class YGPTCompletionOptions(BaseModel):
    """
    Класс параметров модели.

    Параметры:
        stream (bool): признак потокового ответа
        temperature (float): влияет на креативность и случайность ответов, допустимый диапазон: от 0 до 1
        maxTokens (int): ограничение количества токенов, используемых для генерации одного ответа
    """
    stream: bool
    temperature: float
    maxTokens: int

class YGPTMessage(BaseModel):
    """
    Класс с описанием сообщения.

    Параметры:
        role (str): роль отправителя сообщения
        text (str): содержимое сообщения
    """
    role: str
    text: str

class YGPTRequest(BaseModel):
    """
    Класс запроса.

    Параметры:
        modelUri (str): URL доступа к API YandexGPT содержащий имя используемой модели
        completionOptions (YGPTCompletionOptions): параметры модели
        messages (list[YGPTMessage]): список предыдущих сообщений пользователя и ассистента
    """
    modelUri: str
    completionOptions: YGPTCompletionOptions
    messages: list[YGPTMessage]


def chat(request: api.Request) -> str:
    """
    Основная функция формирования ответа на запрос пользователя.

    Параметры:
        request (Request): запрос содержащий параметры чата

    Возвращаемое значение:
        str: ответ на запрос.
    """
    logger.info(request.prompt)

    # читаем настройки
    settings = service.load_settings()

    yandex_gpt = settings.get('yandexGPT')
    if yandex_gpt is not None:
        url = yandex_gpt.get('url')
        api_key = yandex_gpt.get('api_key')
        folder = yandex_gpt.get('folder')
        if yandex_gpt.get('system_template') is not None:
            system_template = yandex_gpt.get('system_template')

        headers = {
            'Authorization': f'Api-Key {api_key}',
            'Content-Type': 'application/json; charset=utf-8',
            'x-folder-id': folder
        }

        # создаем класс параметров модели
        completionOptions = YGPTCompletionOptions(
            stream=False,
            temperature=0.1,
            maxTokens=912
        )

        # создаем список истории сообщений
        messages = []
        
        add_system = True
        for message in request.history:
            # заполняем историю запросов
            messages.append(
                YGPTMessage(
                    role=message.role.value,
                    text=message.content
                )
            )
            if message.role == api.Role.system:
                add_system = False

        # системного запроса не было, значит добавим свой
        if add_system:
            messages.insert(
                0,
                YGPTMessage(
                    role='system',
                    text=system_template
                )
            )
        
        if len(request.history) == 0:
            # если не было истории, то добавим префикс к запросу,
            # чтобы модель отвечала про Екатеринбург даже, если в запросе
            # это не указано
            prompt = f'Вопрос про Екатеринбург: {request.prompt}'
        else:
            prompt = request.prompt

        # добавляем в историю новый запрос пользователя
        messages.append(
            YGPTMessage(
                role='user',
                text=prompt
            )
        )

        # создаем объект запроса к модели
        data = YGPTRequest(
            modelUri=f'gpt://{folder}/yandexgpt-lite',
            completionOptions=completionOptions,
            messages=messages
        )

        # отправляем подготовленный запрос
        response = requests.post(
            url=url,
            headers=headers,
            json=data.model_dump()
        )

        if response.status_code == 200:
            # логируем ответ
            try:
                logger.info(response.json())
            except:
                logger.info(response.content)
            answer = ''
            result = response.json().get('result')
            for alternative in result.get('alternatives'):
                message = alternative.get('message')
                if message.get('role') == 'assistant':
                    answer += message.get('text')
            # возвращаем ответ от модели
            return answer
        else:
            # логируем ошибку
            logger.error(f'code: {response.status_code}, body: {response.content}')
            raise Exception(response.status_code)
    else:
        # настройки не заполнены
        raise Exception('settings is empty')
