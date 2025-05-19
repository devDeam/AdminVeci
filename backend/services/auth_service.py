from db.database import db
from db.models.user import User, UserLogin
from passlib.context import CryptContext
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
collection = db["users"]

class AuthService:

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain: str, hashed: str) -> bool:
        return pwd_context.verify(plain, hashed)

    @classmethod
    def register(cls, user: User):
        if collection.find_one({"username": user.username}):
            return {"success": False, "message": "El usuario ya existe"}

        user_dict = user.dict(by_alias=True, exclude_unset=True)
        user_dict["password"] = cls.hash_password(user.password)
        
        now = datetime.utcnow()
        user_dict["createdAt"] = now
        user_dict["updatedAt"] = now

        collection.insert_one(user_dict)
        return {"success": True}

    @classmethod
    def login(cls, credentials: UserLogin):
        user = collection.find_one({"username": credentials.username})
        if not user:
            return {"success": False, "message": "Usuario no encontrado"}
        if not cls.verify_password(credentials.password, user["password"]):
            return {"success": False, "message": "Contraseña incorrecta"}
        return {"success": True, "role": user.get("role", "basic")}
