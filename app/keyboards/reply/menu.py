from app.keyboards.reply.base import *


menu_kb = ReplyKeyboardMarkup(
    row_width=2,
    resize_keyboard=True,
    one_time_keyboard=False,
    keyboard=[
        [
            KeyboardButton(Buttons.menu.send_points), KeyboardButton(Buttons.menu.my_profile),
        ],
        [
            KeyboardButton(Buttons.menu.rules), KeyboardButton(Buttons.menu.history)
        ],
        [
            KeyboardButton(Buttons.menu.info)
        ]
    ]
)

to_menu_kb = ReplyKeyboardMarkup(
    row_width=1,
    resize_keyboard=True,
    one_time_keyboard=False,
    keyboard=[
        [KeyboardButton(text)] for text in Buttons.menu.go_next
    ]
)

main_menu_kb = ReplyKeyboardMarkup(
    row_width=1,
    resize_keyboard=True,
    one_time_keyboard=False,
    keyboard=[
        [KeyboardButton(Buttons.menu.main_menu)]
    ]
)

my_profile_kb = ReplyKeyboardMarkup(
    row_width=1,
    resize_keyboard=True,
    one_time_keyboard=False,
    keyboard=[
        [KeyboardButton(Buttons.menu.history)],
        [KeyboardButton(Buttons.menu.main_menu)]
    ]
)

pre_history_kb = ReplyKeyboardMarkup(
    row_width=1,
    resize_keyboard=True,
    one_time_keyboard=False,
    keyboard=[
        [KeyboardButton(Buttons.menu.my_send), KeyboardButton(Buttons.menu.to_me_send)],
        [KeyboardButton(Buttons.menu.main_menu)]
    ]
)

back_to_history_kb = ReplyKeyboardMarkup(
    row_width=1,
    resize_keyboard=True,
    one_time_keyboard=False,
    keyboard=[
        [KeyboardButton(Buttons.menu.back_to_history)]
    ]
)

to_auth = ReplyKeyboardMarkup(
    row_width=1,
    resize_keyboard=True,
    one_time_keyboard=False,
    keyboard=[
        [KeyboardButton(Buttons.menu.auth_bt)]
    ]
)