from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
)
from app.schemas.user import UserCreate

# * Lấy token từ header Authorization: Bearer <token>
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


#! Fake database (RAM) → restart server sẽ mất dữ liệu
users = []


def register_user(user: UserCreate):
    """
    Đăng ký user mới.

    Flow:
    - Kiểm tra trùng username
    - Hash password
    - Lưu vào hệ thống
    """
    for old_user in users:
        if old_user["username"] == user.username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username đã tồn tại",
            )

    new_user = {
        "id": len(users) + 1,
        "username": user.username,
        "email": user.email,
        "hashed_password": hash_password(user.password),
    }

    users.append(new_user)

    # ? Không trả password/hash ra ngoài
    return {
        "id": new_user["id"],
        "username": new_user["username"],
        "email": new_user["email"],
    }


def login_user(username: str, password: str):
    """
    Đăng nhập.

    Flow:
    - Tìm user theo username
    - Verify password
    - Tạo JWT token nếu hợp lệ
    """
    user = None

    for u in users:
        if u["username"] == username:
            user = u
            break

    #! Không tiết lộ sai username hay password (bảo mật)
    if not user or not verify_password(password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sai username hoặc password",
        )

    token = create_access_token(data={"sub": user["username"]})

    return {
        "access_token": token,
        "token_type": "bearer",
    }


def get_current_user(token: str):
    """
    Lấy thông tin user hiện tại từ token.

    Flow:
    - Decode token
    - Lấy username từ payload (sub)
    - Truy ngược lại user trong hệ thống
    """
    payload = decode_access_token(token)

    #! Token sai hoặc hết hạn
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token không hợp lệ hoặc đã hết hạn",
        )

    username = payload.get("sub")

    for user in users:
        if user["username"] == username:
            return {
                "id": user["id"],
                "username": user["username"],
                "email": user["email"],
            }

    #! Token hợp lệ nhưng user không tồn tại (edge case)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Không tìm thấy user",
    )
