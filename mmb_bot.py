import datetime
import logging
import os
import sys
from http import HTTPStatus
from time import sleep

import requests
import telebot
from bs4 import BeautifulSoup as bs
from dotenv import load_dotenv

from exceptions import (GetException, ParseException, UnavailableException,
                        err_msg)

url = 'https://mmb.progressor.ru/'
# url = 'http://127.0.0.1:8000/'

load_dotenv()
telegram_token = os.getenv('telegram_token')
channel_name = os.getenv('channel_name')
# это костыль, потом надо будет убрать:
log_channel_name = os.getenv('log_channel_name')

bot = telebot.TeleBot(telegram_token)


def check_tokens():
    """Проверка наличия переменных среды."""
    return all((telegram_token, channel_name))


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    stream=sys.stdout,
)


def err_msg_to_log(error):
    """Отправка сообщения об ошибке в лог."""
    logging.error(err_msg(error))
    bot.send_message(log_channel_name, err_msg(error))


def send_message(bot, message):
    """Отправка сообщения в чат."""
    bot.send_message(channel_name, message)
    logging.info(f'Бот отправил сообщение \"{message}\"')
    bot.send_message(log_channel_name, message)


def get_site_answer():
    """Получение ответа от сайта в виде текста."""
    try:
        response = requests.get(url)
        logging.info('Получен ответ.')
        if response.status_code != HTTPStatus.OK:
            error = (
                f'Ресурс {url} недоступен. '
                f'Код ответа: {response.status_code}'
            )
            raise UnavailableException(error)
        return response.text
    except Exception as error:
        raise GetException(error)


def get_last_mmb(page):
    """Парсингом получаем данные из ответа о предыдущем соревновании."""
    try:
        soup = bs(page, 'html.parser')
        tbls = soup.find_all('table')
        trs = tbls[-1].find_all('tr')
        return trs[1]
    except Exception as error:
        raise ParseException(error)


def main():
    """Основная логика работы бота."""
    if not check_tokens():
        msg = (
            'Отсутствуют обязательные переменные окружения.'
            'Программа принудительно остановлена'
        )
        logging.critical(msg)
        sys.exit(msg)

    try:
        response_text = get_site_answer()
        old_mmb = get_last_mmb(response_text)
        print(old_mmb)
    except Exception as error:
        logging.critical(f'Не могу начать отслеживание: {error}')
        sys.exit(error)

    send_message(bot, 'Начинаем отслеживание...')

    while True:
        try:
            mmb_changed = False
            response_text = get_site_answer()
            current_mmb = get_last_mmb(response_text)
            mmb_changed = (current_mmb != old_mmb)
            old_mmb = current_mmb
            print('очередная итерация...')
            if ((datetime.datetime.now().minute) % 10 and datetime.datetime.now().second <= 20):
                bot.send_message(log_channel_name, str(current_mmb))

            if mmb_changed:
                send_message(bot, 'БЕГОМ ПРОВЕРЯТЬ!!!')

        except GetException as error:
            err_msg_to_log('Не могу получить ответ сайта: ' + str(error))
        except ParseException as error:
            err_msg_to_log('Ошибка парсинга: ' + str(error))
        except Exception as error:
            err_msg_to_log(error)
        finally:
            sleep(10)


if __name__ == '__main__':
    main()
