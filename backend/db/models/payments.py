from pydantic import BaseModel, Field
from datetime import datetime

class PaymentRequest(BaseModel):
    amount: float = Field(..., gt=0)

class PaymentRecord(BaseModel):
    tenant_uid: str
    amount: float
    timestamp: datetime
    invoice_id: str