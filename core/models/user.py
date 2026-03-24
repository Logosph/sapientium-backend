from datetime import datetime

from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    model_config = ConfigDict(extra="ignore")

    email: str
    password_hash: str
    nickname: str
    created: datetime
    last_sign_in: datetime | None = None
