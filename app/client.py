from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import AsyncIterator, Dict, List, Self

import aiohttp
from fake_useragent import UserAgent
from schemas import Pricing, Product
from yarl import URL


class BaseClient(ABC):
    @abstractmethod
    def get_products(self, path) -> List[Product]:
        pass

    @abstractmethod
    def get_product(self, path: str, key: str) -> Product:
        pass


class OnlinerClient(BaseClient):
    def __init__(self, base_url: URL):
        self._base_url = base_url
        self._user = UserAgent().getRandom
        self._client = aiohttp.ClientSession(raise_for_status=True)

    async def close(self) -> None:
        return await self._client.close()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, type, value, traceback) -> None:
        await self._client.close()

    def _make_url(self, path: str) -> URL:
        return self._base_url / path

    async def get_products(self, path: str, params: Dict) -> List[Product]:
        async with self._client.get(url=self._make_url(path), params=params) as resp:
            items = await resp.json()
            products = list()
            for item in items["products"]:
                pricing = Pricing(
                    min=item["prices"]["price_min"]["amount"],
                    max=item["prices"]["price_max"]["amount"],
                    currency=item["prices"]["price_min"]["currency"],
                )
                products.append(
                    Product(
                        full_name=item["full_name"], url=item["url"], description=item["description"], price=pricing
                    )
                )
            return products

    async def get_product(self, path, key) -> Product:
        async with self._client.get(url=self._make_url(f"{path}/{key}")) as resp:
            item = resp.json()
            pricing = Pricing(
                min=item["prices"]["price_min"]["amount"],
                max=item["prices"]["price_max"]["amount"],
                currency=item["prices"]["price_min"]["currency"],
            )
            return Product(full_name=item["full_name"], url=None, description=item["description"], price=pricing)


@dataclass(frozen=True)
class Root:
    base_url: URL

    @asynccontextmanager
    async def client(self) -> AsyncIterator[BaseClient]:
        client = OnlinerClient(self.base_url)
        try:
            yield client
        finally:
            await client.close()
