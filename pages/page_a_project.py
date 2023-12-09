import streamlit as st
from run import add_logo # импорт функции для загрузки изображения и названия веб-интерфейса в меню

# Настройка отображения страницы:
st.set_page_config(page_title="О проекте", page_icon="🛠")

# Вызов функции для агрузки изображения и названия веб-интерфейса в меню
add_logo()

# Заголовок страницы:
st.title("О проекте")

st.markdown("Основная цель проекта - создание чат-бота, который будет помогать пользователям в решении задач, "
            "связанных с путешествиями и туризмом в городе Екатеринбург. Это может включать в себя предоставление "
            "информации о различных достопримечательностях, заведениях общественного питания, местах отдыха, "
            "а также помощь в планировании маршрутов и поиске информации о культурных мероприятиях.")

st.markdown("Инновационность данного проекта заключается в использовании технологий машинного обучения и анализа "
            "естественного языка для создания помощника в области туризма по городу Екатеринбургу. \nЧат-бот \"Умный "
            "городской гид\" представляет собой важный инструмент повышения комфорта и информированности "
            "пользователя. \n\nПрактическая ценность умного городского гида заключается в следующем: \n- Экономия "
            "времени: чат-бот позволяет пользователям быстро и эффективно получить необходимую информацию о городской "
            "среде и инфраструктуре. \n- Удобство использования: интерфейс чат-бота прост и понятен, а возможность "
            "распознавания голосовых запросов делает его удобным для использования даже теми, кто не знаком с "
            "информационными технологиями или не имеет возможности набирать текст (например на морозе). \n- Чат-бот "
            "«Умный городской гид» является полезным инструментом для жителей и гостей города, помогающий им "
            "ориентироваться в незнакомом городе, находить интересные места и получать информацию о местах "
            "общественного питания, развлечениях и достопримечательностях города Екатеринбурга. \n\nТехнический подход "
            "включает использование готовой модели GPT для получения ответов на вопросы пользователей, "
            "которые включают описание и предоставляют по запросу пользователя адрес интересующего места."
            "удобства использование чат-бота через смартфон есть возможность использовать мессенджер.")

st.markdown(f'''<p>Для удобства использования "Умный городской гид" через смартфон можно использовать мессенджер <a href=https://t.me/PP14CityGuideBot>Telegram</a>.</p>''', unsafe_allow_html=True)



