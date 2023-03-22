from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.handler import ctx_data
from aiogram.types import Message, CallbackQuery

from app.config import Config
from app.database.services.repos import UserRepo


class IsEmailMethod(BoundFilter):
    async def check(self, *args: ...) -> bool:
        config = Config.from_env()
        return config.misc.auth_method == 'Email'


class IsPhoneMethod(BoundFilter):
    async def check(self, *args: ...) -> bool:
        config = Config.from_env()
        return config.misc.auth_method == 'Phone'
