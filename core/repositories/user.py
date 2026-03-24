from core.models.user import User
from core.mongo.repository import BaseMongoRepository


class UserRepo(BaseMongoRepository[User]):
    class Meta:
        db_name = "main"
        table_name = "users"
        model = User
