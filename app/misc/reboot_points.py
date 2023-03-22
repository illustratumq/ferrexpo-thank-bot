import logging
import time

from aiogram import Bot
from apscheduler_di import ContextSchedulerDecorator
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from app.config import Config
from app.database.googlesheet.sheets_api import GoogleSheet
from app.database.services.repos import UserRepo, PointRepo
from app.keyboards.reply.menu import to_auth
from app.misc.utils import localize, now

log = logging.getLogger(__name__)


async def set_jobs(scheduler: ContextSchedulerDecorator):
    log.info('Scheduler функції встановлено')
    scheduler.add_job(reboot_points, trigger='cron', day=1, hour=9, minute=0)
    scheduler.add_job(last_day_point, trigger='cron', day='last', hour=13, minute=0)


async def last_day_point(bot: Bot, session: sessionmaker, config: Config):
    user_db = UserRepo(session())
    text = (
        'Друзі, дякуємо всім за участь та розвиток власної навички бути вдячною людиною💚\n'
        'Вже кінець місяця, і це означає що:\n'
        '1 - завтра ти отримаєш нову порцію wellcoin-ів 🎉\n'
        '2  - а ті wellcoin-и, які є в тебе зараз - зникнуть 😱 Хуткіше подаруй їх тим, хто це заслуговує!💚\n'
    )
    for user in await user_db.get_all():
        try:
            await bot.send_message(user.user_id, text=text)
        except:
            for admin_id in config.bot.admin_ids:
                await bot.send_message(admin_id, text=f'Користувач {user.full_name} заблокував бота')


async def reboot_points(bot: Bot, session: sessionmaker, config: Config):
    user_db = UserRepo(session())
    for user in await user_db.get_all():
        text = (
            '<b>Тобі нараховано 100 wellcoin-ів 🎉 💚</b>\n\n'
            'Переходь у розділ "Віддати подяку" та ділись з колегами частинкою доброти 💚'
        )
        await user_db.update_user(user.user_id, gift_points=100)
        try:
            await bot.send_message(user.user_id, text=text)
        except:
            for admin_id in config.bot.admin_ids:
                await bot.send_message(admin_id, text=f'Користувач {user.full_name} заблокував бота')


async def check_auth(session, bot: Bot, config: Config, google_sheet: GoogleSheet):
    session: AsyncSession = session()
    user_db = UserRepo(session)
    users = await user_db.get_all()
    users_sheet = google_sheet.get_auth_data(config.misc.user_spreadsheet_id)
    names = [name for email, name in users_sheet]
    for user in users:
        if user.full_name not in names:
            try:
                await bot.send_message(user.user_id, 'Упс, я виявив, що ти не пройшов авторизацію до кінця. '
                                                     'Давай виправим це!',
                                       reply_markup=to_auth)
                for admin in config.bot.admin_ids:
                    await bot.send_message(admin, text=f'Користувач {user.mention} ({user.user_id})'
                                                       f' не пройшов реєстрацію')
            except:
                pass
    await session.commit()
    await session.close()


async def recreate_events(bot: Bot, session: sessionmaker, config: Config):
    point_db = PointRepo(session)
    user_db = UserRepo(session)
    cell_points = GoogleSheet().read_cells(config.misc.user_spreadsheet_id, 'Events!A2:G')
    cell_points = [[cell_point[i] for i in [0, 3, 4, 5, 6]] for cell_point in cell_points]
    count = 0
    log.info(cell_points[12])
    for point in await point_db.get_all():
        gifter = await user_db.get_user(point.gifter_id)
        user = await user_db.get_user(point.user_id)
        if localize(point.created_at) > now().replace(day=1, month=2):
            data = localize(point.created_at).strftime('%d %B %y')
            point_list = [
                'Переказ балів', str(point.scale), data, point.value, point.comment
            ]
            log.info(point_list)
            if point_list not in cell_points:
                count += 1
                GoogleSheet().write_event(
                    spreadsheet_id=config.misc.user_spreadsheet_id,
                    action='Переказ балів',
                    sender_name=gifter.full_name,
                    getter_name=user.full_name,
                    points=point.scale,
                    val=point.value, message=point.comment
                )
            time.sleep(1)
    for admin_id in config.bot.admin_ids:
        await bot.send_message(admin_id, f'В таблицю додано {count} переказів, що не зберіглися')

