from bson.objectid import ObjectId
from .database import product_collection, order_collection
from .models import ProductCreate, OrderCreate

#  Product CRUD Operations 

async def add_product(product_data: ProductCreate) -> dict:
    """
    Adds a new product to the database.
    """
    product = product_data.model_dump()
    result = await product_collection.insert_one(product)
    new_product = await product_collection.find_one({"_id": result.inserted_id})
    return new_product

async def retrieve_products(name: str | None, size: str | None, limit: int, offset: int) -> tuple[list[dict], int]:
    """
    Retrieves a list of products with filtering and pagination.
    """
    query = {}
    if name:
        query["name"] = {"$regex": name, "$options": "i"} # Case-insensitive partial search
    if size:
        query["sizes.size"] = size # Filter by size in the nested array

    total_products_count = await product_collection.count_documents(query)
    products_cursor = product_collection.find(query, {"sizes": 0}).skip(offset).limit(limit) # Exclude sizes field
    products = await products_cursor.to_list(length=limit)
    return products, total_products_count


#  Order CRUD Operations 

async def add_order(order_data: OrderCreate) -> dict:
    """
    Adds a new order to the database.
    """
    order = order_data.model_dump()
    # Convert productIds from string to ObjectId for the lookup
    for item in order['items']:
        item['productId'] = ObjectId(item['productId'])
        
    result = await order_collection.insert_one(order)
    new_order = await order_collection.find_one({"_id": result.inserted_id})
    return new_order

async def retrieve_orders_by_user(user_id: str, limit: int, offset: int) -> tuple[list[dict], int]:
    """
    Retrieves a user's orders by fetching orders first, then fetching product
    details for each item in a loop.
    """
    # First, get the total count for pagination
    total_orders_count = await order_collection.count_documents({"userId": user_id})

    # Fetch the batch of orders for the current page
    orders_cursor = order_collection.find({"userId": user_id}).skip(offset).limit(limit)
    
    orders_list = await orders_cursor.to_list(length=limit)
    
    # This will hold the final, formatted list of orders
    formatted_orders = []

    for order in orders_list:
        order_total = 0
        formatted_items = []
        for item in order["items"]:
            # For each item, make a separate DB call to get product details (N+1 query)
            product = await product_collection.find_one({"_id": item["productId"]})
            if product:
                order_total += item["qty"] * product["price"]
                formatted_items.append({
                    "productDetails": {
                        "id": str(product["_id"]),
                        "name": product["name"]
                    },
                    "qty": item["qty"]
                })
        
        formatted_orders.append({
            "id": str(order["_id"]),
            "items": formatted_items,
            "total": order_total
        })

    return formatted_orders, total_orders_count