# 🚀 FastAPI – Validation (Day 8)

## 📌 Mục tiêu

- Validate dữ liệu nâng cao
- Chuẩn hóa input
- Xây dựng schema chặt chẽ

---

## ▶️ Chạy server

```bash
uvicorn main:app --reload
```

---

# 📚 API

## CREATE customer

```http
POST /customers
```

```json
{
  "name": "Nguyễn Văn A",
  "phone": "0912345678",
  "email": "test@gmail.com",
  "source": "facebook",
  "budget": 2000000000
}
```

---

# 🧠 Kiến thức

## 1. Field

```python
name: str = Field(..., min_length=2)
budget: float = Field(..., gt=0)
```

👉 Kiểm tra:
- độ dài
- giá trị

---

## 2. Email

```python
email: EmailStr
```

👉 Validate email chuẩn

---

## 3. Literal (enum)

```python
source: Literal["facebook", "zalo", "referral", "hot_data"]
```

👉 Giới hạn giá trị

---

## 4. Custom validator

```python
@field_validator("phone")
```

👉 Validate logic riêng

---

## 5. Clean data

```python
name → strip + title
```

👉 Chuẩn hóa dữ liệu

---

# 🧪 Test

## ✔️ Hợp lệ

```json
{
  "name": "  nguyen van a  ",
  "phone": "0912345678",
  "email": "test@gmail.com",
  "source": "facebook",
  "budget": 2000000000
}
```

---

## ❌ Không hợp lệ

```json
{
  "name": "A",
  "phone": "123",
  "source": "tiktok",
  "budget": -100
}
```

👉 Status: `422`

---

# 🎯 Kết quả

- Validate dữ liệu chuẩn production
- Biết kiểm soát input từ client
- Hiểu sâu Pydantic

---

# 🚀 Bước tiếp

- Authentication (JWT)
- Role (admin / sale)
- Bảo mật API