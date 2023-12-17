import streamlit as st
from run import add_logo # импорт функции для загрузки изображения и названия веб-интерфейса

# Настройка отображения страницы:
st.set_page_config(page_title="Помощь", page_icon=":books:")

# Вызов функции для агрузки изображения и названия веб-интерфейса в меню
add_logo()

# Заголовок страницы
st.title("Часто задаваемые вопросы")
st.title("")

def get_answer_to_question(question, answer):
    """
    На вход функция принимает два параметра со стороковым типом данных question: "вопрос" и answer: "ответ".
    Возвращает результат для вывода на странице веб-интерфейса с помощью streamlit.expander и скрывающий текстс
    помощью streamlit.markdown.
    """
    with st.expander(question):
        st.markdown(f'''<p style="font-size:13px;">{answer}</p>''', unsafe_allow_html=True)


# Вызов функции с передаче параметров для отображения в веб-интерфейсе в разделе "Часто задаваемые вопросы":
get_answer_to_question("Как начать пользоваться умным городским гидом?",
                       'Для начала использования умного городского гида в интерфейсе приложения или веб-сайта Вам '
                       'необходимо перейти во вкладку “Бот-помощник”. Здесь Вы можете задать интересующий Вас вопрос, '
                       'например, “Куда можно сходить погулять в Екатеринбурге?”. Затем ожидайте ответа от '
                       'бота-помощника. Ответ может быть представлен в виде навигации, ведущей к интересным местам, '
                       'или описания конкретного места/заведения.')

get_answer_to_question("Могу ли я пользоваться умным городским гидом через Telegram?",
                       "Да, конечно. Вы можете воспользоваться ботом в <a href=https://t.me/PP14CityGuideBot>Telegram</a>.")

get_answer_to_question("Какой вопрос нужно задать, чтобы найти интересное место для прогулки в Екатеринбурге?",
                       'Напишите, например вопрос "Какие есть парки в Екатеринбурге".')

get_answer_to_question("Где я могу оставить рекомендации или пожелания?", "Пожелания и рекомендации Вы можете "
                                                                          "оставить через форму обратной связи по "
                                                                          "<a href=https://forms.gle"
                                                                          "/Wi1HXgCzzARhBDx87>ссылке</a>.")

get_answer_to_question("Если возникла техническая неполадка, куда могу обратиться?", "Напишите, пожалуйста, на "
                                                                                     "электронную почту "
                                                                                     "team.smart.guide.city@gmail"
                                                                                     ".com, отправив подробное "
                                                                                     "описание проблемы.")
