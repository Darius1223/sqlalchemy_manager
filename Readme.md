# SqlAlchemy Manager [by django style]

---

## Quick start

Simple database structure
```python
Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)


class User(BaseModel):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True)
    first_name = Column(String)

```

First of all, you need to create a `Manager` object

```python
import os

from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy_manager import Manager

database_url = os.getenv("DATABASE_URL", default="sqlite:///db")

engine = create_engine(
    url=database_url,
    echo=True,
)
session_maker = sessionmaker(engine)
manager = Manager(session_maker=session_maker)

```

Basic usage
```python
user = manager(User).create(email="test@test.ru")
user = manager(User).get(email="test_2@test.ru")
```