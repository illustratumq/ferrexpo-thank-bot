from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from app.keyboards.reply.menu import main_menu_kb


async def non_state_message(msg: Message, state: FSMContext):
    await msg.answer(
        'Чат-бот запрограмований на спілкування кнопками 😉\n'
        'Написаний вручну текст не обробляється. '
        'Щоб продовжити діалог, натисніть на кнопку "Головне меню"\n\n'
        'У разі виникнення проблем, натисніть команду /start',
        reply_markup=main_menu_kb
    )
    await state.finish()


def setup(dp: Dispatcher):
    dp.register_message_handler(non_state_message, state='*')
