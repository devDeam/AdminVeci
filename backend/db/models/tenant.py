from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from bson import ObjectId
from datetime import datetime

class Tenant(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")  # Alias para mapear el _id de MongoDB
    name: str
    uid: str
    email: EmailStr
    apt: str
    acct_status: Optional[float] = 0.0
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda dt: dt.isoformat()
        }
