from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from settings import ADMIN_ID

POSITIVE = VkKeyboardColor.POSITIVE
PRIMARY = VkKeyboardColor.PRIMARY
NEGATIVE = VkKeyboardColor.NEGATIVE

PERSON_AGREEMENT = 'https://github.com/FlowHack/FlowParserVk/blob/master/PERSON_AGREEMENT.txt'
LICENSE = 'https://github.com/FlowHack/FlowParserVk/blob/master/LICENSE'
WINDOWS = 'https://github.com/FlowHack/FlowParserVk/archive/refs/heads/master.zip'
POSIX = 'https://github.com/FlowHack/FlowParserVk/archive/refs/heads/master.zip'
MAC = 'https://github.com/FlowHack/FlowParserVk/archive/refs/heads/master.zip'
URL_PAY = 'https://vk.com/donut/club203683544'


def start(id_user):
    keyboard = VkKeyboard()

    keyboard.add_button('🆘Помощь🆘', PRIMARY)
    if (id_user is not None) and (id_user in ADMIN_ID):
        keyboard.add_button('🆘SERVICE🆘', NEGATIVE)
    keyboard.add_line()

    keyboard.add_button('📀Скачать программу💿', PRIMARY)
    keyboard.add_line()

    keyboard.add_button('Проверить доступ к FPVK', POSITIVE)
    keyboard.add_line()

    keyboard.add_button('⛔Сообщить об ошибке⛔', NEGATIVE)

    return keyboard.get_keyboard()


def admin_keyboard():
    keyboard = VkKeyboard(inline=True)

    keyboard.add_button('Включить тех. обслуживание', POSITIVE)
    keyboard.add_line()
    keyboard.add_button('Выключить тех. обслуживание', NEGATIVE)

    return keyboard.get_keyboard()


def inline_vk_donat():
    keyboard = VkKeyboard(inline=True)
    keyboard.add_openlink_button('❗Оплатить подписку❗', URL_PAY)

    return keyboard.get_keyboard()


def inline_cancel():
    keyboard = VkKeyboard(inline=True)
    keyboard.add_button('🚫Отмена🚫', NEGATIVE)

    return keyboard.get_keyboard()


def inline_help():
    keyboard = VkKeyboard(inline=True)

    keyboard.add_button('Главная', POSITIVE)
    keyboard.add_line()

    keyboard.add_button('Парсинг', POSITIVE)
    keyboard.add_line()

    keyboard.add_button('Авторизоваться', POSITIVE)
    keyboard.add_line()

    keyboard.add_button('❓Частые вопросы❓', NEGATIVE)

    return keyboard.get_keyboard()


def inline_help_parse():
    keyboard = VkKeyboard(inline=True)

    keyboard.add_button('Парсинг по группам', POSITIVE)
    keyboard.add_line()

    keyboard.add_button('Парсинг по критериям', POSITIVE)

    return keyboard.get_keyboard()


def inline_help_main():
    keyboard = VkKeyboard(inline=True)
    keyboard.add_button('Авторизоваться', POSITIVE)

    return keyboard.get_keyboard()


def inline_help_parse_group():
    keyboard = VkKeyboard(inline=True)
    keyboard.add_button('Все запросы', POSITIVE)

    return keyboard.get_keyboard()


def inline_help_parse_kriterii():
    keyboard = VkKeyboard(inline=True)

    keyboard.add_button('Выбрать', POSITIVE)
    keyboard.add_line()

    keyboard.add_button('Все запросы', POSITIVE)

    return keyboard.get_keyboard()


def inline_download():
    keyboard = VkKeyboard(inline=True)

    keyboard.add_button('Windows', PRIMARY)
    keyboard.add_line()
    keyboard.add_button('Linux', PRIMARY)

    return keyboard.get_keyboard()


def inline_download_windows():
    keyboard = VkKeyboard(inline=True)

    keyboard.add_openlink_button('Загрузить для Windows', WINDOWS)
    keyboard.add_line()
    keyboard.add_openlink_button('LICENSE', LICENSE)
    keyboard.add_line()
    keyboard.add_openlink_button('Персональное соглашение', PERSON_AGREEMENT)
    keyboard.add_line()
    keyboard.add_button('Ошибки Windows', NEGATIVE)

    return keyboard.get_keyboard()


def inline_download_posix():
    keyboard = VkKeyboard(inline=True)

    keyboard.add_openlink_button('Загрузить для Linux', POSIX)
    keyboard.add_line()
    keyboard.add_openlink_button('LICENSE', LICENSE)
    keyboard.add_line()
    keyboard.add_openlink_button('Персональное соглашение', PERSON_AGREEMENT)

    return keyboard.get_keyboard()

def inline_help_win():
    keyboard = VkKeyboard(inline=True)

    keyboard.add_button('Ошибка: 0x800700E1', PRIMARY)

    return keyboard.get_keyboard()
