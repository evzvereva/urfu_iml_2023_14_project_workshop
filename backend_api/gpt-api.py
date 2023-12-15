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

    if service.check_token(request.api_key) == False:
        logger.error(f'Authentication failed')
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=api.Error(error='authentication failed').model_dump()
        )

    answer = ''

    if request.options is not None:
        if request.options.model == 'ollama':
            logger.info(f'Ollama: request: {request}')
            if request.options.embeddings == 'prompt':
                answer = embeddings.chain_prompt(request.prompt)
            elif request.options.embeddings == 'search_docs':
                answer = embeddings.search_docs(request.prompt)
            elif request.options.embeddings == 'create_vs':
                embeddings.create_vectorestore()
                answer = 'created'
            else:
                answer = ollama.chat(request)
                logger.info(f'Ollama: request: {request}')
    
    if len(answer) == 0:
        try:
            answer = yandex_gpt.chat(request)
            logger.info(f'YGPT: request: {request}')
        except Exception as e:
            logger.error(f'YGPT: {str(e)}')

            answer = ollama.chat(request)
            logger.info(f'Ollama: request: {request}')

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
