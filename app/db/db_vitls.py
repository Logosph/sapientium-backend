from functools import lru_cache

from pymongo import MongoClient

from core.config import get_settings


@lru_cache
def get_mongo_client() -> MongoClient:
    return MongoClient(get_settings().mongodb_uri)
