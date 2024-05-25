from typing import Optional
from pydantic import BaseModel

class PropertySchema(BaseModel):
    propertyName: str
    address: str
    city: str
    state: str

class UpdatePropertyModel(BaseModel):
    propertyName: Optional[str]
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    



 