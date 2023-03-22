from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from app.config import Config
from app.database.googlesheet.sheets_api import GoogleSheet
from app.database.services.repos import PointRepo, UserRepo
from app.filters import IsAdminFilter
from app.keyboards import Buttons
from app.keyboards.inline.authorization import auth_kb
from app.keyboards.reply.admin import admin_kb, delete_kb
from app.keyboards.reply.send import select_user_kb
from app.states.states import DeleteSG


async def delete_user(msg: Message, user_db: UserRepo):
    users = await user_db.get_all()
    await msg.answer('Оберіть учасника якого треба видалити',
                     reply_markup=await select_user_kb(users))
    await msg.answer('Або знайдіть його через пошук', reply_markup=auth_kb('Email'))
    await DeleteSG.User.set()


async def confirm(msg: Message, user_db: UserRepo, state: FSMContext):
    user = await user_db.get_user_by_name(msg.text)
    if user:
        await msg.answer(f'Ви дійсно бажаєте видалити {user.full_name} видалено з бази даних?', reply_markup=delete_kb)
        await state.update_data(user_id=user.user_id)
    else:
        await msg.answer('Не знайшов такого користувача')
    await DeleteSG.Confirm.set()


async def deleting(msg: Message, user_db: UserRepo, state: FSMContext):
    data = await state.get_data()
    await user_db.delete_user(user_id=int(data['user_id']))
    await msg.answer('Користувача було успішно видалено', reply_markup=admin_kb)
    await state.finish()


async def admin(msg: Message):
    await msg.answer('Вітаю в панелі Адміністратора', reply_markup=admin_kb)


async def update_users(msg: Message, user_db: UserRepo, google_sheet: GoogleSheet, config: Config):
    users = google_sheet.get_users_data(config.misc.user_spreadsheet_id)
    names = [user[0] for user in users]
    count = 0
    for user in await user_db.get_all():
        if user.full_name in names:
            auth_data = users[names.index(user.full_name)][1]
            if user.auth_data != auth_data:
                await user_db.update_user(user.user_id, auth_data=auth_data)
                await msg.answer(f'Оновлено користувача {user.full_name} ({auth_data})')
                count += 1
    await msg.answer(f'Перевірка оновлень пройшла успішно. Оновлено {count} користувачів.')


def setup(dp: Dispatcher):
    dp.register_message_handler(admin, IsAdminFilter(), Command('admin'), state='*')
    dp.register_message_handler(admin, IsAdminFilter(), text='Відмінити', state='*')
    dp.register_message_handler(delete_user, IsAdminFilter(), text=Buttons.admin.delete, state='*')
    dp.register_message_handler(confirm, IsAdminFilter(), state=DeleteSG.User)
    dp.register_message_handler(deleting, text='Так', state=DeleteSG.Confirm)
    dp.register_message_handler(update_users, text=Buttons.admin.update, state='*')