import pytest
from sqlalchemy.exc import IntegrityError
from typing_extensions import TypedDict

from sqlalchemy_manager.manager import Manager, TooManyValuesError
from tests.config import session_maker, engine
from tests.models import User, BaseModel


class ModeItems(TypedDict):
    email: str
    first_name: str


@pytest.fixture(autouse=True)
def create_table():
    BaseModel.metadata.drop_all(engine)
    BaseModel.metadata.create_all(engine)


@pytest.fixture
def sql_manager() -> Manager:
    manager = Manager(session_maker=session_maker)
    return manager


@pytest.fixture()
def test_user(create_table, sql_manager) -> User:
    return sql_manager(User).create(email="test@test.ru", first_name="Test")


@pytest.fixture()
def test_user_2(create_table, sql_manager) -> User:
    return sql_manager(User).create(email="test_2@test.ru", first_name="Test")


def test_smoke():
    assert 1 == 1


def test_get_query(sql_manager, test_user):
    user = sql_manager(User).get(email="test@test.ru")
    assert user.id == test_user.id


def test_get_multy_query(sql_manager, test_user, test_user_2):
    with pytest.raises(TooManyValuesError):
        sql_manager(User).get(first_name="Test")


def test_create_query(sql_manager):
    items = ModeItems(email="test@test.ru", first_name="Test")

    user = sql_manager(User).create(**items)

    assert user.email == items["email"]
    assert user.first_name == items["first_name"]

    with pytest.raises(IntegrityError):
        sql_manager(User).create(**items)
