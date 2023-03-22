import logging

from aiogram import Bot

log = logging.getLogger(__name__)


async def notify(bot: Bot, admin_ids: tuple[int, ...], reply_markup=None) -> None:
    for admin in admin_ids:
        try:
            await bot.send_message(admin, 'Бот запущен', reply_markup=reply_markup)
        except Exception as err:
            log.exception(err)
