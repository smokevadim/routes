from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, Float, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy_utils import database_exists, create_database

from settings import SQLALCHEMY_DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_size=10, max_overflow=20)
if not database_exists(engine.url):
    create_database(engine.url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)


class Point(Base):
    __tablename__ = 'points'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    coord_x = Column(Float(6), nullable=False)
    coord_y = Column(Float(6), nullable=False)


class Route(Base):
    __tablename__ = 'routes'
    route_num = Column(Integer, primary_key=True, index=True)
    user_id = Column('User', ForeignKey('users.id'), nullable=False)
    user = relationship('User', backref='routes')
    start_id = Column('Start', ForeignKey('points.id'), nullable=False)
    start = relationship('Point', foreign_keys='Point.id', primaryjoin='Route.start_id == Point.id', uselist=False)
    finish_id = Column('Finish', ForeignKey('points.id'), nullable=False)
    finish = relationship('Point', foreign_keys='Point.id', primaryjoin='Route.finish_id == Point.id', uselist=False)

    @hybrid_property
    def distance(self):
        from api import services
        return services.calc_route_distance(self)


class PointInRoute(Base):
    __tablename__ = 'points_in_routes'
    id = Column(Integer, primary_key=True, index=True)
    point_id = Column('Point', ForeignKey('points.id', ondelete='CASCADE'), nullable=False, index=True)
    point = relationship('Point', backref='points_in_routes')
    route_id = Column('Route', ForeignKey('routes.route_num', ondelete='CASCADE'), nullable=False, index=True)
    route = relationship('Route', backref='points_in_routes')


class Distance(Base):
    __tablename__ = 'distances'
    id = Column(Integer, primary_key=True, index=True)
    point_A_id = Column(Integer, ForeignKey('points.id', ondelete='CASCADE'), nullable=False, index=True)
    point_A = relationship('Point', foreign_keys=[point_A_id])
    point_B_id = Column(Integer, ForeignKey('points.id', ondelete='CASCADE'), nullable=False, index=True)
    point_B = relationship('Point', foreign_keys=[point_B_id])
    distance = Column(Integer)


Base.metadata.create_all(bind=engine)


@event.listens_for(PointInRoute, "after_insert")
def calc_distances_in_route(mapper, connection, target: PointInRoute):
    """Catch-signal to generate route between start point and finish point"""

    from api.services import get_distance
    from api.db import get_db
    db = get_db().__next__()
    points = target.route.points_in_routes
    last_point = None
    if points:
        last_point = db.get(Point, points[-1].point_id)
    a = last_point if last_point else target.route.start

    b = target.point or db.get(Point, target.point_id)
    c = target.route.finish

    get_distance(a, b)
    get_distance(b, c)
