from fastapi import APIRouter, Query
from db.models.tenant import Tenant
from services.tenant_service import TenantService
from db.models.payments import PaymentRequest
from services.payment_service import register_payment

router = APIRouter(prefix="/tenants")

@router.post("/create")
def create_tenant(tenant: Tenant):
    return TenantService.create(tenant)

@router.get("/")
def list_tenants(search: str = ""):
    return TenantService.get_all(search)

@router.get("/{uid}")
def get_tenant(uid: str):
    return TenantService.get_tenant(uid)

@router.delete("/{uid}")
def delete_tenant(uid: str):
    return TenantService.delete(uid)

@router.put("/{uid}")
def update_tenant(uid: str, data: dict):
    return TenantService.update(uid, data)

@router.post("/{tenant_uid}/pay")
def pay_tenant_debt(tenant_uid: str, payment: PaymentRequest):
    result = register_payment(tenant_uid, payment.amount)
    return result