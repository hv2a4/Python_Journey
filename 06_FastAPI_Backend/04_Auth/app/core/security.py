from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext

#! TODO: đưa SECRET_KEY ra biến môi trường khi deploy production
SECRET_KEY = "change-this-secret-key"

# ? Thuật toán mã hóa token
ALGORITHM = "HS256"

# ? Thời gian sống của access token (phút)
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# * Context dùng để hash password bằng bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hash mật khẩu trước khi lưu vào hệ thống.
    Không bao giờ lưu password dạng plain text.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    So sánh mật khẩu người dùng nhập với mật khẩu đã hash trong hệ thống.
    Dùng trong quá trình login.
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    """
    Tạo JWT token.

    - Nhận payload (data)
    - Gắn thêm thời gian hết hạn (exp)
    - Encode thành token

    Token này sẽ được client dùng để gọi API bảo vệ.
    """
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str):
    """
    Giải mã JWT token.

    - Nếu hợp lệ → trả payload
    - Nếu sai hoặc hết hạn → trả None
    """
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
