from typing import Optional

from pydantic import BaseModel


class Pricing(BaseModel):
    min: Optional[float] = None
    max: Optional[float] = None
    currency: Optional[str] = None


class Product(BaseModel):
    full_name: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None
    price: Pricing
