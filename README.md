# mmb_bot
## Описание
Бот отслеживает сайт соревнований по ориентированию и сообщает в телеграм, когда начинается регистрация.

## Технологии
Python 3, Telegram Bot API, dotenv, Beautiful Soup

## Развёртывание
Используется Python 3.7.9.


Клонируйте репозиторий и перейдите в него в командной строке:
```
git clone <адрес репозитория>
```
```
cd mmb_bot/
```
Cоздайте и активируйте виртуальное окружение:
```
python -m venv env
```
```
source env/bin/activate
```
Установите зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
Создайте в папке mmb_bot/ файл .env и задайте там переменные окружения:
```
telegram_token = 'ваш_токен'
channel_name = '@имя_канала'
log_channel_name = '@имя_канала_для_логов'
```
Запустите скрипт:
```
python mmb_bot.py
```
