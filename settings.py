import os
from json import loads
from logging import INFO, Formatter, getLogger
from logging.handlers import RotatingFileHandler

from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv

PATH = os.getcwd()
PATH_ATTACHMENT = os.path.join(PATH, 'attachment')
PATH_SETTINGS = os.path.join(PATH, 'settings.settings')
TEMPLATE_SETTINGS = """
DOWNLOADS={DOWNLOADS}
SCHEDULER_SEND_MESSAGE={SCHEDULER_SEND_MESSAGE}
SERVICE={SERVICE}
"""
ADMIN_ID = [311966436]


def get_logger(name: str, file: str) -> object:
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


def create_settings():
    __template__ = TEMPLATE_SETTINGS.format(
        DOWNLOADS='0', SCHEDULER_SEND_MESSAGE='0', SERVICE='0'
    )
    with open(PATH_SETTINGS, 'w', encoding='utf-8') as write_file:
        write_file.write(__template__.strip())


create_settings()


def get_settings() -> dict:
    with open(PATH_SETTINGS, 'r', encoding='utf-8') as __file:
        __settings__ = __file.read().strip().split()

    settings = {}
    for i in __settings__:
        item = i.strip().split('=')
        settings[str(item[0])] = str(item[1])

    return settings


def update_settings(**kwargs):
    settings = get_settings()
    for item in kwargs.items():
        item = list(item)
        settings[str(item[0])] = str(item[1])

    __template = TEMPLATE_SETTINGS.format(
        DOWNLOADS=settings['DOWNLOADS'],
        SCHEDULER_SEND_MESSAGE=settings['SCHEDULER_SEND_MESSAGE'],
        SERVICE=settings['SERVICE']
    )

    with open(PATH_SETTINGS, 'w', encoding='utf-8') as __file:
        __file.write(__template.strip())


LOGGER = get_logger

logger = LOGGER('settings', 'main')

logger.info('Загружаю переменные виртуального окружения')
load_dotenv()
TOKEN = os.environ.get('TOKEN')
GROUP_ID = os.environ.get('GROUP_ID')
REPORT_ID = os.environ.get('REPORT_ID')

logger.info('Загружаю сообщения ответов для пользователей')
MESSAGES = loads(open('response.json', 'r', encoding='utf-8').read().strip())

scheduler = BackgroundScheduler()
scheduler.start()
