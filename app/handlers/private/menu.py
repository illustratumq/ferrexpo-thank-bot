from aiogram import Dispatcher
from aiogram.types import Message

from app.database.services.repos import UserRepo, PointRepo
from app.keyboards.reply.menu import main_menu_kb, Buttons, my_profile_kb

rules_str = '''
<b>Вдячність</b> - це позитивний емоційний стан, коли людина визнає та цінує те, що отримала у житті. <b>Вдячність має велику силу!</b>

За допомогою цього простору, ми прагнемо зробити Практику Вдячності простою, фановою та приємною! 🧡 На початку кожного місяця, ти будеш отримувати 100 wellcoin-ів (балів). Кількість wellcoin-ів до своїх подяк ти можеш розподіляти їх на власний розсуд.

Цей чат-бот допоможе тобі:
✅ швидко та зручно відправити твої теплі слова колегам;
✅ розподіляти та рахувати wellcoin-и 💚
✅ отримувати подяки від співробітників за твої добрі вчинки;
✅ отримувати корисну інформацію та практики для підтримки себе у ресурсному стані 😎

<b>🔹 Передача своїх wellcoin-ів (балів) складається з 4 кроків:</b>
1 - вибір колеги, кому ти хочеш подякувати за добро, яке вона/він зробили для тебе у цьому місяці.
2 - написати теплі слова та детальніше розписати, за що саме ти дякуєш.
3 - вказати кількість wellcoin-ів, які хочеш додати.
4 - вкажи, за яку саме цінність ти вдячна/-ний?

В кінці місяця ми підрахуємо бали та визначимо переможців, які зібрати найбільшу кількість wellcoin-ів - зробили добра для своїх колег❤️️
'''


async def profile(msg: Message, user_db: UserRepo, point_db: PointRepo):
    user = await user_db.get_user(msg.from_user.id)
    points = await point_db.get_user_points(user.user_id, count=True)
    points_this_month = await point_db.get_user_points(user.user_id, count=True, this_month=True)
    text = (
        f'<b>Отримані wellcoin-и 💚</b>\n'
        f'В цьому місяці: {points_this_month}\n'
        f'За весь період: {points}\n\n'
        f'<b>В цьому місяці ти можеш ще віддати: {user.gift_points}💚</b>'
    )
    await msg.answer(text, reply_markup=my_profile_kb)


async def rules(msg: Message):
    await msg.answer(rules_str, reply_markup=main_menu_kb)


async def info(msg: Message):
    text = (
        'Стаття "5 переваг вдячності для здоров\'я"💚\n\n'
        'Реальні дослідження, які показують позитивний вплив '
        'на наше здоров\'я та самопочуття:\n\nhttps://www.wellright.com/blog/5-wellness-benefits-of-gratitude '
    )
    await msg.answer(text, reply_markup=main_menu_kb)


async def unused_menu(msg: Message):
    await msg.answer('Цей розділ у розробці 🙃', reply_markup=main_menu_kb)


def setup(dp: Dispatcher):
    dp.register_message_handler(profile, text=Buttons.menu.my_profile, state='*')
    dp.register_message_handler(rules, text=Buttons.menu.rules, state='*')
    dp.register_message_handler(info, text=Buttons.menu.info, state='*')
