# SqlAlchemy Manager [by django style]

<p align="center">
<a href="https://github.com/Darius1223/sqlalchemy_manager/actions?query=workflow%3ATest+event%3Apush+branch%3Amaster" target="_blank">
    <img src="https://github.com/Darius1223/sqlalchemy_manager/workflows/Test/badge.svg?event=push&branch=master" alt="Test">
</a>
<a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/tiangolo/fastapi" target="_blank">
    <img src="https://coverage-badge.samuelcolvin.workers.dev/tiangolo/fastapi.svg" alt="Coverage">
</a>
<a href="https://pypi.org/project/sqlalchemy-django-manager/" target="_blank">
    <img src="https://img.shields.io/pypi/v/sqlalchemy-django-manager?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/sqlalchemy-django-manager/" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/sqlalchemy-django-manager.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>

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