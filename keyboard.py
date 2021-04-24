from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from settings import GROUP_ID

HASH = f'action=pay-to-group&amount=2&group_id={GROUP_ID}&aid=7743684'
POSITIVE = VkKeyboardColor.POSITIVE
PRIMARY = VkKeyboardColor.PRIMARY
NEGATIVE = VkKeyboardColor.NEGATIVE

WINDOWS = 'https://github.com/FlowHack/FlowParserVk/archive/refs/heads/app/windows.zip'


def start():
    keyboard = VkKeyboard()

    keyboard.add_button('🆘Помощь🆘', PRIMARY)
    keyboard.add_line()

    keyboard.add_button('📀Скачать программу💿', PRIMARY)
    keyboard.add_line()

    keyboard.add_button('Проверить доступ к FPVK', POSITIVE)
    keyboard.add_line()

    keyboard.add_button('⛔Сообщить об ошибке⛔', NEGATIVE)

    return keyboard.get_keyboard()


def inline_vk_donat():
    keyboard = VkKeyboard(inline=True)
    keyboard.add_vkpay_button(HASH)

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

    keyboard.add_openlink_button('Windows', WINDOWS)

    return keyboard.get_keyboard()
