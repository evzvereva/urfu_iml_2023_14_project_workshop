from enum import Enum

from pydantic import BaseModel


class Role(str, Enum):
    """
    Перечисление возможных ролей отправителя сообщения.
    """
    system = 'system'
    user = 'user'
    assistant = 'assistant'


class Message(BaseModel):
    """
    Класс с описанием сообщения.

    Параметры:
        role (Role): роль отправителя сообщения
        content (str): содержимое сообщения
    """
    role: Role
    content: str


class ModelOptions(BaseModel):
    """
    Класс параметров модели.

    Параметры:
        model (str): имя модели
        embeddings (str):
            - 'prompt': запрос с использованием embeddings
            - 'search_docs': только поиск документов
            - 'create_vs': создание или обновление векторного хранилища
    """
    model: str
    embeddings: str = ''


class Request(BaseModel):
    """
    Класс запроса в методе chat API.

    Параметры:
        api_key (str): ключ авторизации API
        prompt (str): текст запроса пользователя
        history (list[Message]): список предыдущих сообщений пользователя
         и ассистента
        options (ModelOptions): параметры модели
    """
    api_key: str
    prompt: str
    history: list[Message]
    options: ModelOptions | None = None


class Response(BaseModel):
    """
    Класс ответа метода chat API.

    Параметры:
        answer (str): текст ответа на запрос пользователя
    """
    answer: str


class Error(BaseModel):
    """
    Класс ошибки при выполненнии метода chat API.

    Параметры:
        error (str): описание ошибки
    """
    error: str
