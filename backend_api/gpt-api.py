import embeddings
import service
from domain import api
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from service import ollama, yandex_gpt

logger = service.getLogger(__name__)

app = FastAPI()


@app.get('/')
async def root() -> str:
    """
    Обработчик корневого метода /

    Возвращаемое значение:
        str:
    """
    return ''


@app.post('/chat')
async def chat(request: api.Request) -> JSONResponse:
    """
    Обработчик метода /chat

    Параметры:
        request (Request): запрос содержащий параметры чата

    Возвращаемое значение:
        JSONResponse: ответ в формате JSON.
    """

    # авторизация по токену
    if not service.check_token(request.api_key):
        # если не прошла, то вернем ошибку 401
        logger.error('Authentication failed')
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=api.Error(error='authentication failed').model_dump()
        )

    answer = ''

    # проверяем наличие параметров в запросе
    if request.options is not None:
        if request.options.model == 'ollama':
            logger.info(f'Ollama: request: {request}')

            # проверяем параметр embeddings
            if request.options.embeddings == 'prompt':
                # формируем ответ с учетом локальных документов
                answer = embeddings.chain_prompt(request.prompt)
            elif request.options.embeddings == 'search_docs':
                # ищем документы и возвращаем список в виде строки
                answer = embeddings.search_docs(request.prompt)
            elif request.options.embeddings == 'create_vs':
                # создаем векторное хранилище по локальным документам
                # это нужно для поиска и формирования ответа по ним
                embeddings.create_vectorestore()
                answer = 'created'
            else:
                # embeddings не заполнен, значит отправляем простой запрос
                # к модели
                answer = ollama.chat(request)
                logger.info(f'Ollama: request: {request}')

    if len(answer) == 0:
        # ответ не был сформирован ранее
        try:
            # отправляем запрос в YandexGPT
            answer = yandex_gpt.chat(request)
            logger.info(f'YGPT: request: {request}')
        except Exception as e:
            # логируем ошибку YandexGPT
            logger.error(f'YGPT: {str(e)}')

            # отправляем запрос серверу Ollama
            answer = ollama.chat(request)
            logger.info(f'Ollama: request: {request}')

    # формируем ответ на запрос в формате JSON
    return JSONResponse(
        api.Response(answer=answer).model_dump(),
        status_code=200,
        headers={'Content-Type': 'application/json; charset=utf-8'}
    )


@app.exception_handler(RequestValidationError)
async def exceptionHandler(request: Request, exc: RequestValidationError):
    """
    Обработчик ошибок RequestValidationError.

    Параметры:
        request: The request object.
        exc (RequestValidationError): The exception object.

    Возвращаемое значение:
        None
    """
    logger.error(f'exception: {str(exc)}; body: {exc.body}')
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )
