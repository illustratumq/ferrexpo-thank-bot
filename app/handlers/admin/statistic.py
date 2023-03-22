import os
from datetime import timedelta

import matplotlib.pyplot as plt
from aiogram import Dispatcher
from aiogram.types import Message, InputFile
from matplotlib.axes import Axes

from app.database.models.base import TimedBaseModel
from app.database.services.repos import UserRepo, PointRepo
from app.keyboards import Buttons
from app.keyboards.reply.admin import admin_kb
from app.misc.utils import now


async def statistic(msg: Message, user_db: UserRepo, point_db: PointRepo):
    # try:
    if True:
        this_month_date = now().strftime('%d, %B')
        current_points = await point_db.get_all_points(this_month=True)
        count_scale = sum([point.scale for point in current_points])
        count_transactions = len(current_points)
        image = False
        if current_points:
            fig, ax = plt.subplots(figsize=(10, 5))
            plot_data(current_points, 'Перекази', 'g', 1, ax, fig)
            plt.savefig('statistic.png')
            image = True
        text = (
            f'🗓 Статистика за цей місяць. Сьогодні {this_month_date}\n\n'
            f'Всього перераховано: {count_scale} wellcoin-ів 💚 за {count_transactions} пересилань\n\n'
        )

        if len(current_points) > 3:
            current_points.sort(key=lambda point: point.scale, reverse=True)
            most_big_scale = ', '.join([f'{(await user_db.get_user(point.gifter_id)).full_name} ({point.scale})'
                                       for point in current_points[:3]])
            text += f'<b>Топ 3 найбільших пересилань</b>:\n{most_big_scale}\n\n'

        values = []
        for point in current_points:
            point_values = point.value.split(',')
            for value in point_values:
                if value != '':
                    values.append(value.strip())
        sorted_values = list(set(values))
        sorted_values.sort(key=lambda value: values.count(value), reverse=True)
        most_popular_values = ', '.join([f'{value}' for value in sorted_values])
        text += f'<b>Список цінностей за популярністю</b>:\n{most_popular_values}\n\n'

        points = await point_db.get_all_points()
        points.sort(key=lambda point: point.gifter_id, reverse=True)
        user_ids = [point.gifter_id for point in points]
        sorted_users = list(set(user_ids))
        sorted_users.sort(key=lambda user_id: user_ids.count(user_id), reverse=True)
        the_most_active_users = ', '.join(
            [
                f'{(await user_db.get_user(user_id)).full_name}' for user_id in sorted_users
            ]
        )
        text += f'<b>Найактивніші користувачі</b>:\n{the_most_active_users}\n\n'
        if not image:
            await msg.answer(text, reply_markup=admin_kb)
        else:
            await msg.answer_photo(InputFile('statistic.png'), caption=text, reply_markup=admin_kb)
            os.remove('statistic.png')
    # except:
    #     await msg.answer('Упс, занадто мало даних :(', reply_markup=admin_kb)


def setup(dp: Dispatcher):
    dp.register_message_handler(statistic, text=Buttons.admin.statistic, state='*')


def plot_data(data: list[TimedBaseModel], name: str, color: str, alpha: int, ax: Axes, fig):
    objects = [obj.created_at.strftime('%d.%m.%y') for obj in data]
    dates = [obj.created_at for obj in data]
    dates.sort()
    days = (now() - now().replace(day=dates[0].day, month=dates[0].month, year=dates[0].year)).days + 1
    dates = [(dates[0] + timedelta(days=i)).strftime('%d.%m.%y') for i in range(days)]
    counts = [objects.count(date) for date in dates]
    dates_rng = range(len(dates))
    ax.plot(dates_rng, counts, label=name, color=color)
    ax.scatter(dates_rng, counts, color=color, alpha=0.3)
    ax.fill_between(dates_rng, counts, alpha=alpha/10, color=color)
    ax.legend()
    fig.autofmt_xdate()
    ax.set_xlabel('Дата')
    ax.set_ylabel('Кількість')
    ax.set_title('Кількість переказів у цьому місяці')
    ax.set_yticks([i for i in range(0, max(counts)+1)])
    ax.grid(ls='--', alpha=0.3)
    ax.minorticks_on()
    numeric = len(dates)
    if numeric > 10:
        counter = int(len(dates) / 10) + 1 if isinstance(len(dates) / 10, float) else len(dates) / 10
        dates = over(dates, counter)
        dates_rng = over([i for i in dates_rng], counter)
    plt.xticks(dates_rng, dates)
    return ax


def over(lst: list, n: int):
    new_lst = [lst[0]]
    for i in range(len(lst)):
        if (i + 1) % n == 0:
            new_lst.append(lst[i])
    return new_lst
