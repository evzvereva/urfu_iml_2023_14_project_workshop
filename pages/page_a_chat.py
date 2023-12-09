import streamlit as st
import requests
from run import add_logo # импорт функции для загрузки изображения и названия веб-интерфейса в меню

# Импорт функции, которая читает файл с настройками для подключения к модели через API
from api_login import api_login

# Настройка отображения страницы
# st.set_page_config(page_title="Чат", page_icon="🗯️")

# Вызов функции для загрузки изображения и названия веб-интерфейса в меню
add_logo()

# Запись функции в переменную для дальнейшей работы с ней
api_log = api_login.api_login()

if api_log:
    # Если сообщений нет от пользователя, первое, что он видит это приветсвие от ассистента
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": "Добро пожаловать! \n\nС радостью помогу ответить на "
                                                                      "ваши вопросы о "
                                                                      "достопримечательностях, местах отдыха и питания в "
                                                                      "Екатеринбурге. \n\nПожалуйста, уточните, что конкретно "
                                                                      "вас интересует?"}]

    # Создание ключей роль и контент для дальнейшего наполнения
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Получение вопроса от пользователя:
    questions_user = st.chat_input("Напишите ваш вопрос!")

    # Добавление вопроса в словарь для генерации ответа на него от ассистента
    api_log["yandexGPT"]["prompt"] = questions_user

    # Передача url и параметров (API, prompt, history( history по умолчанию список пустой)), в формате json получаем результат
    response = requests.post(api_log["yandexGPT"]["url"], json=api_log["yandexGPT"])

    # При получении вопроса от пользователя, действуют следующие условия
    if questions_user:
        # user:
        with st.chat_message("user"):
            st.markdown(api_log["yandexGPT"]['prompt'])
        # передача вопроса от пользователя
        st.session_state.messages.append({"role": "user", "content": questions_user})
        # assistant:
        answer = response.json()["answer"]
        with st.chat_message("assistant"):
            st.markdown(answer)
        # передача ответа от ассистента
        st.session_state.messages.append({"role": "assistant", "content": answer})
