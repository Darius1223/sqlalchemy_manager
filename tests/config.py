import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

database_url = os.getenv("DATABASE_URL", default="sqlite:///db")
engine = create_engine(
    url=database_url,
    echo=True,
)
session_maker = sessionmaker(engine)
