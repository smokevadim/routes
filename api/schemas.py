from typing import Optional, List

from pydantic import BaseModel


class BaseOrmModel(BaseModel):
    class Config:
        orm_mode = True


class User(BaseOrmModel):
    username: str


class Point(BaseOrmModel):
    id: int
    name: str
    coord_x: float
    coord_y: float


class ShortPoint(BaseOrmModel):
    name: str


class AddRoutePoint(BaseOrmModel):
    id: int


class ListPointInRoute(BaseOrmModel):
    point: Point


class AddRoute(BaseOrmModel):
    route_num: int
    user: User
    start: AddRoutePoint
    finish: AddRoutePoint


class Route(BaseOrmModel):
    route_num: int
    user: User
    start: Point
    finish: Point
    points_in_routes: List[ListPointInRoute]


class ShortRoute(BaseOrmModel):
    route_num: int
    start: ShortPoint
    finish: ShortPoint
    distance: int


class PointInRoute(BaseOrmModel):
    point_id: int
    route_id: int
    route: Route


class Distance(BaseOrmModel):
    point_A_id: int
    point_B_id: int
    distance: int


class Token(BaseModel):
    user: str
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class Reports(BaseOrmModel):
    username: str
    routes: List[ShortRoute]
