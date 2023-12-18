# УРФУ_ИМО_2023. Проектный практикум - «Умный городской гид». Команда №14

# Чат-бот «Умный городской гид»
Целью проекта является создание чат-бота «Умный городской гид» (далее - программный продукт), который будет предоставлять информацию и помогать в решении различных задач, связанных с путешествиями и туризмом по городу Екатеринбургу.
Более детальная информация о проекте представлена на его сайте, расположенном по адресу [ссылке](https://urfu-iml-2023-14-project-workshop.streamlit.app/).
Программный продукт «Умный городской гид» состоит из следующих компонентов:
- Web приложение (реализовано на платформе streamlit)
- API (серверная часть)
- Телеграм-бот<br>
Web приложение обеспечивает интуитивно простой интерфейс для взаимодействия с пользователем. Описание API представлено в папке «backend_api» в файле «README.md» ([ссылка на данный файл](/backend_api/README.md)). Телеграм-бот был включен в состав программного продукта для возможности получать информацию в телеграме, обеспечив удобство использование данного сервиса на мобильных устройствах (мобильные телефоны, планшеты и т.д.), его описание можно найти в соответствующем каталоге проекта в файле «README.md» ([ссылка на данный файл](/tg_bot/README.md))

## Начало работы
Для удобства развертывания проекта для каждый из трех раннее упомянутых компонетов имеет файл «requirements.txt», содержащий перечень необходимых пакетов, подлежащих установке. В дополнение к этому для API и телеграм-бота были подготовлены «Docker».

Для начало работы требуется установить все три компонента програмного продукта с необходимыми пакетами:
1. Установка API осуществляется с помощью Dockerfile, подробное описание процесса установки можно посмотреть перейдя по [ссылке](/backend_api/README.md)(см. раздел «Установка»)  
2. Установка Телеграм-бот осуществляется командой "docker build -t tg-bot" из каталога "tg_bot/", а запуск командой "python3 main.py"
3. Установка необходимых пакетов для Web приложения осуществляется из корневого каталога командой в терминале "pip install -r requirements.txt", далее необходимо выполнить следующую команду "python3 run.py".

## Пример использования чат-бота

Необходимую информацию можно получить от чат-бота на сайте проекта или с помощью телеграма.

### Запрос информации на сайте проекта
1. Для получения информации от чат-бота «Умный городской гид» необходимо зайти на страницу проекта по [ссылке](https://urfu-iml-2023-14-project-workshop.streamlit.app/) и перейти на вкладку «Бот-помощник» (на рисунке 1 выделена прямоугольником зеленого цвета).
<image src="/image_and_history_city/web.png" alt="Рисунок 1. Сайт проекта"><i>Рисунок 1. Сайт проекта</i>

2. В поле ввода запроса (на рисунке 2 выделено прямоугольником зеленого цвета) указать какую информацию о Екатеринбурге необходимо получить.
<image src="/image_and_history_city/request_web_1.png" alt="Рисунок 2. Поле ввода запроса"><i>Рисунок 2. Поле ввода запроса</i>

3. На рисунке 3 и 4 показаны результаты работы бота при следующем запросе информации - "Рестораны Екатеринбурга лучшие" (на рисунках выделено прямоугольниками зеленого цвета).
<image src="/image_and_history_city/result_web_1.png" alt="Рисунок 3. Результаты работы «Бота-помощника»"><i>Рисунок 3. Результаты работы «Бота-помощника»</i>
<br><br>
<image src="/image_and_history_city/result_web_2.png" alt="Рисунок 4. Результаты работы «Бота-помощника»"><i>Рисунок 4. Результаты работы «Бота-помощника»</i>
<br><br>
Ответы на часто задаваемые вопросы при работе с чат-ботом можно посмотреть на вкладке «Помощь» сайта проекта или перейти по [ссылке](https://urfu-iml-2023-14-project-workshop.streamlit.app/Помощь)

### Запрос информации в телеграме
Для использования чат-бота в телеграме потребуется сначала его установить. В интернет браузере на мобильном телефоне или планшете требуется перейти по следующей [ссылке](https://t.me/PP14CityGuideBot) и нажать на кнопку «СТАРТ» (выделена прямоугольником зеленого цвета).   
<image src="/image_and_history_city/telegramm_start.jpg" width="349" height="775" alt="Установка «Бота-помощника»">
<br><i>Рисунок 5. Установка «Бота-помощника»</i>
<br><br>
На экране появится сообщение, о готовности к работе «Бота-помощника».
<image src="/image_and_history_city/Bot_ready.jpg" width="349" height="775" alt="«Бот-помощник» готов к работе">
<br><i>Рисунок 6. «Бот-помощник» готов к работе</i>
<br><br>
В поле ввода запроса (на рисунке 7 выделено прямоугольником зеленого цвета) указать какую информацию о Екатеринбурге необходимо получить.<br>
<image src="/image_and_history_city/telegramm_request.jpg" width="349" height="775" alt="Рисунок 7. Поле ввода запроса">
<br><i>Рисунок 7. Поле ввода запроса</i>
<br><br>
На рисунке 8 показаны результаты работы бота при следующем запросе информации - "Лучшие три театра Екатеринбурга" (на рисунках выделено прямоугольниками зеленого цвета).
<image src="/image_and_history_city/telegramm_result.jpg" width="349" height="775" alt="Рисунок 8. Результаты работы «Бота-помощника»">
<br><i>Рисунок 8. Результаты работы «Бота-помощника»</i>
<br><br>
Чат-бот имеет функцию «Переключения режима озвучивания», данная функция позволяет получать информацию от чат-бота в голосовом режиме. Более подробную информацию о функциях и командах чат-бота можно посмотреть, перейдя по следующей [ссылке](/tg_bot/README.md).

## Информация о членах команды и их ролях

| КОМАНДА  | |
|-------------------|---------------------------------------------|
| Мулявин Александр | Fullstack developer. Создание телеграм-бота, настройка интерфейса и подключение к API моделей Ollama, YandexGPT|
| Зверева Екатерина | Менеджер проекта, fullstack developer. Контролирует ход выполнения задач и соблюдение сроков. Отвечает за настройку и наполнение веб-интерфейса с помощью библиотеки Streamlit, подключение чата к API модели Ollama, YandexGPT|
| Одинцов Сергей    | QA engineer. Ручное тестирование телеграм-бота|
| Кузнецов Александр| ML Engineer. Поиск и настройка модели Ollama, написание API к модели|
| Косташ Денис      | QA engineer. Ручное тестирование веб-интерфейса|
|Телегинский Владислав| Технический писатель. Написание документации веб приложения, телеграм-бота и API|

## Условия лицензии
Данный программный продукт распространяется по принципу «OpenSource». Программный продукт является бесплатным для личного использования, допускается вносить изменения в него (изменять код) для его улучшения. Авторские права при этом сохраняются за группой разработчиков, указанных в разделе «Информация о членах команды и их ролях».
В коммерческих целях допускается использовать программный продукт только с письменного разрешения группы разработчиков.
