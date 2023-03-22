from datetime import datetime

import pytz

from app.config import Config


def now():
    config = Config.from_env()
    return datetime.now().replace(microsecond=0).astimezone(pytz.timezone(config.misc.timezone))


def localize(date: datetime):
    config = Config.from_env()
    return date.astimezone(pytz.timezone(config.misc.timezone))

