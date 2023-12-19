import requests
import service
from domain import api
from pydantic import BaseModel

logger = service.getLogger(__name__)

system_template = 'Ты - справочник по городу Екатеринбург. \
Помоги найти короткий ответ. Поиск только по Екатеринбургу.'

class OllamaOptions(BaseModel):
    """
    Класс параметров модели.

    Параметры:
        seed (int): значение, используемое для получения похожих ответов на одинаковые запросы
        temperature (float): влияет на креативность и случайность ответов, допустимый диапазон: от 0 до 1
    """
    seed: int
    temperature: float
    vocab_only: bool
    embedding_only: bool

class OllamaMessage(BaseModel):
    """
    Класс с описанием сообщения.

    Параметры:
        role (str): роль отправителя сообщения
        content (str): содержимое сообщения
    """
    role: str
    content: str

class OllamaRequest(BaseModel):
    """
    Класс запроса.

    Параметры:
        model (str): имя используемой модели
        stream (bool): признак потокового ответа
        options (OllamaOptions): параметры модели
        messages (list[OllamaMessage]): список предыдущих сообщений пользователя и ассистента
    """
    model: str
    stream: bool
    options: OllamaOptions
    messages: list[OllamaMessage]


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

    ollama_settings = settings.get('ollama')
    if ollama_settings is not None:
        url = ollama_settings.get('url')
        model = ollama_settings.get('model')
        if ollama_settings.get('system_template') is not None:
            system_template = ollama_settings.get('system_template')

        headers = {
            'Content-Type': 'application/json; charset=utf-8'
        }

        # создаем класс параметров модели
        options = OllamaOptions(
            seed=42,
            temperature=0.1,
            vocab_only=False,
            embedding_only=False
        )

        # создаем список истории сообщений
        messages = []
        
        add_system = True
        for message in request.history:
            # заполняем историю запросов
            messages.append(
                OllamaMessage(
                    role=message.role.value,
                    content=message.content
                )
            )
            if message.role == api.Role.system:
                add_system = False

        # системного запроса не было, значит добавим свой
        if add_system:
            messages.insert(
                0,
                OllamaMessage(
                    role='system',
                    content=system_template
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
            OllamaMessage(
                role='user',
                content=prompt
            )
        )

        # создаем объект запроса к модели
        data = OllamaRequest(
            model=model,
            stream=False,
            options=options,
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
            
            message = response.json().get('message')
            answer = message.get('content')
            # возвращаем ответ от модели
            return answer
        else:
            # логируем ошибку
            logger.error(f'code: {response.status_code}, body: {response.content}')
            raise Exception(response.status_code)
    else:
        # настройки не заполнены
        raise Exception('settings is empty')
