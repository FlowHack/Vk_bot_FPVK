import os
from datetime import datetime
from difflib import SequenceMatcher

from requests.exceptions import ReadTimeout
from vk_api.longpoll import VkEventType
from vk_api.tools import VkTools
from vk_api.upload import VkUpload
from vk_api.utils import get_random_id

import keyboard as create_keyboard
from settings import (ADMIN_ID, GROUP_ID, LOGGER, MESSAGES, PATH_ATTACHMENT,
                      get_settings, scheduler, update_settings)

LOGGER = LOGGER('handler', 'main')


class Handler:
    def __init__(self, api, client, longpoll):
        self._tools = VkTools(client)
        self._longpoll = longpoll
        self._client = client
        self._user_id = None
        self._text_message = None
        self._api = api
        self._donat = []

        while True:
            try:
                self.__get_don__()
                if int(get_settings()['SCHEDULER_SEND_MESSAGE']) == 0:
                    update_settings(SCHEDULER_SEND_MESSAGE=1)
                    scheduler.add_job(self.__get_don__, 'interval', minutes=5)
                    scheduler.add_job(
                        lambda:
                        self.__send_message__(
                            'За сегодня скачиваний: '
                            f'{self.__get_download__()}',
                            user_id=311966436
                        ),
                        trigger='cron', hour='23', minute='58', second='50'
                    )

                self.longpoll_listen()
            except ReadTimeout as error:
                if "HTTPSConnectionPool(host='im.vk.com', port=443)" \
                        in str(error):
                    print(str(error))
                    LOGGER.error(f'Ошибка Longpool {error}')
                    pass

    def longpoll_listen(self):
        LOGGER.warning('Запуск прослушивания longpoll')
        for event in self._longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                self._text_message = event.text
                self._user_id = event.user_id
                self.message_processing()

    def message_processing(self):
        text = self._text_message.lower()

        if not self.__is_member__():
            self.__send_message__(MESSAGES['not_is_member'])

        if self.__similarity__('start', text) or \
                self.__similarity__('привет', text) or \
                self.__similarity__('хай', text) or \
                self.__similarity__('начать', text):
            keyboard = create_keyboard.start(self._user_id)
            self.__send_message__(MESSAGES['start'], keyboard=keyboard)
        elif self.__similarity__('проверить доступ к fpvk', text):
            if self.__is_don__():
                self.__send_message__(MESSAGES['vkpay_done'])
            else:
                keyboard = create_keyboard.inline_vk_donat()
                self.__send_message__(MESSAGES['vkpay'], keyboard=keyboard)
        elif self.__similarity__('⛔cообщить об ошибке⛔', text):
            keyboard = create_keyboard.inline_cancel()
            self.__send_message__(MESSAGES['report'], keyboard=keyboard)

            report = self.report()
            if report is True:
                self.__send_message__(MESSAGES['report_true'])
            elif report is None:
                self._text_message = 'start'
                self.message_processing()
            else:
                self.__send_message__(
                    MESSAGES['report_false'].format(words=report[1])
                )
        elif self.__similarity__('🆘помощь🆘', text):
            keyboard = create_keyboard.inline_help()
            self.__send_message__(
                MESSAGES['help'], keyboard=keyboard,
                attachment=self.upload_photo('FPVK_preview.png')
            )
        elif self.__similarity__('главная', text):
            keyboard = create_keyboard.inline_help_main()
            self.__send_message__(
                MESSAGES['help_main'],
                attachment=self.upload_photo('help_main.png'),
                keyboard=keyboard
            )
        elif self.__similarity__('парсинг', text):
            keyboard = create_keyboard.inline_help_parse()
            self.__send_message__(
                MESSAGES['help_parse'],
                keyboard=keyboard,
                attachment=self.upload_photo('help_parse_group.png')
            )
        elif self.__similarity__('парсинг по группам', text):
            keyboard = create_keyboard.inline_help_parse_group()
            self.__send_message__(
                MESSAGES['help_parse_group'],
                keyboard=keyboard,
                attachment=self.upload_photo('help_parse_group.png')
            )
        elif self.__similarity__('все запросы', text):
            keyboard = create_keyboard.inline_help_parse()
            self.__send_message__(
                MESSAGES['help_all_requests'],
                attachment=self.upload_photo('help_all_requests.png'),
                keyboard=keyboard
            )
        elif self.__similarity__('парсинг по критериям', text):
            keyboard = create_keyboard.inline_help_parse_kriterii()
            self.__send_message__(
                MESSAGES['help_parse_kriterii'],
                keyboard=keyboard,
                attachment=self.upload_photo('help_parse_kriterii.png')
            )
        elif self.__similarity__('выбрать', text):
            keyboard = create_keyboard.inline_help_parse()
            self.__send_message__(
                MESSAGES['help_choose_request'],
                attachment=self.upload_photo('help_choose_kriterii.png'),
                keyboard=keyboard
            )
        elif self.__similarity__('авторизоваться', text):
            keyboard = create_keyboard.inline_help()
            one = self.upload_photo('help_authorization_info.png')
            two = self.upload_photo('help_authorization_get_token.png')
            three = self.upload_photo('help_authorization_token.png')

            self.__send_message__(
                MESSAGES['help_authorization'],
                keyboard=keyboard,
                attachment=[one, two, three]
            )
        elif self.__similarity__('📀cкачать программу💿', text):
            if int(get_settings()['SERVICE']) == 1:
                self.__send_message__(MESSAGES['download_service'])
            else:
                keyboard = create_keyboard.inline_download()

                self.__send_message__(
                    MESSAGES['download'].format(
                        downloads=self.__get_download__()),
                    keyboard=keyboard
                )
        elif self.__similarity__('windows', text):
            keyboard = create_keyboard.inline_download_windows()

            self.__send_message__(
                MESSAGES['download_windows'],
                keyboard=keyboard
            )
            downloads = self.__get_download__()
            self.__click_download_(downloads)
        elif self.__similarity__('linux', text):
            keyboard = create_keyboard.inline_download_posix()

            self.__send_message__(
                MESSAGES['download_posix'],
                keyboard=keyboard
            )
            downloads = self.__get_download__()
            self.__click_download_(downloads)
        elif text == '🆘service🆘' and self._user_id in ADMIN_ID:
            keyboard = create_keyboard.admin_keyboard()
            self.__send_message__(
                'Команды:', keyboard=keyboard
            )
        elif 'включить тех. обслуживание' == text and \
                self._user_id in ADMIN_ID:
            update_settings(SERVICE=1)
            self.__send_message__('Включил тех. обслуживание =)')
        elif 'выключить тех. обслуживание' == text and \
                self._user_id in ADMIN_ID:
            update_settings(SERVICE=0)
            self.__send_message__('Выключил тех. обслуживание =)')
        elif self.__similarity__('❓частые вопросы❓', text):
            keyboard = create_keyboard.inline_help()
            self.__send_message__(
                MESSAGES['frequently_asked_questions'],
                keyboard=keyboard
            )
        elif text == '1':
            keyboard = create_keyboard.inline_help()
            self.__send_message__(
                MESSAGES['asked_1'],
                keyboard=keyboard
            )

        else:
            self.__send_message__(
                'Что это?\n\nНапиши мне "start", "Начать" или "Привет"'
            )

    def report(self):
        while True:
            for event in self._longpoll.check():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    attachment = []
                    text = event.text
                    user_id = event.user_id

                    if text == '🚫Отмена🚫':
                        return None

                    length = len(text.split(' '))
                    if length < 70:
                        return False, length

                    for i in range(1, len(event.attachments) // 2 + 1):
                        type_attach = event.attachments.get(f'attach{i}_type')
                        attach = event.attachments.get(f'attach{i}')
                        attachment.append(f'{type_attach}{attach}')

                    if len(attachment) > 0:
                        attachment = attachment
                        self.__send_message__(
                            f'Сообщение об ошибке от пользователя: {user_id}'
                            f'\n\n{text}\n\nПрикреплено: '
                            f'{", ".join(attachment)}',
                            user_id=311966436,
                        )
                    else:
                        self.__send_message__(
                            f'Сообщение об ошибке от пользователя: {user_id}'
                            f'\n\n{text}',
                            user_id=311966436
                        )

                    return True

    def upload_photo(self, photo):
        upload = VkUpload(self._client)
        photo = os.path.join(PATH_ATTACHMENT, photo)
        photo = upload.photo_messages(photo)[0]

        owner_id = photo['owner_id']
        photo_id = photo['id']
        access_key = photo['access_key']

        attachment = f'photo{owner_id}_{photo_id}_{access_key}'

        return attachment

    def __send_message__(self, message, user_id=None, **kwargs):
        user_id = user_id or self._user_id

        post = {
            'user_id': user_id,
            'message': message,
            'random_id': get_random_id()
        }

        if len(kwargs) > 0:
            post.update(kwargs)

        self._api.messages.send(**post)
        print(f'{datetime.now()}:::{self._user_id} -> {self._text_message}')

    def __is_member__(self):
        is_Member = self._api.groups.isMember(
            group_id=GROUP_ID, user_id=self._user_id
        )

        return True if is_Member == 1 else False

    def __get_don__(self):
        LOGGER.info('Получение списка донов')
        try:
            params = {
                'group_id': GROUP_ID,
                'filter': 'donut'
            }
            request = self._tools.get_all(
                'groups.getMembers', max_count=1000, values=params
            )

            donat = request.get('items')
            self.donat = donat
        except ConnectionError:
            LOGGER.error('Нет подключения для обновления списка донов')
            return
        LOGGER.info('Успешно')

    def __is_don__(self):
        return True if self._user_id in self.donat else False

    @staticmethod
    def __get_download__():
        return int(get_settings()['DOWNLOADS'])

    @staticmethod
    def __click_download_(downloads):
        downloads = str(downloads + 1)
        update_settings(DOWNLOADS=downloads)

    @staticmethod
    def __similarity__(a: str, b: str):
        matcher = SequenceMatcher(a=a, b=b).ratio()
        matcher = round(matcher, 3)

        return True if matcher >= 0.888 else False
