import streamlit as st
from PIL import Image
from pathlib import Path
from streamlit.source_util import get_pages as st_get_pages
from streamlit.source_util import _on_pages_changed as st_on_pages_changed

# Заголовок страницы
st.title("O Екатеринбурге")

def st_page_rename(pages_name: dict[str, str]) -> None:
    """
    Переименование страниц в меню. На вход функция принимает название файла и новое название в веб-интерфейсе
    """
    pages = st_get_pages("")
    for page_k, page_v in pages.items():
        script_path = Path(page_v["script_path"])

        for page_name_k, page_name_v in pages_name.items():
            name_path = Path(page_name_k)

            if Path.samefile(script_path, name_path):
                page_v["page_name"] = page_name_v

    st_on_pages_changed.send()

def main_app() -> None:
    """
    Запуск основного приложения
    """

    st_page_rename({"run.py": "О Екатеринбурге",
                    "pages/page_a_chat.py": "Бот-помощник",
                    "pages/page_a_project.py": "О проекте",
                    "pages/page_a_team.py": "Команда",
                    "pages/page_help.py": "Помощь"})


main_app()

# Открываем изображение и отображаем в веб-интерфейсе:
img = Image.open("image_and_history_city/ekaterinburg.jpeg")
st.image(img, width=None, caption="Екатеринбург, Россия")

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
