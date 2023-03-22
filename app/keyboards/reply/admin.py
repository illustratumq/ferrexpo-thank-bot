from app.keyboards.reply.base import *


admin_kb = ReplyKeyboardMarkup(
    row_width=2,
    resize_keyboard=True,
    one_time_keyboard=False,
    keyboard=[
        [KeyboardButton(Buttons.admin.statistic), KeyboardButton(Buttons.admin.rating)],
        [KeyboardButton(Buttons.admin.delete), KeyboardButton(Buttons.admin.update)]
    ]
)

delete_kb = ReplyKeyboardMarkup(
    row_width=2,
    resize_keyboard=True,
    one_time_keyboard=False,
    keyboard=[
        [KeyboardButton('Так')],
        [KeyboardButton('Відмінити')]
    ]
)