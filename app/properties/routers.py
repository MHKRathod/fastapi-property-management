# app/api/properties/routers.py
from fastapi import APIRouter, Depends, HTTPException,Body
from typing import List
from . import controllers,models
from .controllers import find_cities_by_state
from .models import UpdatePropertyModel

router = APIRouter()

@router.post("/properties", response_description="Add new property", response_model=dict)
async def create_property(property: models.PropertySchema = Depends()):
    return await controllers.create_property(property)

@router.get("/properties", response_description="List all properties", response_model=list)
async def get_properties():
    return await controllers.get_properties()

@router.get("/properties/{city_name}", response_description="Get properties by city", response_model=List[dict])
async def get_properties_by_city(city_name: str):
    return await controllers.get_properties_by_city(city_name)

@router.put("/properties/{id}", response_description="Update a property", response_model=dict)
async def update_property_data(id: str, req: UpdatePropertyModel = Body(...)):
    return await controllers.update_property_data(id, req)

@router.delete("/properties/{id}", response_description="Delete a property")
async def delete_property_data(id: str):
    return await controllers.delete_property_data(id)

@router.get("/find_cities_by_state/{state_name}", response_description="Get cities by state", response_model=List[str])
async def get_cities_by_state(state_name: str):
    return await find_cities_by_state(state_name)

@router.get("/find_similar_properties/{property_id}", response_description="Find similar properties by city", response_model=List[dict])
async def find_similar_properties_endpoint(property_id: str):
    return await controllers.find_similar_properties_endpoint(property_id)
