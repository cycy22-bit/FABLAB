from dataclasses import dataclass


@dataclass
class MaterielDTO:
    id: int | None
    label: str
    category: str
    stock_quantity: int
    minimum_stock: int