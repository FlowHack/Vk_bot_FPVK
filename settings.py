import os
from json import loads
from logging import INFO, Formatter, getLogger
from logging.handlers import RotatingFileHandler

from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv

PATH = os.getcwd()
PATH_ATTACHMENT = os.path.join(PATH, 'attachment')
PATH_DOWNLOADS = os.path.join(PATH, 'downloads.txt')


def __get_logger__(name: str, file: str) -> object:
    """
    Функция создания логгера
    :param name: имя файла логгера
    :return: объект логгера
    """
    if 'log' not in os.listdir(PATH):
        os.mkdir(os.path.join(PATH, 'log'))

    file_logger = getLogger(name)
    file_logger.setLevel(INFO)

    logger_format = (
        '[%(asctime)s] [%(name)s] [%(levelname)s] > %(message)s'
    )
    date_format = '%Y-%m-%d %H:%M:%S'
    formatter = Formatter(fmt=logger_format, datefmt=date_format)

    handler = RotatingFileHandler(
        os.path.join(PATH, 'log', f'{file}.log'),
        maxBytes=5252880,
        backupCount=5
    )

    handler.setFormatter(formatter)
    file_logger.addHandler(handler)

    return file_logger


LOGGER = __get_logger__

logger = LOGGER('settings', 'main')

logger.info('Загружаю переменные виртуального окружения')
load_dotenv()
TOKEN = os.getenv('TOKEN')
GROUP_ID = os.getenv('GROUP_ID')
REPORT_ID = os.getenv('REPORT_ID')

logger.info('Загружаю сообщения ответов для пользователей')
MESSAGES = loads(open('response.json', 'r', encoding='utf-8').read().strip())

scheduler = BackgroundScheduler()
scheduler.start()
