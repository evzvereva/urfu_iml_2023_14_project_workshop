import yaml

def api_login():
    """
    Функция позволяет открыть и прочитать файл с расширением .yaml с настройками для подключения к API GPT бота
    """
    with open("settings.yaml", "r") as file:
        settings = yaml.load(file, Loader=yaml.loader.BaseLoader)
        return settings
