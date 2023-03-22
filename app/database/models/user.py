import sqlalchemy as sa
from sqlalchemy.dialects.mysql import ENUM

from app.database.models.base import TimedBaseModel
from app.database.services.enums import UserStatusEnum


class User(TimedBaseModel):
    user_id = sa.Column(sa.BIGINT, primary_key=True, autoincrement=False, index=True, nullable=True)
    full_name = sa.Column(sa.VARCHAR(300), nullable=False)
    mention = sa.Column(sa.VARCHAR(350), nullable=True)
    auth_data = sa.Column(sa.VARCHAR(100), nullable=True)
    gift_points = sa.Column(sa.BIGINT, nullable=False, default=100)
    status = sa.Column(ENUM(UserStatusEnum), default=UserStatusEnum.UNAUTHORIZED, nullable=False)
