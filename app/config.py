import logging
from dataclasses import dataclass

from environs import Env
from sqlalchemy.engine import URL


@dataclass
class DbConfig:
    host: str
    port: int
    user: str
    password: str
    database: str

    @property
    def sqlalchemy_url(self) -> URL:
        return URL.create(
            'postgresql+asyncpg',
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database
        )


@dataclass
class RedisConfig:
    host: str
    port: int


@dataclass
class TgBot:
    token: str
    name: str
    admin_ids: tuple[int, ...]


@dataclass
class Miscellaneous:
    log_level: int
    user_spreadsheet_id: str
    auth_method: str
    timezone: str


@dataclass
class Config:
    bot: TgBot
    db: DbConfig
    redis: RedisConfig
    misc: Miscellaneous

    @classmethod
    def from_env(cls, path: str = None) -> 'Config':
        env = Env()
        env.read_env(path)

        return Config(
            bot=TgBot(
                token=env.str('BOT_TOKEN'),
                admin_ids=tuple(map(int, env.list('ADMIN_IDS'))),
                name=env.str('BOT_NAME')
            ),
            db=DbConfig(
                host=env.str('DB_HOST', 'localhost'),
                port=env.int('DB_PORT', 5432),
                user=env.str('DB_USER', 'postgres'),
                password=env.str('DB_PASS', 'postgres'),
                database=env.str('DB_NAME', 'postgres'),
            ),
            redis=RedisConfig(
                host=env.str('REDIS_HOST', 'localhost'),
                port=env.int('REDIS_PORT', 6379),
            ),
            misc=Miscellaneous(
                log_level=env.log_level('LOG_LEVEL', logging.INFO),
                user_spreadsheet_id=env.str('USR_SPREADSHEET'),
                timezone=env.str('TIMEZONE'),
                auth_method=env.str('AUTH_METHOD')
            )
        )
