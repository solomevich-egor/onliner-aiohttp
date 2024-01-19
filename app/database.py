from abc import ABC, abstractmethod
from typing import List, Self

from beanie import init_beanie
from config import settings
from models import Product
from motor.motor_asyncio import AsyncIOMotorClient
from schemas import Product as ProductSchema


class MongoDbConnector:
    def __init__(self):
        self._client = AsyncIOMotorClient(
            settings.MONGO_HOST.get_secret_value(),
            int(settings.MONGO_PORT.get_secret_value()),
            username=settings.MONGO_USER.get_secret_value(),
            password=settings.MONGO_PASS.get_secret_value(),
        )

    async def __aenter__(self) -> Self:
        if self._client is None:
            raise Exception("Databased connector is not initialized")

        await init_beanie(database=self._client[settings.MONGO_DB.get_secret_value()], document_models=[Product])
        return self

    async def __aexit__(self, type, value, traceback):
        self._client.close()


class AddProductBase(ABC):
    @abstractmethod
    def add(self, data: ProductSchema) -> None:
        pass

    @abstractmethod
    def add_all(self, data: List[ProductSchema]) -> None:
        pass


class AddProductMongo(AddProductBase):
    @staticmethod
    async def add(item: ProductSchema) -> None:
        async with MongoDbConnector():
            await Product(
                full_name=item.full_name,
                html_url=item.url,
                description=item.description,
                price={"min": item.price.min, "max": item.price.max, "currency": item.price.currency},
            ).create()

    @staticmethod
    async def add_all(items: List[ProductSchema]) -> None:
        async with MongoDbConnector():
            for item in items:
                await Product(
                    full_name=item.full_name,
                    html_url=item.url,
                    description=item.description,
                    price={"min": item.price.min, "max": item.price.max, "currency": item.price.currency},
                ).create()


def addProduct() -> AddProductBase:
    return AddProductMongo()
