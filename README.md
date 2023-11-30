# Dota 2 Player Statistics

## Описание

Dota 2 Player Statistics - это веб-приложение, которое предоставляет пользователям статистику игроков Dota 2.

## Особенности

- Просмотр статистики игроков Dota 2
- Возможность оценивать игроков
- Система комментариев для игроков

## Технологии

- Django
- Python
- Dota 2 API
- JavaScript
- HTML/CSS

## Установка

Для запуска проекта локально выполните следующие шаги:

1. Клонируйте репозиторий:

`git clone https://github.com/sndmndss/dota2-site.git`

`cd dota2-player-statistics`

2. Установите виртуальное окружение и активируйте его:

`python -m venv venv source venv/bin/activate` # Для Unix или MacOS
`venv\Scripts\activate` # Для Windows

3. Установите зависимости:

`pip install -r requirements.txt`

 
4. Настройте переменные окружения, создав файл `.env` в корне проекта с следующим содержимым:

`SECRET_KEY=your_secret_key `

`STEAM_LOGIN=your_steam_login`

`STEAM_PASSWORD=your_steam_password`

5. Выполните миграции:

`python manage.py migrate`

6. Запустите сервер разработки:

`uvicorn d2site.asgi:application --host 127.0.0.1 --port 8000 --reload`

## Использование

После запуска сервера перейдите по адресу `http://127.0.0.1:8000/` в вашем браузере, чтобы начать использовать приложение.
