from gpt4all import GPT4All
import domain
import service

logger = service.getLogger(__name__)

system_template = 'Ты городской гид по городу Екатерибург. \
Отвечаешь на вопросы только про город Екатеринбург и только на русском языке.'

model = None
settings = service.load_settings()
gpt4all_settings = settings.get('GPT4All')

def init_model() -> None:
    """
    GPT4All model initialization.
    """
    global model, system_template, gpt4all_settings

    if model is None:
        gpt4all_path = gpt4all_settings.get('model_path')
        gpt4all_model = gpt4all_settings.get('model_name')

        if gpt4all_settings.get('system_template') is not None:
            system_template = gpt4all_settings.get('system_template')

        model = GPT4All(
            model_name=gpt4all_model,
            model_path=gpt4all_path,
            device=gpt4all_settings.get('device'),
            allow_download=False
        )

def chat(request: domain.Request) -> str:
    """
    The main function of responding to user requests, which uses the GPT4All model.

    Args:
        request (Request): The request object containing the chat data.

    Returns:
        str: The response to the request.
    """
    global model, gpt4all_settings

    logger.info(request.prompt)

    init_model()

    answer = ''

    # default prompt template
    prompt_template = '### Human: \n{0}\n### Assistant:\n'
    
    if gpt4all_settings.get('prompt_template') is not None:
        prompt_template = gpt4all_settings.get('prompt_template')

    with model.chat_session(
        system_prompt=system_template,
        prompt_template=prompt_template
    ):

        for message in request.history:
            model.current_chat_session.append(
                {
                    'role': message.role.value,
                    'content': message.content
                }
            )
        
        if len(request.history) > 0:
            logger.info(f'Session: {model.current_chat_session}')

        answer = model.generate(
            request.prompt,
            max_tokens=912,
            temp=0.3,
            top_k=40,
            top_p=0.9,
            repeat_penalty=1.1,
            repeat_last_n=64,
            n_batch=9
        )

        if '###' in answer:
            logger.info(f'Answer with ###: {answer}')
            answer = answer[:answer.find('###')]

    logger.info(f'Answer: {answer}')

    return answer
