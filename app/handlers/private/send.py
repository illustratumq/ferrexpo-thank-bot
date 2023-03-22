from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from app.config import Config
from app.database.googlesheet.sheets_api import GoogleSheet
from app.database.services.repos import UserRepo
from app.keyboards.inline.authorization import auth_kb
from app.keyboards.reply.menu import main_menu_kb
from app.keyboards.reply.send import *
from app.states.states import SendSG


def is_number(msg: Message):
    return str(msg.text).isnumeric()


async def send_points(msg: Message, state: FSMContext, user_db: UserRepo):
    user = await user_db.get_user(msg.from_user.id)
    if user.gift_points == 0:
        await msg.answer('Ти вже використав 100/100 wellcoin-ів 💚 за цей місяць. Дочекайся настпуного поповнення!',
                         reply_markup=main_menu_kb)
        return
    text = (
        'Круто! Сьогодні ти зробиш когось щасливим!\nДякуємо тобі 💚\n\n'
        'Щоб почати, натисни на кнопку <b>"Список колег"</b>'
    )
    await msg.answer(text, reply_markup=send_kb)
    await state.update_data(gefter_id=msg.from_user.id)


async def select_command(msg: Message, google_sheet: GoogleSheet, config: Config):
    commands = google_sheet.get_commands(config.misc.user_spreadsheet_id)
    await msg.answer('Обери команду колег', reply_markup=select_user_commands(commands))
    await msg.answer('Ти також можеж знайти колегу <b>за його ім\'ям</b> використавши пошук',
                     reply_markup=auth_kb('Email'))
    await SendSG.Command.set()


async def select_user(msg: Message, user_db: UserRepo, google_sheet: GoogleSheet, config: Config):
    users = await user_db.get_authorized_user()
    users.remove(await user_db.get_user(msg.from_user.id))
    exist_users = []
    for user in users:
        google_sheet_user = google_sheet.get_user(config.misc.user_spreadsheet_id, user.auth_data)
        if google_sheet_user and google_sheet_user[-1] in msg.text:
            exist_users.append(user)
    await msg.answer('Вибери зі списку того, кому ти хочеш направили wellcoin-и 💚',
                     reply_markup=await select_user_kb(exist_users))
    await SendSG.User.set()


async def save_user(msg: Message, state: FSMContext, user_db: UserRepo):
    user = await user_db.get_user_by_name(msg.text)
    if user is None:
        await msg.answer('Упс... Не знайшов такого користувача, скористайся кнопкою "Список колег",'
                         ' або настисни "Пошук 🔍"')
        return
    await state.update_data(name=msg.text)
    text = (
        'Напиши свої теплі слова вдячності тут. Спробуй подарувати свою вдячність від серця ❤'
    )
    await msg.answer(text, reply_markup=main_menu_kb)
    await SendSG.Message.set()


async def save_message(msg: Message, state: FSMContext, user_db: UserRepo):
    await state.update_data(message=msg.text)
    user = await user_db.get_user(msg.from_user.id)
    await msg.answer(f'Скільки wellcoin-ів ти бажаєш відправити? В тебе є {user.gift_points} 👇')
    await SendSG.Points.set()


async def save_points(msg: Message, user_db: UserRepo, state: FSMContext):
    user = await user_db.get_user(msg.from_user.id)
    if not is_number(msg):
        return await msg.answer('Не схоже на число.. Спробуйте ще раз!')
    elif int(msg.text) > user.gift_points:
        return await msg.answer(f'Занадто багато.. Ти маєш лише {user.gift_points}')
    elif int(msg.text) == 0:
        return await msg.answer('Занадто мало... Спробуй ще раз!')
    await state.update_data(points=int(msg.text))
    text = (
        f'Чудово, зафіксовано передачу {msg.text} wellcoin-ів ✅.\n\n'
        f'Вкажи за яку саме цінність ти вдячна/-ний? '
        f'Це може бути одна або декілька цінностей Компанії або твоя власна.\n\n' 
        f'Натисни на цінності із списку, які хочеш обрати а потім натисни "✅Відправити wellcoin-и"'
    )
    await msg.answer(text=text, reply_markup=values_kb())
    await state.update_data(value='')
    await SendSG.Value.set()


async def input_values(msg: Message, state: FSMContext):
    data = await state.get_data()
    value = data['value']
    if value == '':
        values = [msg.text]
    else:
        value.append(msg.text)
        values = value
    values_str = ', '.join(values)
    await state.update_data(value=values)
    await msg.answer(f'Обрані цінності: {values_str}', reply_markup=values_kb(next_button=True, added_values=values))


async def input_custom_value(msg: Message):
    await msg.answer('Вкажи, будь ласка, що це?')
    await SendSG.CustomValue.set()


async def confirm(msg: Message):
    await msg.answer('Все готово, відправити wellcoin-и?', reply_markup=confirm_send_kb)
    await SendSG.Confirm.set()


async def send(msg: Message, user_db: UserRepo, point_db: PointRepo,
               state: FSMContext, config: Config, google_sheet: GoogleSheet):
    state_data = await state.get_data()
    name = state_data['name']
    points = int(state_data['points'])
    message = state_data['message']
    value = state_data['value']
    gifter = await user_db.get_user(msg.from_user.id)
    user = await user_db.get_user_by_name(name)
    await point_db.add(
        user_id=user.user_id, gifter_id=gifter.user_id,
        scale=points, value=', '.join(value), comment=message
    )
    remain_points = gifter.gift_points - points
    await user_db.update_user(gifter.user_id, gift_points=remain_points)
    answer_text = (
        f'✉ Wellcoin-и відправлено! '
    )
    if remain_points == 0:
        answer_text += 'В цьому місяці ти використав всі 100 wellcoin-ів'
        await msg.answer(answer_text, reply_markup=main_menu_kb)
    else:
        answer_text = f'В цьому місяці в тебе є ще {remain_points} wellcoin-ів, якими ти можеш поділитися!'
        await msg.answer(answer_text, reply_markup=send_kb)
    user_msg = (
        f'👉💚 Переказ {points} wellcoin-ів\n\n'
        f'Вітаємо! Тобі подарували подяку від {gifter.full_name} '
        f'за цінність: <b>{value}</b>💐\n\n<i>{message}</i>'
    )
    await msg.bot.send_message(user.user_id, text=user_msg)
    await state.finish()
    await send_points(msg, state, user_db)
    await state.update_data(gefter_id=msg.from_user.id)
    google_sheet.write_event(
        spreadsheet_id=config.misc.user_spreadsheet_id,
        action='Переказ балів',
        sender_name=gifter.full_name,
        getter_name=user.full_name,
        points=points,
        val=value, message=message, sheet_name='Send'
    )


def setup(dp: Dispatcher):
    dp.register_message_handler(send_points, text=Buttons.menu.send_points, state='*')
    dp.register_message_handler(select_command, text=Buttons.send.select_user, state='*')
    dp.register_message_handler(select_user, state=SendSG.Command)
    dp.register_message_handler(save_user, state=SendSG.User)
    dp.register_message_handler(save_message, state=SendSG.Message)
    dp.register_message_handler(save_points, state=SendSG.Points)
    dp.register_message_handler(input_custom_value, state=[SendSG.Value, SendSG.CustomValue],
                                text=Buttons.send.custom_value)
    dp.register_message_handler(confirm, state=[SendSG.Value, SendSG.CustomValue], text=Buttons.send.next_button)
    dp.register_message_handler(input_values, state=[SendSG.Value, SendSG.CustomValue])
    dp.register_message_handler(send, state=SendSG.Confirm)

