from threading import Lock

from sqlalchemy.orm import Session

# Dependency
from api.models import SessionLocal


class SingletonMeta(type):
    """Потокобезопасная реализация класса Singleton.

    """
    _instances = {}
    _lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class DB(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self.db: Session = get_db().__next__()
        super().__init__()
