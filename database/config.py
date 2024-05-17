from sqlalchemy import URL, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from core import (
    DATABASE_HOST,
    DATABASE_NAME,
    DATABASE_PASSWORD,
    DATABASE_PORT,
    DATABASE_USERNAME,
)

url = URL.create(
    drivername="postgresql+psycopg2",
    username=DATABASE_USERNAME,
    password=DATABASE_PASSWORD,
    host=DATABASE_HOST,
    port=DATABASE_PORT,
    database=DATABASE_NAME,
)

engine = create_engine(url, echo=True)  # pool_size=20

# Base.metadata.create_all(engine) # TODO: handles by alembic

Session = sessionmaker(
    bind=engine, expire_on_commit=False
)  # can be used as context manager
