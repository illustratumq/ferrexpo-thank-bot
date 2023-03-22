import sqlalchemy as sa

from app.database.models.base import TimedBaseModel


class Point(TimedBaseModel):
    point_id = sa.Column(sa.BIGINT, primary_key=True, autoincrement=True)
    user_id = sa.Column(sa.BIGINT, nullable=False)
    gifter_id = sa.Column(sa.BIGINT, nullable=False)
    scale = sa.Column(sa.BIGINT, nullable=False, default=0)
    value = sa.Column(sa.VARCHAR(1000), nullable=True)
    comment = sa.Column(sa.VARCHAR(2000), nullable=True)
