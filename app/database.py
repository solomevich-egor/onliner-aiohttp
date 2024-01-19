from abc import ABC, abstractmethod
from typing import List

from beanie import init_beanie
from config import settings
from models import Product
from motor.motor_asyncio import AsyncIOMotorClient
from schemas import Product as ProductSchema


class AddProductBase(ABC):
    @abstractmethod
    def add(self, data) -> None:
        pass

    @abstractmethod
    def add_all(self, data) -> None:
        pass


class AddProductMongo(AddProductBase):
    def __init__(self):
        self._mongo_client = AsyncIOMotorClient(
            settings.MONGO_HOST.get_secret_value(),
            int(settings.MONGO_PORT.get_secret_value()),
            username=settings.MONGO_USER.get_secret_value(),
            password=settings.MONGO_PASS.get_secret_value(),
        )

        self.db_product = None

    async def open_connection(self):
        await init_beanie(database=self._mongo_client[settings.MONGO_DB.get_secret_value()], document_models=[Product])

    def close_connection(self):
        self._mongo_client.close()

    async def add(self, item: ProductSchema):
        await Product(
            full_name=item.full_name,
            url=item.url,
            description=item.description,
            price={"min": item.price.min, "max": item.price.max, "currency": item.price.currency},
        ).create()

    async def add_all(self, items: List[ProductSchema]):
        for item in items:
            await Product(
                full_name=item.full_name,
                url=item.url,
                description=item.description,
                price={"min": item.price.min, "max": item.price.max, "currency": item.price.currency},
            ).create()


def addProduct() -> AddProductBase:
    return AddProductMongo()
