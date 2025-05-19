from db.database import db
from db.models.tenant import Tenant
from datetime import datetime
from bson import ObjectId

class TenantService:
    collection = db["tenants"]

    @classmethod
    def create(cls, tenant: Tenant):
        if cls.collection.find_one({"uid": tenant.uid}):
            return {"success": False, "message": "El documento de identidad ya existe"}
        
        data = tenant.dict(by_alias=True, exclude_unset=True, exclude_none=True)

        # Agregar fechas de creación y actualización
        now = datetime.utcnow()
        data["createdAt"] = now
        data["updatedAt"] = now
        print("Datos que se insertarán:", data)
        cls.collection.insert_one(data)
        return {"success": True}

    @classmethod
    def get_all(cls, search: str = ""):
        search = search or ""  # Asegura que no sea None
        if search.strip():     # Solo aplica filtro si hay algo real que buscar
            query = {
                "$or": [
                    {"name": {"$regex": search, "$options": "i"}},
                    {"uid": {"$regex": search, "$options": "i"}},
                    {"email": {"$regex": search, "$options": "i"}},
                    {"apt": {"$regex": search, "$options": "i"}},
                ]
            }
        else:
            query = {}

        results = cls.collection.find(query)
        tenants = [{**doc, "_id": str(doc["_id"])} for doc in results]
        return tenants


    @classmethod
    def get_tenant(cls, uid: str):
        results = cls.collection.find({"uid": {"$regex": uid, "$options": "i"}})
        tenants = [{**doc, "_id": str(doc["_id"])} for doc in results]
        return tenants or {"message": "Inquilino no encontrado"}

    @classmethod
    def delete(cls, id_str: str):
        try:
            oid = ObjectId(id_str)
        except Exception:
            return {"success": False, "detail": "ID inválido"}

        result = cls.collection.delete_one({"_id": oid})
        return {"success": result.deleted_count > 0}

    @classmethod
    def update(cls, id_str: str, data: dict):
        data.pop("_id", None)
        data.pop("uid", None)
        data["updatedAt"] = datetime.utcnow()

        result = cls.collection.update_one({"_id": ObjectId(id_str)}, {"$set": data})
        return {"success": result.modified_count > 0}
