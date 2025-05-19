from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal
from bson import ObjectId
from datetime import datetime

class User(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str
    lastName: str
    uid: str
    username: str
    email: EmailStr
    password: str
    role: Literal["admin", "basic"] = "basic"
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: lambda dt: dt.isoformat()}

class UserLogin(BaseModel):
    username: str
    password: str