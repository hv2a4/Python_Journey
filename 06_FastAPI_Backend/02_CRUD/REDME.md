# 🚀 FastAPI – CRUD API (Day 5–7)

## 📌 Mục tiêu

- Xây dựng API CRUD hoàn chỉnh
- Áp dụng:
  - Pydantic Model
  - Response Model
  - HTTPException
  - Tách project (router / service / schema)

---

## 📁 Cấu trúc

```bash
02_CRUD/
├── main.py
├── app/
│   ├── routers/
│   │   └── customers.py
│   ├── schemas/
│   │   └── customer.py
│   └── services/
│       └── customer_service.py
```

---

## ▶️ Chạy server

```bash
uvicorn main:app --reload
```

Docs:

```
http://127.0.0.1:8000/docs
```

---

# 📚 API

## 1. GET all customers

```http
GET /customers
```

---

## 2. GET customer by ID

```http
GET /customers/{id}
```

---

## 3. CREATE customer

```http
POST /customers
```

```json
{
  "name": "Anh A",
  "phone": "0909",
  "budget": 2000000000
}
```

👉 Status: `201 Created`

---

## 4. UPDATE customer

```http
PUT /customers/{id}
```

---

## 5. DELETE customer

```http
DELETE /customers/{id}
```

---

# 🧠 Kiến thức

## CRUD

| Method | Ý nghĩa |
|-------|--------|
| GET | Lấy dữ liệu |
| POST | Tạo mới |
| PUT | Cập nhật |
| DELETE | Xóa |

---

## Response Model

```python
response_model=CustomerResponse
```

👉 Giúp:
- Chuẩn hóa dữ liệu trả về
- Không leak dữ liệu

---

## HTTPException

```python
raise HTTPException(status_code=404, detail="Not found")
```

👉 Trả lỗi chuẩn API

---

# 🎯 Kết quả

- API CRUD hoàn chỉnh
- Tách project chuẩn
- Hiểu luồng backend thực tế

---

# 🚀 Bước tiếp

- Validation nâng cao
- Auth (JWT)
- Database