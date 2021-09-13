"""
This file generate fixtures in DB.
"""

import random
import warnings

import numpy as np

from api import models
from api.db import get_db

warnings.simplefilter("ignore")


def add_users():
    db = get_db().__next__()
    for i in range(3):
        db_user = models.User(username=f'user{i + 1}')
        db.add(db_user)
    db.commit()


def add_points():
    arr = np.random.rand(1_000_000, 2) * 180
    i = 1
    db = get_db().__next__()
    for x, y in arr:
        db_point = models.Point(
            name=f'point_{i}',
            coord_x=float("{0:.6f}".format(x)),
            coord_y=float("{0:.6f}".format(y)),
        )
        db.add(db_point)
        i += 1
    db.commit()
    db.re


def add_routes():
    db = get_db().__next__()
    users = db.query(models.User).all()
    points = db.query(models.Point).all()
    for i in range(10):
        db_route = models.Route(
            route_num=i,
            user_id=random.choice(users).id,
            start_id=random.choice(points).id,
            finish_id=random.choice(points).id,
        )
        db.add(db_route)
        db.commit()


def add_points_in_routes():
    db = get_db().__next__()
    routes = db.query(models.Route).all()
    routes = db.query(models.Route).all()
    points_count = db.query(models.Point).count()
    for route in routes:
        for i in range(random.randint(1, 100)):
            db_point_in_route = models.PointInRoute(route=route,
                                                    point=db.get(models.Point, random.randint(1, points_count)))
            db.add(db_point_in_route)
        db.commit()


def try_add(f, *args, **kwargs):
    try:
        print('Adding fixtures ', f.__name__)
        f(*args, **kwargs)
    except Exception as e:
        get_db().db.rollback()


if __name__ == '__main__':
    try_add(add_users)
    try_add(add_points)
    try_add(add_routes)
    try_add(add_points_in_routes)
