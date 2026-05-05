from fastapi import APIRouter, Depends

from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate):
    return auth_service.register_user(user)


@router.post("/login", response_model=Token)
def login(user: UserLogin):
    return auth_service.login_user(user.username, user.password)


@router.get("/me", response_model=UserResponse)
def get_me(token: str = Depends(auth_service.oauth2_scheme)):
    return auth_service.get_current_user(token)


@router.get("/protected")
def protected_route(token: str = Depends(auth_service.oauth2_scheme)):
    current_user = auth_service.get_current_user(token)

    return {
        "msg": "You are allowed",
        "user": current_user,
    }
