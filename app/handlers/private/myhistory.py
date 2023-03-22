from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram.utils.callback_data import CallbackData

from app.database.services.repos import PointRepo, UserRepo
from babel.dates import format_datetime

from app.keyboards import Buttons
from app.keyboards.inline.history import history_kb, history_cb
from app.keyboards.reply.menu import main_menu_kb, pre_history_kb, back_to_history_kb


async def history_type(msg: Message, state: FSMContext):
    try:
        data = await state.get_data()
        last_msg_id = data['last_msg_id']
        await msg.bot.delete_message(msg.from_user.id, last_msg_id)
    except:
        pass
    await msg.answer('Подивись історію своїх переказів або переказів для тебе', reply_markup=pre_history_kb)


async def my_history_pre(msg: Message, point_db: PointRepo, user_db: UserRepo,
                         state: FSMContext):
    await state.finish()
    points_i_send = await point_db.get_gifter_points(msg.from_user.id)
    points_to_me = await point_db.get_user_points(msg.from_user.id)
    if msg.text == Buttons.menu.to_me_send:
        if len(points_to_me) == 0:
            await msg.answer('Тобі ще не надіслали wellcoin-ів 😥', reply_markup=main_menu_kb)
            return
    else:
        if len(points_i_send) == 0:
            await msg.answer('Ти ще не робив переказів 😥', reply_markup=main_menu_kb)
            return
    await msg.answer(f'Ви зробили {len(points_i_send)} та отримали {len(points_to_me)} переказів  💚 за весь час',
                     reply_markup=back_to_history_kb)
    await my_history(msg, {}, point_db, user_db, state, to_me=msg.text == Buttons.menu.to_me_send)


async def my_history(upd: Message | CallbackData, callback_data: dict, point_db: PointRepo, user_db: UserRepo,
                     state: FSMContext, to_me: bool = False):
        chat_id = upd.from_user.id
        msg = upd if isinstance(upd, Message) else upd.message
        data = await state.get_data()
        if not data:
            if to_me:
                points = await point_db.get_user_points(upd.from_user.id)
            else:
                points = await point_db.get_gifter_points(upd.from_user.id)
            point_ids = [point.point_id for point in points]
            await state.update_data(points=point_ids[::-1], current_point=point_ids[0], to_me=to_me)
        data = await state.get_data()
        to_me = data['to_me']
        points = data['points']
        current_point = data['current_point']
        current_index = points.index(current_point)

        action = callback_data.get('action')
        if action == 'close':
            await msg.delete_reply_markup()
            await state.finish()
            return
        elif action == 'next':
            if len(points) == 1:
                await upd.answer('Більше немає переказів')
                return
            elif current_index == len(points) - 1:
                current_point = points[0]
            else:
                current_point = points[current_index+1]
        elif action == 'prev':
            if len(points) == 1:
                await upd.answer('Більше немає переказів')
                return
            elif current_index == 0:
                current_point = points[-1]
            else:
                current_point = points[current_index-1]
        else:
            current_point = points[0]

        await state.update_data(current_point=current_point)
        point = await point_db.get_point(int(current_point))
        user_id = point.gifter_id if to_me else point.user_id
        receiver = await user_db.get_user(user_id)
        dates = format_datetime(point.created_at, locale='uk_UA')

        current_index = points.index(current_point)
        title = 'Історія переказів для тебе' if to_me else 'Моя історія переказів'
        from_user = 'від' if to_me else 'для'
        text = (
            f'📌 {title} ({current_index + 1}/{len(points)})\n\n'
            f'💚 Переказ {point.scale} wellcoin-iв, {from_user} {receiver.full_name}\n'
            f'📅 <b>Дата</b>: {dates}\n\n'
            f'<b>Цінності</b>: <i>{point.value}</i>\n\n'
            f'<b>Коментар</b>: <i>{point.comment}</i>'
        )
        if 'last_msg_id' not in list(data.keys()):
            last_msg = await msg.answer(text, reply_markup=history_kb())
        else:
            last_msg_id = data['last_msg_id']
            last_msg = await msg.bot.edit_message_text(text, chat_id, last_msg_id, reply_markup=history_kb())
        await state.update_data(last_msg_id=last_msg.message_id)


def setup(dp: Dispatcher):
    dp.register_message_handler(history_type, text=[Buttons.menu.history, Buttons.menu.back_to_history],
                                state='*')
    dp.register_message_handler(my_history_pre, text=[Buttons.menu.my_send, Buttons.menu.to_me_send], state='*')
    dp.register_callback_query_handler(my_history, history_cb.filter(), state='*')