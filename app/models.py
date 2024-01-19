from uuid import UUID, uuid4

from beanie import Document
from pydantic import BaseModel, Field
from pymongo import IndexModel


class Pricing(BaseModel):
    min: float
    currency: str
    max: float


class Product(Document):
    uuid: UUID = Field(default_factory=uuid4)
    full_name: str | None
    html_url: str | None
    description: str | None
    price: Pricing

    class Settings:
        name = "products"
        indexes = [
            IndexModel("uuid", unique=True),
        ]
