import streamlit as st
from PIL import Image
from st_pages import Page, show_pages, add_page_title

# Настройка отображения страницы:
# st.set_page_config(page_title="О Екатеринбурге", page_icon="🏙️", layout="wide")

# Вызов функции из библиотеки для настройки страницы:
add_page_title()

# Переименование отображения страниц в веб-интерфейсе:
show_pages([Page("run.py", "О Екатеринбурге"),
            Page("pages/page_a_chat.py", "Бот-помощник"),
            Page("pages/page_a_project.py", "О проекте"),
            Page("pages/page_a_team.py", "Команда"),
            Page("pages/page_help.py", "Помощь")])

# Открываем изображение и отображаем в веб-интерфейсе:
img = Image.open("image_and_history_city/ekaterinburg.jpeg")
st.image(img, width=700, caption="Екатеринбург, Россия")

# Чтение файла для дальнейшей загрузки информации о городе Екатеринбурге:
with open("image_and_history_city/ekaterinburg.txt", "r") as file:
    content = file.read()
    st.markdown(content)


def add_logo():
    """
    Позволяет добавить изображение и главное название веб-интерфейса в меню с помощью streamlit.markdown.
    """
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url(https://avatars.mds.yandex.net/i?id=5c17d44202c2993115ce701239c02807c5c846c3-10608704-images-thumbs&n=13);
                background-repeat: no-repeat;
                padding-top: 100px;
                background-position: 1px 1px;
            }
            [data-testid="stSidebarNav"]::before {
                content: "Умный городской гид";
                margin-left: 20px;
                margin-top: 20px;
                font-size: 30px;
                position: relative;
                top: 100px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


add_logo()
