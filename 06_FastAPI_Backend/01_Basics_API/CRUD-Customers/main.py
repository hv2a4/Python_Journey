# * ============ IMPORTS ============
# ! Import FastAPI framework và các utilities
from fastapi import FastAPI, status, HTTPException

# ! Pydantic để validate dữ liệu input/output
from pydantic import BaseModel, Field

# ! unidecode để chuyển đổi ký tự có dấu thành không dấu (để search)
from unidecode import unidecode

# * Khởi tạo ứng dụng FastAPI
app = FastAPI(title="API quản lý khách hàng")


# * ============ MODELS (Pydantic Schemas) ============
# ? Dùng để validate dữ liệu từ client gửi lên
class Customer(BaseModel):
    # ! name: bắt buộc, ít nhất 2 ký tự
    name: str = Field(..., min_length=2)
    # ! phone: số điện thoại (chuỗi)
    phone: str
    # ! budget: tiền, bắt buộc, phải > 0
    budget: float = Field(..., gt=0)


# ? Model trả về cho client (có thêm id)
class CustomerResponse(Customer):
    id: int


# * ============ DATABASE (Mô phỏng - In-memory) ============
# ? Trong thực tế: sử dụng database thật (PostgreSQL, MongoDB, ...)
# ! Tạm thời dùng list để lưu dữ liệu (mất hết khi restart server)
customers = [
    {"id": 1, "name": "Anh A", "phone": "0903", "budget": 120000000},
    {"id": 2, "name": "Anh B", "phone": "0703", "budget": 300000000},
]


# * ============ ENDPOINTS (API Routes) ============


# * [GET] Lấy danh sách tất cả khách hàng (có thể filter)
# ? Hỗ trợ 2 query parameters: name (tìm kiếm) và min_budget (lọc theo ngân sách)
@app.get("/customers", response_model=list[CustomerResponse])
def get_customer(name: str | None = None, min_budget: float | None = None):
    # ! Copy danh sách để không modify dữ liệu gốc
    result = customers.copy()

    # ? Filter theo tên nếu có (không phân biệt hoa/thường, không dấu)
    if name:
        keyword = unidecode(name.lower())
        result = [c for c in result if keyword in unidecode(c["name"].lower())]

    # ? Filter theo ngân sách tối thiểu nếu có
    if min_budget is not None:
        result = [c for c in result if c["budget"] >= min_budget]

    return result


# * [GET] Lấy chi tiết khách hàng theo ID
# ? URL parameter: customer_id (bắt buộc)
@app.get("/customers/{customer_id}", response_model=CustomerResponse)
def get_customer_by_id(customer_id: int):
    # ! Duyệt qua từng khách hàng để tìm ID khớp
    for c in customers:
        if c["id"] == customer_id:
            return c

    # ! Nếu không tìm thấy → trả về lỗi 404
    raise HTTPException(status_code=404, detail="Customer not found")


# * [POST] Tạo khách hàng mới
# ? Request body: Customer model (name, phone, budget)
# ! HTTP Status 201: Created (tài nguyên được tạo thành công)
@app.post(
    "/customers", status_code=status.HTTP_201_CREATED, response_model=CustomerResponse
)
def create_customer(customer: Customer):
    # ! Tạo object mới với ID tự động (ID = số lượng customers + 1)
    new_customer = {
        "id": len(customers) + 1,
        "name": customer.name,
        "phone": customer.phone,
        "budget": customer.budget,
    }

    # ! Thêm khách hàng vào danh sách
    customers.append(new_customer)

    # ! Trả về khách hàng vừa tạo
    return new_customer


# * [PUT] Cập nhật khách hàng theo ID
# ? URL parameter: customer_id
# ? Request body: Customer model (dữ liệu mới)
@app.put("/customers/{customer_id}", response_model=CustomerResponse)
def update_customer(customer_id: int, customer: Customer):
    # ! Duyệt qua danh sách để tìm khách hàng cần cập nhật
    for c in customers:
        if c["id"] == customer_id:
            # ! model_dump(): chuyển Pydantic model thành dict
            # ! update(): cập nhật các field của dict
            c.update(customer.model_dump())
            return c

    # ! Nếu không tìm thấy → trả về lỗi 404
    raise HTTPException(status_code=404, detail="Customer not found!")


# * [DELETE] Xóa khách hàng theo ID
# ? URL parameter: customer_id
# ! HTTP Status 204: No Content (xóa thành công, không có dữ liệu trả về)
@app.delete("/customers/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(customer_id: int):
    # ! Duyệt qua danh sách với enumerate để lấy index
    for i, c in enumerate(customers):
        if c["id"] == customer_id:
            # ! Xóa khách hàng tại vị trí i
            customers.pop(i)
            return

    # ! Nếu không tìm thấy → trả về lỗi 404
    raise HTTPException(status_code=404, detail="Customer not found")
