from pydantic import BaseModel


class Pricing(BaseModel):
    min: float | None
    max: float | None
    currency: str | None


class Product(BaseModel):
    full_name: str | None
    url: str | None
    description: str | None
    price: Pricing
