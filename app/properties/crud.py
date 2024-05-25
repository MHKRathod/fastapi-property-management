from typing import List
from .database import property_collection, property_helper
from bson.objectid import ObjectId
from fastapi import HTTPException
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def add_property(property_data: dict) -> dict:
    try:
        property = await property_collection.insert_one(property_data)
        new_property = await property_collection.find_one({"_id": property.inserted_id})
        return property_helper(new_property)
    except Exception as e:
        logger.error(f"Error adding property: {e}")
        raise HTTPException(status_code=500, detail="Error adding property")

async def retrieve_properties() -> List[dict]:
    try:
        return [property_helper(property) async for property in property_collection.find()]
    except Exception as e:
        logger.error(f"Error retrieving properties: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving properties")

async def retrieve_properties_by_city(city_name: str) -> List[dict]:
    try:
        return [property_helper(property) async for property in property_collection.find({"city": city_name})]
    except Exception as e:
        logger.error(f"Error retrieving properties by city: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving properties by city")

async def retrieve_property(id: str) -> dict:
    try:
        property = await property_collection.find_one({"_id": ObjectId(id)})
        return property_helper(property) if property else None
    except Exception as e:
        logger.error(f"Error retrieving property: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving property")

async def update_property(id: str, data: dict) -> bool:
    try:
        if not data:
            return False
        result = await property_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        return result.modified_count > 0
    except Exception as e:
        logger.error(f"Error updating property: {e}")
        raise HTTPException(status_code=500, detail="Error updating property")

async def delete_property(id: str) -> bool:
    try:
        result = await property_collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count > 0
    except Exception as e:
        logger.error(f"Error deleting property: {e}")
        raise HTTPException(status_code=500, detail="Error deleting property")

async def find_similar_properties(property_id: str) -> List[dict]:
    try:
        property_city = await property_collection.find_one({"_id": ObjectId(property_id)}, {"city": 1})
        if not property_city:
            raise HTTPException(status_code=404, detail="Property not found")
        return [property_helper(property) async for property in property_collection.find({"city": property_city["city"]}) if str(property["_id"]) != property_id]
    except Exception as e:
        logger.error(f"Error finding similar properties: {e}")
        raise HTTPException(status_code=500, detail="Error finding similar properties")
