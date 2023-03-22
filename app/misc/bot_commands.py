from aiogram import types, Bot
import logging

log = logging.getLogger(__name__)


async def set_default_commands(bot: Bot):
    # await bot.set_my_commands(
    #     [
    #         types.BotCommand('start', '[Ре]Старт боту'),
    #     ]
    # )
    log.info("Установка команд пройшла успішно...")
