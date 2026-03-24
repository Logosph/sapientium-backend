from typing import Any, Generic, Protocol, TypeVar

from pydantic import BaseModel
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.results import (
    DeleteResult,
    InsertManyResult,
    InsertOneResult,
    UpdateResult,
)

M = TypeVar("M", bound=BaseModel)


class MongoRepositoryMeta(Protocol):
    db_name: str
    table_name: str
    model: type[BaseModel]


class BaseMongoRepository(Generic[M]):
    class Meta:
        db_name: str = "main"
        table_name: str = ""
        model: type[BaseModel] = BaseModel

    def __init__(self, mongo_client: MongoClient) -> None:
        self.mongo_client = mongo_client

    def get_meta(self) -> MongoRepositoryMeta:
        for cls in self.__class__.__mro__:
            if hasattr(cls, "Meta") and getattr(cls.Meta, "table_name", None):
                return cls.Meta  # type: ignore[no-any-return]
        msg = f"{self.__class__.__name__}.Meta must define table_name"
        raise AttributeError(msg)

    def get_collection(self) -> Collection[dict[str, Any]]:
        meta = self.get_meta()
        return self.mongo_client[meta.db_name][meta.table_name]

    def get_model(self) -> type[BaseModel]:
        return self.get_meta().model

    def select(self, **query: Any) -> list[M]:
        model_cls = self.get_model()
        cursor = self.get_collection().find(query)
        return [model_cls.model_validate(doc) for doc in cursor]  # type: ignore[misc]

    def insert_one(self, doc: M | dict[str, Any]) -> InsertOneResult:
        model_cls = self.get_model()
        if isinstance(doc, model_cls):
            payload = doc.model_dump()
        else:
            payload = doc  # type: ignore[assignment]
        return self.get_collection().insert_one(payload)

    def insert_many(self, docs: list[M] | list[dict[str, Any]]) -> InsertManyResult:
        model_cls = self.get_model()
        payload = [
            doc.model_dump() if isinstance(doc, model_cls) else doc for doc in docs
        ]
        return self.get_collection().insert_many(payload)  # type: ignore[arg-type]

    def update_one(self, query: dict[str, Any], update: dict[str, Any]) -> UpdateResult:
        return self.get_collection().update_one(query, update)

    def update_many(
        self,
        query: dict[str, Any],
        update: dict[str, Any],
    ) -> UpdateResult:
        return self.get_collection().update_many(query, update)

    def delete_one(self, **query: Any) -> DeleteResult:
        return self.get_collection().delete_one(query)

    def delete_many(self, **query: Any) -> DeleteResult:
        return self.get_collection().delete_many(query)
