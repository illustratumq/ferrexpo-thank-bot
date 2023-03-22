from app.database.models.point import Point
from app.database.models.user import User
from app.database.services.db_ctx import BaseRepo
from app.database.services.enums import UserStatusEnum
from app.misc.utils import now


class UserRepo(BaseRepo[User]):
    model = User

    async def get_user(self, user_id: int) -> User:
        return await self.get_one(self.model.user_id == user_id)

    async def get_authorized_user(self):
        return await self.get_all(self.model.status == UserStatusEnum.AUTHORIZED)

    async def get_user_by_auth_data(self, auth_data: str) -> User:
        return await self.get_one(self.model.auth_data == auth_data)

    async def get_user_by_name(self, name: str) -> User:
        return await self.get_one(self.model.full_name == name)

    async def update_user(self, user_id: int, **kwargs) -> None:
        return await self.update(self.model.user_id == user_id, **kwargs)

    async def delete_user(self, user_id: int):
        await self.delete(self.model.user_id == user_id)


class PointRepo(BaseRepo[Point]):
    model = Point

    async def get_point(self, point_id: int) -> Point:
        return await self.get_one(self.model.point_id == point_id)

    async def update_point(self, point_id: int, **kwargs) -> None:
        return await self.update(self.model.point_id == point_id, **kwargs)

    async def delete_point(self, point_id: int):
        await self.delete(self.model.point_id == point_id)

    async def get_all_points(self, *clauses, this_month: bool = True) -> list[Point]:
        points = await self.get_all(*clauses)
        if this_month:
            for point in points:
                if point.created_at.strftime('%Y:%m') != now().strftime('%Y:%m'):
                    points.remove(point)
        return points

    async def get_user_points(self, user_id: int, count: bool = False,
                              this_month: bool = False) -> list[Point] | int:
        points = await self.get_all(self.model.user_id == user_id)
        if this_month:
            this_month_points = []
            for point in points:
                if point.created_at.month == now().month and point.created_at.year == now().year:
                    this_month_points.append(point)
            points = this_month_points
        if count:
            points_sum = sum([point.scale for point in points])
            return 1 if points_sum == 0 else points_sum
        else:
            return points

    async def get_gifter_points(self, user_id: int):
        return await self.get_all(self.model.gifter_id == user_id)
