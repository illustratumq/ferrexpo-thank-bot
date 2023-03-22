from aiogram import Dispatcher
from aiogram.types import Message

from app.database.services.repos import UserRepo, PointRepo
from app.handlers.private.start import users_rating
from app.keyboards.reply.admin import admin_kb
from app.keyboards.reply.menu import Buttons


async def rating_table(msg: Message, user_db: UserRepo, point_db: PointRepo):
    users = await users_rating(user_db, point_db)
    table = '<b>🏆 Топ учасників</b>\n\n'
    for user, rang in zip(users[:9], range(1, 11)):
        user = await user_db.get_user(user)
        medal = ''
        if rang == 1:
            medal = '🥇'
        elif rang == 2:
            medal = '🥈'
        elif rang == 3:
            medal = '🥉'
        table += f'{rang}. {medal} {user.full_name} {await point_db.get_user_points(user.user_id, count=True)}\n'
    await msg.answer(table, reply_markup=admin_kb)


def setup(dp: Dispatcher):
    dp.register_message_handler(rating_table, text=Buttons.admin.rating, state='*')
