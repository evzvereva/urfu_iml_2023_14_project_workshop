import service
from domain import api
from gpt4all import GPT4All

logger = service.getLogger(__name__)

system_template = 'Ты городской гид по городу Екатерибург. \
Отвечаешь на вопросы только про город Екатеринбург и только на русском языке.'

model = None
settings = service.load_settings()
gpt4all_settings = settings.get('GPT4All')


def init_model() -> None:
    """
    Функция инициализации модели GPT4All.

    Возвращаемое значение:
        None
    """
    global model, system_template, gpt4all_settings

    # инициализируем модель только один раз
    # при этом происходит загрузка в память GPU
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


def chat(request: api.Request) -> str:
    """
    Основная функция формирования ответа на запрос пользователя.

    Параметры:
        request (Request): запрос содержащий параметры чата

    Возвращаемое значение:
        str: ответ на запрос.
    """
    global model, gpt4all_settings

    logger.info(request.prompt)

    init_model()

    answer = ''

    # шаблон по умолчанию
    prompt_template = '### Human: \n{0}\n### Assistant:\n'

    if gpt4all_settings.get('prompt_template') is not None:
        prompt_template = gpt4all_settings.get('prompt_template')

    # начинаем сессию чата
    with model.chat_session(
        system_prompt=system_template,
        prompt_template=prompt_template
    ):

        # заполняем сессию историем сообщений
        for message in request.history:
            model.current_chat_session.append(
                {
                    'role': message.role.value,
                    'content': message.content
                }
            )

        # логирование для анализа
        if len(request.history) > 0:
            logger.info(f'Session: {model.current_chat_session}')

        # формируем ответ
        answer = model.generate(
            f'Вопрос про Екатеринбург: {request.prompt}',
            max_tokens=912,
            temp=0.1,
            top_k=40,
            top_p=0.9,
            repeat_penalty=1.1,
            repeat_last_n=64,
            n_batch=9
        )

        # обрезаем ответ, если он содержит ###
        # иногда модель начинает после ответа сама задавать вопросы
        # и отвечает на них, это начинается после ###
        if '###' in answer:
            logger.info(f'Answer with ###: {answer}')
            answer = answer[:answer.find('###')]

    # логируем ответ
    logger.info(f'Answer: {answer}')

    return answer
