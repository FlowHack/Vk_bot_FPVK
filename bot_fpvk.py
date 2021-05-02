from time import sleep

from requests.exceptions import ConnectionError
from vk_api import VkApi
from vk_api.longpoll import VkLongPoll

from handler import Handler
from settings import GROUP_ID, LOGGER, PATH_DOWNLOADS, TOKEN, scheduler

LOGGER = LOGGER('main_bot', 'main')


class Bot:
    def __init__(self):
        self.client, self.longpoll = self.__get_client__()
        self.api = self.client.get_api()
        LOGGER.info('Получен клиент, longpoll и api')
        self.handler = Handler(self.api, self.client, self.longpoll)

    def __get_client__(self):
        try:
            LOGGER.info('Получение клиента VK')
            client = VkApi(token=TOKEN)

            LOGGER.info('Получение longpoll')
            vk_longpoll = VkLongPoll(client, group_id=GROUP_ID)

            return client, vk_longpoll

        except ConnectionError:
            LOGGER.error('Нет подключения к интернету, перезапускаю')
            sleep(5)
            self.__get_client__()


if __name__ == '__main__':
    while True:
        def __clear_downloads__():
            LOGGER.warning('Сброс значения downloads')
            with open(PATH_DOWNLOADS, 'w', encoding='utf-8') as file:
                file.write('0')

        scheduler.add_job(__clear_downloads__, trigger='cron', hour='0')

        try:
            my_bot = Bot()
        except BaseException as error:
            LOGGER.error(f'Неизестная ошибка! {error}')
            pass
