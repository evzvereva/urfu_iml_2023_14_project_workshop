# Проектная практика. Подгруппа 14. Telegram Bot

Данный бот является составной частью проекта "Умный городской гид по Екатеринбургу"
и создан в рамках Проектной практики Подгруппы 14. Бот доступен по адресу:
[https://t.me/PP14CityGuideBot](https://t.me/PP14CityGuideBot)

Сайт проекта доступен по [ссылке](https://urfu-iml-2023-14-project-workshop.streamlit.app/).

## Как использовать Бота

Для начала работы с Ботом необходимо перейти по ссылке [https://t.me/PP14CityGuideBot](https://t.me/PP14CityGuideBot)

### Старт и знакомство с Ботом

Первым шагом нужно запустить бота нажав кнопку или ввести команду ```/start```
![img.png](img/img.png)

Далее можно вводить вопросы по городу Екатеринбургу.

### Доступные функции Меню

Бот может обрабатывать команды:

- ```/help``` - Получение справки по Боту
- ```/about``` - Получение информации о нас
- ```/clear``` - очистка контекста общения с Ботом. Бот поддерживает историю общения и старается давать ответы
  основанные на предыдущих вопросах и ответах
- ```/voice_out``` - у Бота есть возможность озвучить полученный ответ (функция работает в режиме переключателя)

## Технические детали

### Используемые библиотеки

Полный список зависимостей доступен в файле ```requirements.txt``` в текущем каталоге.
Ниже приведен список ключевых библиотек:

- ```aiogram3``` - современная и полностью асинхронная платформа
  для Telegram Bot API
- ```speechkit``` - библиотека для использования речевых технологий на базе машинного
- обучения для создания голосовых помощников (Yandex SpeechKit)
- ```requests``` - модуль для отправки HTTP запросов

### Как запустить

Для запуска бота необходимо запустить скрипт ```main.py``` на выполнение:

```python3 main.py```

Для удобства развертывания бота создан скрипт сборки Docker-контейнера.

### Настройка токенов авторизации

Бот использует сторонние сервисы для обработки голоса и вопросов пользователя,
потому требуется указать токены авторизации на указанных ниже сервисах:

- GPTApi - сервис разработанный в рамках данного проекта
- Yandex Cloud - сервисы распознования и генерации голоса
- Telegram API - интерфейс для авторизации бота в Телеграм

Файл должен называться ```config.yaml``` и иметь следующую структуру:

``` 
tg_bot_config:
  token: '<token>'
speechkit_config:
  cloud_folder: '<folder_id>'
  api_key: '<api_key>'
custom_gpt_config:
  api_key: '<api_key>'
```