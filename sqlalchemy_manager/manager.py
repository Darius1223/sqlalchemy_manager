from typing import Type, TypeVar, Generic, Any

from sqlalchemy import select, Result, CursorResult
from sqlalchemy.orm import sessionmaker

from sqlalchemy_manager.exceptions import (
    FieldNotFoundError,
    RecordDoesNotExistsError,
    TooManyValuesError,
)

ModelType = TypeVar("ModelType")


class QueryBuilder(Generic[ModelType]):
    """Build SQL queries"""

    def __init__(self, model: Type[ModelType], session_maker: sessionmaker):
        self._session_maker = session_maker
        self._model: Type[ModelType] = model

    def get(self, **expression: Any) -> ModelType:
        _filter = set()
        for field, value in expression.items():
            model_field = getattr(self._model, field, None)
            if not model_field:
                raise FieldNotFoundError(
                    f"Field '{field}' not in model '{self._model}'"
                )
            _filter.add(model_field == value)
        statement = select(self.model).where(*_filter)
        with self.session_maker() as session:
            cursor: Result | CursorResult = session.execute(statement)
            result = cursor.fetchall()

            if not result:
                raise RecordDoesNotExistsError("The record was not found")
            elif len(result) > 1:
                raise TooManyValuesError(
                    "The number of returned records is overestimated"
                )
            else:
                return result[0][0]

    def create(self, **expression: Any) -> ModelType:
        item = self.model(**expression)
        with self.session_maker() as session:
            session.add(item)
            session.commit()
            session.refresh(item)
        return item

    @property
    def session_maker(self) -> sessionmaker:
        return self._session_maker

    @property
    def model(self) -> Type[ModelType]:
        return self._model


class Manager:
    """ORM manager [factory for query builder]"""

    def __init__(
        self,
        session_maker: sessionmaker,
        _query_builder_class: Type[QueryBuilder] = QueryBuilder,
    ):
        self._session_maker = session_maker
        self._query_builder_class: Type[QueryBuilder] = _query_builder_class

    @property
    def session_maker(self) -> sessionmaker:
        return self._session_maker

    def __call__(self, model: Type[ModelType]) -> QueryBuilder[ModelType]:
        return self._query_builder_class(model, self.session_maker)
