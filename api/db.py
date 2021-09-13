from api.models import SessionLocal


def get_db():
    """DB session generator"""

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
