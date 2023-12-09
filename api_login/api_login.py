import streamlit as st

def api_login():
    """
    Функция позволяет вызвать функцию upload_login_app_setting() открыть и прочитать файл с расширением .yaml с
    настройками для подключения к API GPT бота
    """
    api_json = {"yandexGPT": {
        "url": st.secrets["url"],
        "api_key": st.secrets["api_key"],
        "prompt": "",
        "history": []}}
    return api_json
