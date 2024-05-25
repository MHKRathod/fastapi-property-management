from motor.motor_asyncio import AsyncIOMotorClient
from bson.objectid import ObjectId
from fastapi import HTTPException

MONGO_DETAILS = "mongodb://localhost:27017/propertyManagement"
client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.propertyManagement
property_collection = database.get_collection("properties")

def property_helper(property) -> dict:
    return {
        "id": str(property["_id"]),
        "propertyName": property["propertyName"],
        "address": property["address"],
        "city": property["city"],
        "state": property["state"],
    }
