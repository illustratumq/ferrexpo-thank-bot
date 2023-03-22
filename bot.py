import asyncio
import logging

import betterlogging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.types import ParseMode, AllowedUpdates

from app import middlewares, filters, handlers
from app.config import Config
from app.database.googlesheet.sheets_api import GoogleSheet
from app.database.services.db_engine import create_db_engine_and_session_pool
from app.misc.bot_commands import set_default_commands
from app.misc.notify_admins import notify
from app.misc.reboot_points import set_jobs
from app.misc.scheduler import compose_scheduler

log = logging.getLogger(__name__)


async def main():
    config = Config.from_env()
    betterlogging.basic_colorized_config(level=config.misc.log_level)
    log.info('Запускаюсь...')

    storage = RedisStorage2(host=config.redis.host, port=config.redis.port)
    bot = Bot(config.bot.token, parse_mode=ParseMode.HTML)
    dp = Dispatcher(bot, storage=storage)
    db_engine, sqlalchemy_session_pool = await create_db_engine_and_session_pool(config.db.sqlalchemy_url,
                                                                                 config.misc.log_level)

    allowed_updates = (
            AllowedUpdates.MESSAGE + AllowedUpdates.CALLBACK_QUERY +
            AllowedUpdates.EDITED_MESSAGE + AllowedUpdates.INLINE_QUERY
    )

    scheduler = compose_scheduler(config, bot, sqlalchemy_session_pool)
    environments = dict(config=config, dp=dp, google_sheet=GoogleSheet.env(), scheduler=scheduler)
    middlewares.setup(dp, environments, sqlalchemy_session_pool)

    filters.setup(dp)
    handlers.setup(dp)

    await set_default_commands(bot)
    await notify(bot, config.bot.admin_ids)
    await set_jobs(scheduler)
    log.info('Бот запущений!')


    try:
        scheduler.start()
        await dp.skip_updates()
        await dp.start_polling(allowed_updates=allowed_updates, reset_webhook=True)
    finally:
        await storage.close()
        await storage.wait_closed()
        await (await bot.get_session()).close()
        await db_engine.dispose()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        log.warning('Бот зупинено!')
