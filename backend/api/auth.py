from fastapi import APIRouter
from db.models.user import User, UserLogin
from services.auth_service import AuthService

router = APIRouter(prefix="/auth")

@router.post("/register")
def register(user: User):
    return AuthService.register(user)

@router.post("/login")
def login(credentials: UserLogin):
    return AuthService.login(credentials)
