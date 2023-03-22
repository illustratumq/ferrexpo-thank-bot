from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message

from app.config import Config
from app.database.googlesheet.sheets_api import GoogleSheet
from app.database.services.enums import UserStatusEnum
from app.database.services.repos import UserRepo, PointRepo
from app.handlers.private.authorization import authorization_cmd
from app.keyboards.reply.menu import menu_kb, Buttons, to_auth


async def start_cmd(msg: Message, user_db: UserRepo, state: FSMContext, config: Config, google_sheet: GoogleSheet):
    user = await user_db.get_user(msg.from_user.id)
    if not user:
        await authorization_cmd(msg, user_db, google_sheet, config)
    elif user.status == UserStatusEnum.UNAUTHORIZED:
        await msg.answer('Ти не пройшов авторизацію. Давай виправим це!',
                         reply_markup=to_auth)
    else:
        await state.finish()
        text = (
            f'Вітаємо тебе у просторі Вдячності! Ти знаходишься в головному меню.\n\n'
        )
        await msg.answer(text, reply_markup=menu_kb)


async def after_registration_greeting(msg: Message):
    text = (
        'Дякуємо за реєстрацію 💚\n\n'
        'Дослідження показують, що час який людина присвячує вдячності, може зробити її '
        'щасливішою та навіть здоровішою! 💪\n\n'
        'Радіємо, що ти усвідомлено ставишся до свого життя '
        'і знаходиш час, щоб подякувати своїм колегам, за добрі справи, які вони зробили для тебе!🙏'
    )
    await msg.answer(text, reply_markup=menu_kb)


def setup(dp: Dispatcher):
    dp.register_message_handler(start_cmd, CommandStart(), state='*')
    dp.register_message_handler(after_registration_greeting, text=Buttons.menu.go_next, state='*')
    dp.register_message_handler(start_cmd, text=Buttons.menu.main_menu, state='*')


async def users_rating(user_db: UserRepo, point_db: PointRepo) -> list:
    users = await user_db.get_all()
    rating = []
    for user in users:
        rating.append(dict(user_id=user.user_id, point=await point_db.get_user_points(user.user_id, count=True)))
    rating.sort(key=lambda usr: usr['point'], reverse=True)
    return [int(usr['user_id']) for usr in rating]
