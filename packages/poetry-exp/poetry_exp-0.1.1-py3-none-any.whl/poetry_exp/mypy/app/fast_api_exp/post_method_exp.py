from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

"""
When a model attribute has a default value, it is not required.
Otherwise, it is required. To make an attribute optional, you can use None.
"""

app = FastAPI()


@app.post("/items")
async def create_item(item: Item):
    print(f'Creating item: {item}')
    print(f'Item : {item.name} created successfully')
    item_dict = item.dict()
    item_dict['CreatedAt'] = datetime.now()

    return item_dict


@app.post("/items/{item_id}")
async def create_item2(item_id:int, item: Item):
    print(f'Creating item: {item}')
    print(f'Item : {item.name} created successfully')
    item_dict = item.dict()
    item_dict['CreatedAt'] = datetime.now()
    item_dict['id'] = item_id

    return item_dict