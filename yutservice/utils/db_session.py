from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from yutservice.models.dbmodels import Base
from yutservice.config import CONFIG


engine = create_engine(
    CONFIG["POSTGRES_DATABASE_URL"],
    # connect_args={"check_same_thread": False},
)
LocalSession = sessionmaker(bind=engine)


def get_db() -> Session:
    """Dependency injection."""
    db = LocalSession()
    try:
        yield db
        db.commit()
    finally:
        db.close()


def DB_init():
    Base.metadata.create_all(engine)
