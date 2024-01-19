import asyncio
import json
from typing import Dict

from client import Root
from database import addProduct
from yarl import URL


async def main(source: Dict) -> None:
    add_product = addProduct()
    await add_product.open_connection()

    for url in source:
        root = Root(URL(url))
        for resource in source[url]:
            async with root.client() as client:
                await add_product.add_all(await client.get_products(path=resource, params=source[url][resource]))

    add_product.close_connection()


if __name__ == "__main__":
    file_url = "onliner.json"
    with open(file_url) as file:
        source = json.load(file)

    asyncio.run(main(source))
