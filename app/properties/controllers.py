from fastapi import HTTPException
from bson import ObjectId
from typing import List
from . import models, database
from .crud import (
    add_property, 
    retrieve_properties, 
    retrieve_properties_by_city, 
    update_property, 
    delete_property, 
    retrieve_property, 
    find_similar_properties
)
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_property(property: models.PropertySchema) -> dict:
    try:
        return await add_property(property.dict())
    except Exception as e:
        logger.error(f"Error adding property: {e}")
        raise HTTPException(status_code=500, detail="Error adding property")

async def get_properties() -> List[dict]:
    try:
        return await retrieve_properties()
    except Exception as e:
        logger.error(f"Error retrieving properties: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving properties")

async def get_properties_by_city(city_name: str) -> List[dict]:
    try:
        return await retrieve_properties_by_city(city_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error retrieving properties by city")

async def update_property_data(id: str, req: models.UpdatePropertyModel) -> dict:
    try:
        req_data = req.model_dump(exclude_unset=True)
        if not req_data:
            raise HTTPException(status_code=400, detail="No fields to update")
        if not await update_property(id, req_data):
            raise HTTPException(status_code=404, detail="Property not found")
        return await retrieve_property(id)
    except HTTPException as he:
        logger.error(f"HTTPException while updating property: {he.detail}")
        raise
    except Exception as e:
        logger.error(f"Exception while updating property: {e}")
        raise HTTPException(status_code=500, detail="Error updating property")

async def delete_property_data(id: str) -> dict:
    try:
        sanitized_id = id.strip()
        if not ObjectId.is_valid(sanitized_id):
            raise HTTPException(status_code=400, detail="Invalid property ID")
        if not await delete_property(sanitized_id):
            raise HTTPException(status_code=404, detail="Property not found")
        return {"message": "Property deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting property: {e}")
        raise HTTPException(status_code=500, detail="Error deleting property")

async def find_cities_by_state(state_name: str) -> List[str]:
    try:
        cities = await database.property_collection.distinct("city", {"state": state_name})
        if not cities:
            raise HTTPException(status_code=404, detail="No cities found for the given state")
        return cities
    except HTTPException as he:
        logger.error(f"Error finding cities by state: {he.detail}")
        raise he
    except Exception as e:
        logger.error(f"Error finding cities by state: {e}")
        raise HTTPException(status_code=500, detail="Error finding cities by state")

async def find_similar_properties_endpoint(property_id: str) -> List[dict]:
    try:
        return await find_similar_properties(property_id)
    except Exception as e:
        logger.error(f"Error finding similar properties: {e}")
        raise HTTPException(status_code=500, detail="Error finding similar properties")
