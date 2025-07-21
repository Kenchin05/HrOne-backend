from . import crud
from fastapi import APIRouter, Body, status, HTTPException
from fastapi.responses import JSONResponse
from typing import List, Optional
from .models import ProductCreate, ProductResponse, OrderCreate, OrderResponse
from .database import str_object_id
from .models import OrderCreate, OrderResponse, PaginatedOrderResponse
router = APIRouter()

#  Products API 

@router.post("/products", status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate = Body(...)):
    # ... (your existing product creation code)
    new_product = await crud.add_product(product)
    if new_product:
        return {"id": str_object_id(new_product["_id"])}
    raise HTTPException(status_code=400, detail="Product could not be created.")

#  Orders API 

@router.post("/orders", status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderCreate = Body(...)):
    new_order = await crud.add_order(order)
    if new_order:
        return {"id": str_object_id(new_order["_id"])}
    raise HTTPException(status_code=400, detail="Order could not be created.")

# list products
@router.get("/products")
async def list_products(
    name: Optional[str] = None,
    size: Optional[str] = None,
    limit: int = 10,
    offset: int = 0
):
    products, total_count = await crud.retrieve_products(name, size, limit, offset)
    formatted_products = [
        {"id": str_object_id(p["_id"]), "name": p["name"], "price": p["price"]}
        for p in products
    ]
    response_data = {
        "data": formatted_products,
        "page": {
            "limit": len(formatted_products),
            "next": (offset + limit) if (offset + limit) < total_count else None,
            "previous": (offset - limit) if (offset - limit) >= 0 else None
        }
    }
    return JSONResponse(status_code=status.HTTP_200_OK, content=response_data)



# list orders for a given user_id
@router.get("/orders/{user_id}")
async def list_orders_for_user(user_id: str, limit: int = 10, offset: int = 0):
    # Removed the `response_model` from the decorator
    orders, total_count = await crud.retrieve_orders_by_user(user_id, limit, offset)
    
    next_page_offset = offset + limit
    prev_page_offset = offset - limit

    # The new `retrieve_orders_by_user` already formats the data,
    # so we just need to structure the final response.
    response_data = {
        "data": orders,
        "page": {
            "limit": len(orders),
            "next": next_page_offset if next_page_offset < total_count else None,
            "previous": prev_page_offset if prev_page_offset >= 0 else None
        }
    }
    # Return a JSONResponse directly.
    return JSONResponse(status_code=status.HTTP_200_OK, content=response_data)