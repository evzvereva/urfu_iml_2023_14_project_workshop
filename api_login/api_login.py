import streamlit as st

def api_login():
    """
    Функция позволяет вызвать функцию upload_login_app_setting() открыть и прочитать файл с расширением .yaml с
    настройками для подключения к API GPT бота
    """
    api_json = {"yandexGPT": {
        "api_key": "",
        "prompt": "",
        "history": []}}

    api_json["yandexGPT"]["api_key"] = st.secrets["api_key"]
    api_json["yandexGPT"]["url"] = st.secrets["url"]
    return api_json
