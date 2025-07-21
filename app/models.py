from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from bson import ObjectId




#  Product Models 
class Size(BaseModel):
    size: str
    quantity: int

class ProductCreate(BaseModel):
    name: str
    price: float
    sizes: List[Size]

class ProductResponse(BaseModel):
    id: str
    name: str
    price: float



#  Order Models 
class OrderItem(BaseModel):
    productId: str
    qty: int

class OrderCreate(BaseModel):
    userId: str
    items: List[OrderItem]

class ProductDetails(BaseModel):
    id: str
    name: str   

class OrderItemDetails(BaseModel):
    productDetails: ProductDetails
    qty: int

class OrderResponse(BaseModel):
    id: str
    items: List[OrderItemDetails]
    total: float
    


class PageInfo(BaseModel):
    limit: int
    next: Optional[int]
    previous: Optional[int]

class PaginatedOrderResponse(BaseModel):
    data: List[OrderResponse]
    page: PageInfo