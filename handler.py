from datetime import datetime
from difflib import SequenceMatcher
from time import time as time_now

from vk_api.tools import VkTools
from vk_api.utils import get_random_id
from vk_api.upload import VkUpload
from vk_api.longpoll import VkEventType
import os
from requests.exceptions import ReadTimeout

import keyboard as create_keyboard
from settings import GROUP_ID, MESSAGES, PATH_ATTACHMENT


class Handler:
    def __init__(self, api, client, longpoll):
        self._tools = VkTools(client)
        self._longpoll = longpoll
        self._client = client
        self._user_id = None
        self._text_message = None
        self._api = api
        self._donat = []
        self._time_donat = 0

        while True:
            try:
                self.longpoll_listen()
            except ReadTimeout as error:
                if "HTTPSConnectionPool(host='im.vk.com', port=443)" in \
                        str(error):
                    pass

    def longpoll_listen(self):
        for event in self._longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                self._text_message = event.text
                self._user_id = event.user_id

                self.message_processing()

    def message_processing(self):
        text = self._text_message.lower()

        if not self.__isMember__():
            self.__send_message__(MESSAGES['not_is_member'])

        if self.__similarity__('start', text) or \
                self.__similarity__('привет', text) or \
                self.__similarity__('хай', text) or \
                self.__similarity__('начать', text):
            keyboard = create_keyboard.start()
            self.__send_message__(MESSAGES['start'], keyboard=keyboard)
        elif self.__similarity__('проверить доступ к fpvk', text):
            if self.__isDon__():
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
                    MESSAGES['report_false'].format(symbols=report[1])
                )
        elif self.__similarity__('🆘помощь🆘', text):
            keyboard = create_keyboard.inline_help()
            self.__send_message__(
                MESSAGES['help'], keyboard=keyboard,
                attachment=self.upload_photo('FPVK_preview.gif')
            )
        elif self.__similarity__('главная', text):
            keyboard = create_keyboard.inline_help_main()
            self.__send_message__(
                MESSAGES['help_main'],
                attachment=self.upload_photo('help_main.png'),
                keyboard=keyboard
            )
        elif self.__similarity__('парсинг', text):
            keyboard=create_keyboard.inline_help_parse()
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
            keyboard = create_keyboard.inline_download()

            self.__send_message__(
                MESSAGES['download'],
                keyboard=keyboard
            )

        else:
            self.__send_message__(
                'Что это?\n\nНапиши мне "start" или "Привет"'
            )

    def report(self):
        while True:
            for event in self._longpoll.check():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    text = event.text
                    user_id = event.user_id

                    if text == '🚫Отмена🚫':
                        return None

                    if len(text) < 70:
                        return False, len(text)

                    self.__send_message__(
                        f'Сообщение об ошибке от пользователя: {user_id}\n\n'
                        f'{text}',
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

    def __isMember__(self):
        isMember = self._api.groups.isMember(
            group_id=GROUP_ID, user_id=self._user_id
        )

        return True if isMember == 1 else False

    def __isDon__(self):
        time = time_now()

        if self._time_donat < time - 300:
            params = {
                'group_id': GROUP_ID,
                'filter': 'donut'
            }
            request = self._tools.get_all(
                'groups.getMembers', max_count=1000, values=params
            )

            donat = request.get('items')
            self.donat = donat
            self.time_donat = time

        return True if self._user_id in self.donat else False

    @staticmethod
    def __similarity__(a: str, b: str):
        matcher = SequenceMatcher(a=a, b=b).ratio()
        matcher = round(matcher, 3)

        return True if matcher >= 0.888 else False
