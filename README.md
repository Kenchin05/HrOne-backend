# E-Commerce API Backend

This is the backend service for a simple e-commerce application, built with Python 3, FastAPI, and MongoDB. It handles the core logic for managing products and processing user orders.

## How It Works

This project is built around a clean, service-oriented architecture to keep the code organized and maintainable.

### Tech Stack
- **FastAPI**: For building the asynchronous API. It's fast, provides automatic data validation, and generates interactive documentation.
- **Uvicorn**: As the ASGI server to run the application.
- **MongoDB**: A NoSQL database used for storing product and order data. The free tier on MongoDB Atlas is perfect for this.
- **Motor**: The asynchronous Python driver for MongoDB, which works well with FastAPI's `async/await` syntax.
- **Pydantic**: Used by FastAPI to define data shapes for request bodies, ensuring all incoming data is valid before it hits the application logic.

### Application Flow
The application logic is separated into a few key files inside the `app/` directory:

1.  `routes.py`: This is the entry point for all API requests. It defines the endpoints (e.g `/products`, `/orders`) and handles parsing request data like path parameters, query params, and the request body. It then calls the appropriate function in the `crud.py` module to handle the logic.

2.  `crud.py`: This file (Create, Read, Update, Delete) contains all the database interaction logic. Functions here are responsible for querying the collections in MongoDB. For instance, `add_product` inserts a new document, and `retrieve_orders_by_user` fetches data from the database.

3.  `models.py`: Defines the Pydantic models. These are essentially the data schemas for the application. FastAPI uses these to validate incoming requests. For example, when a `POST` request is made to `/products`, the JSON body is validated against the `ProductCreate` model.

### Database Logic for Orders
To get a user's order details, the app needs to combine data from the `orders` and `products` collections.

The current implementation in `crud.py` does this with a straightforward, procedural approach:
- It first queries the `orders` collection to find all orders matching the `user_id`.
- Then, it iterates through each order and each item within that order.
- For every item, it performs a separate `find_one` query on the `products` collection to get the details for that specific product.


---

## Getting Started

Follow these steps to get the project running locally.

### 1. Prerequisites
- Python 3.10+
- A running MongoDB instance (local or via [MongoDB Atlas](https://www.mongodb.com/cloud/atlas))

### 2. Setup
Clone the repository, create and activate a virtual environment, and install the dependencies.
```bash
# Clone the repo
git clone <your-repository-url>
cd <repository-directory>

# Set up and activate the virtual environment
python3 -m venv venv
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### 3. Database Configuration
1.  Open `app/database.py`.
2.  Update the `MONGO_DETAILS` variable with your MongoDB connection string.
3.  **If using MongoDB Atlas**, make sure you've whitelisted your current IP address in the "Network Access" settings of your cluster.

### 4. Run the Server
Use Uvicorn to start the local server.
```bash
uvicorn app.main:app --reload
```
The API will be live at `http://127.0.0.1:8000`.

The interactive API docs (via Swagger UI) are available at `http://127.0.0.1:8000/docs`. This is the best place to test the endpoints.

---

## API Endpoints(all of the data shown here are for illustrative purposes only)

### Product API

#### `POST /products`
Adds a new product to the database.

**Request Body:**
```json
{
  "name": "Classic White T-Shirt",
  "price": 799.0,
  "sizes": [
    {
      "size": "M",
      "quantity": 50
    },
    {
      "size": "L",
      "quantity": 30
    }
  ]
}
```
**Response (`201`):**
```json
{
  "id": "63f8b1a3b4c1e2f3a4b5c6d7"
}
```

#### `GET /products`
Lists all products with optional filters and pagination.

**Query Parameters:**
- `name` (str): Search by name (case-insensitive, partial match).
- `size` (str): Filter by available size (e.g., "M").
- `limit` (int): Defaults to 10.
- `offset` (int): Defaults to 0.

**Response (`200`):**
```json
{
  "data": [
    {
      "id": "63f8b1a3b4c1e2f3a4b5c6d7",
      "name": "Classic White T-Shirt",
      "price": 799.0
    }
  ],
  "page": {
    "limit": 1,
    "next": null,
    "previous": null
  }
}
```
---
### Order API

#### `POST /orders`
Places a new order. `productId` must be a valid ObjectId of an existing product.

**Request Body:**
```json
{
  "userId": "user_abc_123",
  "items": [
    {
      "productId": "63f8b1a3b4c1e2f3a4b5c6d7",
      "qty": 2
    }
  ]
}
```
**Response (`201`):**
```json
{
  "id": "63f8b2a4c5d1e2f3a4b5c6d8"
}
```

#### `GET /orders/{user_id}`
Fetches all orders for a given user, with product details joined in.

**Query Parameters:**
- `limit` (int): Defaults to 10.
- `offset` (int): Defaults to 0.

**Response (`200`):**
```json
{
  "data": [
    {
      "id": "63f8b2a4c5d1e2f3a4b5c6d8",
      "items": [
        {
          "productDetails": {
            "id": "63f8b1a3b4c1e2f3a4b5c6d7",
            "name": "Classic White T-Shirt"
          },
          "qty": 2
        }
      ],
      "total": 1598.0
    }
  ],
  "page": {
    "limit": 1,
    "next": null,
    "previous": null
  }
}
```

---

## Error Handling

The API uses standard HTTP status codes to indicate the success or failure of a request.
- `2xx` codes indicate success.
- `4xx` codes indicate a client-side error (e.g., invalid request data). 
- `5xx` codes indicate a server-side error.



