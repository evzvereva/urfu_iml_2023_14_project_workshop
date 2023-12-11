import domain
import service
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from service import gpt4all, yandex_gpt

logger = service.getLogger(__name__)

app = FastAPI()

@app.get('/')
async def root() -> str:
    """
    Handler for the root endpoint.
    
    Returns:
        str: The message to display at the root endpoint.
    """
    return ''

@app.post('/chat')
async def chat(request: domain.Request) -> JSONResponse:
    """
    Handler for the '/chat' endpoint.

    Args:
        request (Request): The request object containing the chat data.

    Returns:
        JSONResponse: The response to the request.
    """

    if service.check_token(request.api_key) == False:
        logger.error(f'Authentication failed')
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=domain.Error(error='authentication failed').model_dump()
        )

    answer = ''

    if request.service == 'gpt4all':
        answer = gpt4all.chat(request)
        logger.info(f'GPT4all: request: {request}')        
    else:
        try:
            answer = yandex_gpt.chat(request)
            logger.info(f'YGPT: request: {request}')
        except Exception as e:
            logger.error(f'YGPT: {str(e)}')

            answer = gpt4all.chat(request)
            logger.info(f'GPT4all: request: {request}')

    return JSONResponse(
        domain.Response(answer=answer).model_dump(),
        status_code=200,
        headers={'Content-Type': 'application/json; charset=utf-8'}
    )

@app.exception_handler(RequestValidationError)
async def exceptionHandler(request: Request, exc: RequestValidationError):
    """
    Exception handler for RequestValidationError.

    Args:
        request: The request object.
        exc (RequestValidationError): The exception object.

    Returns:
        None
    """
    logger.error(f'exception: {str(exc)}; body: {exc.body}')
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )
