from datetime import timedelta
from typing import List

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from api import schemas, security, models, services
from api.db import get_db
from api.security import ACCESS_TOKEN_EXPIRE_MINUTES
from main import app


@app.post("/token/", response_model=schemas.Token)
async def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = security.authenticate_user(db, form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {
        "user": user.username,
        "access_token": access_token,
        "token_type": "bearer"
    }


@app.get("/points/", response_model=List[schemas.Point])
async def get_points(offset: int = 0, limit: int = 100, current_user: schemas.User = Depends(security.get_current_user),
                     db: Session = Depends(get_db)):
    return db.query(models.Point).slice(offset, limit).all()


@app.get("/routes/", response_model=List[schemas.Route])
async def get_routes(offset: int = 0, limit: int = 100, username: str = None,
                     current_user: schemas.User = Depends(security.get_current_user), db: Session = Depends(get_db)):
    if username:
        routes = db.query(models.Route).join(models.User).filter(models.Route.user_id == models.User.id).filter(
            models.User.username == username).slice(offset, limit).all()
    else:
        routes = db.query(models.Route).slice(offset, limit).all()
    return routes


@app.post("/routes/", response_model=schemas.Route)
async def post_routes(route: schemas.AddRoute, current_user: schemas.User = Depends(security.get_current_user),
                      db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == route.user.username).one()
    start = db.get(models.Point, route.start.id)
    finish = db.get(models.Point, route.finish.id)
    db_route = models.Route(
        route_num=route.route_num,
        user=user,
        start_id=route.start.id,
        finish_id=route.finish.id,
    )
    db.add(db_route)
    db.commit()
    db.refresh(db_route)

    points = services.generate_route(start, finish)
    for point in points:
        point_in_route_db = models.PointInRoute(
            point_id=point.id,
            route=db_route,
        )
        db.add(point_in_route_db)
    db.commit()

    return db_route


@app.get("/reports/", response_model=List[schemas.Reports])
async def get_reports(db: Session = Depends(get_db)):
    return db.query(models.User).all()
