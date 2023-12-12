import domain
import requests
import service
from pydantic import BaseModel

logger = service.getLogger(__name__)

system_template = 'Ты - справочник по городу Екатеринбург. \
Помоги найти короткий ответ. Поиск только по Екатеринбургу.'

class OllamaOptions(BaseModel):
    seed: int
    temperature: float
    vocab_only: bool
    embedding_only: bool

class OllamaMessage(BaseModel):
    role: str
    content: str

class OllamaRequest(BaseModel):
    model: str
    stream: bool
    options: OllamaOptions
    messages: list[OllamaMessage]

def chat(request: domain.Request) -> str:
    """
    The main function of responding to user requests, which uses the Ollama API.

    Args:
        request (Request): The request object containing the chat data.

    Returns:
        str: The response to the request.
    """
    logger.info(request.prompt)

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

        options = OllamaOptions(
            seed=42,
            temperature=0.1,
            vocab_only=False,
            embedding_only=False
        )

        messages = []
        
        add_system = True
        for message in request.history:
            messages.append(
                OllamaMessage(
                    role=message.role.value,
                    content=message.content
                )
            )
            if message.role == domain.Role.system:
                add_system = False

        if add_system:
            messages.insert(
                0,
                OllamaMessage(
                    role='system',
                    content=system_template
                )
            )
        
        if len(request.history) == 0:
            prompt = f'Вопрос про Екатеринбург: {request.prompt}'
        else:
            prompt = request.prompt

        messages.append(
            OllamaMessage(
                role='user',
                content=prompt
            )
        )

        data = OllamaRequest(
            model=model,
            stream=False,
            options=options,
            messages=messages
        )

        response = requests.post(
            url=url,
            headers=headers,
            json=data.model_dump()
        )

        if response.status_code == 200:
            try:
                logger.info(response.json())
            except:
                logger.info(response.content)
            
            message = response.json().get('message')
            answer = message.get('content')
            return answer
        else:
            logger.error(f'code: {response.status_code}, body: {response.content}')
            raise Exception(response.status_code)
    else:
        raise Exception('settings is empty')
