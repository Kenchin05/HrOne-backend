import motor.motor_asyncio
from bson.objectid import ObjectId


load_dotenv()

#  MongoDB Connection 
MONGO_DETAILS = os.getenv("MONGO_DETAILS")

if not MONGO_DETAILS:
    raise ValueError("MONGO_DETAILS environment variable not set!")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
db = client.hron_ecommerce


product_collection = db.get_collection("products")
order_collection = db.get_collection("orders")

# MongoDB uses BSON ObjectId for the `_id` field.
# We need to convert it to a string for JSON responses.
def str_object_id(id) -> str:
    return str(id)