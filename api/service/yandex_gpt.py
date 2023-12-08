import domain
import service
import requests
from pydantic import BaseModel

logger = service.getLogger(__name__)

system_template = 'Ты - справочник по городу Екатеринбург. \
Помоги найти короткий ответ. Поиск только по Екатеринбургу.'

class YGPTCompletionOptions(BaseModel):
    stream: bool
    temperature: float
    maxTokens: int

class YGPTMessage(BaseModel):
    role: str
    text: str

class YGPTRequest(BaseModel):
    modelUri: str
    completionOptions: YGPTCompletionOptions
    messages: list[YGPTMessage]

def chat(request: domain.Request) -> str:
    """
    The main function of responding to user requests, which uses the YandexGPT API.

    Args:
        request (Request): The request object containing the chat data.

    Returns:
        str: The response to the request.
    """
    logger.info(request.prompt)

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

        completionOptions = YGPTCompletionOptions(
            stream=False,
            temperature=0.3,
            maxTokens=912
        )

        messages = []
        
        add_system = True
        for message in request.history:
            messages.append(
                YGPTMessage(
                    role=message.role.value,
                    text=message.content
                )
            )
            if message.role == domain.Role.system:
                add_system = False

        if add_system:
            messages.insert(
                0,
                YGPTMessage(
                    role='system',
                    text=system_template
                )
            )
        
        messages.append(
            YGPTMessage(
                role='user',
                text=request.prompt
            )
        )

        data = YGPTRequest(
            modelUri=f'gpt://{folder}/yandexgpt-lite',
            completionOptions=completionOptions,
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
            answer = ''
            result = response.json().get('result')
            for alternative in result.get('alternatives'):
                message = alternative.get('message')
                if message.get('role') == 'assistant':
                    answer += message.get('text')
            return answer
        else:
            logger.error(f'code: {response.status_code}, body: {response.content}')
            raise Exception(response.status_code)
    else:
        raise Exception('settings is empty')
