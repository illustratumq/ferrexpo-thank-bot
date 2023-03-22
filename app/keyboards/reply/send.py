from app.database.models.user import User
from app.database.services.repos import PointRepo
from app.keyboards.reply.base import *

send_kb = ReplyKeyboardMarkup(
    row_width=1,
    resize_keyboard=True,
    one_time_keyboard=False,
    keyboard=[
        [KeyboardButton(Buttons.send.select_user)],
        [KeyboardButton(Buttons.menu.main_menu)]
    ]
)

confirm_send_kb = ReplyKeyboardMarkup(
    row_width=1,
    resize_keyboard=True,
    one_time_keyboard=False,
    keyboard=[
        [KeyboardButton(Buttons.send.confirm)],
        [KeyboardButton(Buttons.menu.main_menu)]
    ]
)


def select_user_commands(commands: list):
    keyboard = []
    cache = []
    i = 0
    for command in commands:
        cache.append(KeyboardButton(command))
        i += 1
        if i == 2:
            keyboard.append(cache)
            cache = []
            i = 0
    if len(cache) > 0:
        keyboard.append(cache)
    keyboard.append([KeyboardButton(Buttons.menu.main_menu)])
    return ReplyKeyboardMarkup(
        row_width=1,
        resize_keyboard=True,
        one_time_keyboard=False,
        keyboard=keyboard
    )


async def select_user_kb(users: list[User]):
    keyboard = []
    cache = []
    i = 0
    for user in users:
        if user:
            cache.append(KeyboardButton(user.full_name))
            i += 1
            if i == 2:
                keyboard.append(cache)
                cache = []
                i = 0
    if len(cache) > 0:
        keyboard.append(cache)
    keyboard.append([KeyboardButton(Buttons.send.select_user), KeyboardButton(Buttons.menu.main_menu)])
    return ReplyKeyboardMarkup(
        row_width=1,
        resize_keyboard=True,
        one_time_keyboard=False,
        keyboard=keyboard
    )


def values_kb(next_button: bool = False, added_values: list[str] = None):
    keyboard = []
    cache = []
    i = 0
    values: list = Buttons.send.values
    if added_values:
        for val in added_values:
            if val in values:
                values.remove(val)
    for value in values:
        cache.append(KeyboardButton(value))
        i += 1
        if i == 2:
            keyboard.append(cache)
            cache = []
            i = 0
    if len(cache) > 0:
        keyboard.append(cache)
    if next_button:
        keyboard.append(
            [KeyboardButton(Buttons.send.custom_value), KeyboardButton(Buttons.send.next_button)]
        )
    else:
        keyboard += [[KeyboardButton(Buttons.send.custom_value)]]
    return ReplyKeyboardMarkup(
        row_width=1,
        resize_keyboard=True,
        one_time_keyboard=False,
        keyboard=keyboard
    )