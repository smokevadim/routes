import random
from typing import List

from sqlalchemy import or_, and_

from api import models
from api.db import DB


def generate_route(start: models.Point, finish: models.Point) -> List[models.Point]:
    db = DB().db
    points = [item.id for item in db.query(models.Point).filter(models.Point not in [start, finish]).all()]
    route = []
    for i in range(random.randint(4, 104)):
        route.append(db.get(models.Point, random.choice(points)))
    return route


def calc_distance(a: models.Point, b: models.Point) -> int:
    return random.randint(1, 100)


def get_distance(a: models.Point, b: models.Point) -> int:
    db = DB().db
    distance = db.query(models.Distance).filter(
        or_(
            and_(models.Distance.point_A == a, models.Distance.point_B == b),
            and_(models.Distance.point_A == b, models.Distance.point_B == a)
        )
    ).one_or_none()
    if not distance:
        _dist = calc_distance(a, b)
        distance = models.Distance(
            point_A_id=a.id,
            point_B_id=b.id,
            distance=_dist
        )
        db.add(distance)
        db.commit()
        db.refresh(distance)

    return distance.distance


def calc_route_distance(route: models.Route):
    dist = 0
    a = route.start
    for i, point_in_route in enumerate(route.points_in_routes):
        b = point_in_route
        dist += calc_distance(a, b)
        a = b
    dist += calc_distance(a, route.finish)
    return dist
