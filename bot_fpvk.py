from time import sleep

from requests.exceptions import ConnectionError
from vk_api import VkApi
from vk_api.longpoll import VkLongPoll

from handler import Handler
from settings import GROUP_ID, LOGGER, TOKEN, scheduler, update_settings

LOGGER = LOGGER('main_bot', 'main')


class Bot:
    def __init__(self):
        self.client, self.longpoll = self.get_client()
        self.api = self.client.get_api()
        LOGGER.info('Получен клиент, longpoll и api')
        self.handler = Handler(self.api, self.client, self.longpoll)

    def get_client(self):
        try:
            LOGGER.info('Получение клиента VK')
            client = VkApi(token=TOKEN)

            LOGGER.info('Получение longpoll')
            vk_longpoll = VkLongPoll(
                client, group_id=GROUP_ID
            )

            return client, vk_longpoll

        except ConnectionError:
            LOGGER.error('Нет подключения к интернету, перезапускаю')
            sleep(5)
            self.get_client()


if __name__ == '__main__':
    def clear_downloads():
        LOGGER.warning('Сброс значения downloads')
        update_settings(DOWNLOADS=0)

    scheduler.add_job(
        clear_downloads, trigger='cron', hour='0', minute='58', second='55'
    )

    while True:
        try:
            my_bot = Bot()
        except BaseException as error:
            LOGGER.error(f'Неизестная ошибка! {error}')
            pass
