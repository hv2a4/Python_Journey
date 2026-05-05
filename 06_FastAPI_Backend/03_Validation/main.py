from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional, Literal
import re

app = FastAPI(title="Validation Practice")

# =========================
# SCHEMA
# =========================


class Customer(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    phone: str
    email: Optional[EmailStr] = None
    source: Literal["facebook", "zalo", "referral", "hot_data"]
    status: Literal["new", "follow", "closed"] = "new"
    budget: float = Field(..., gt=0)

    # validate phone custom
    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):
        if not re.fullmatch(r"0\d{9,10}", value):
            raise ValueError("Số điện thoại không hợp lệ")
        return value

    # normalize name
    @field_validator("name")
    @classmethod
    def normalize_name(cls, v):
        return v.strip().title()


class CustomerResponse(Customer):
    id: int


# =========================
# FAKE DB
# =========================

customers = []
# =========================
# CREATE
# =========================


@app.post(
    "/customers", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED
)
def create_customer(customer: Customer):
    new_customer = {
        "id": len(customers) + 1,
        "name": customer.name,
        "phone": customer.phone,
        "email": customer.email,
        "source": customer.source,
        "status": customer.status,
        "budget": customer.budget,
    }
    customers.append(new_customer)
    return new_customer


# =========================
# GET ALL + FILTER
# =========================


@app.get("/customers", response_model=list[CustomerResponse])
def get_customers(
    name: Optional[str] = None,
    source: Optional[str] = None,
    status_filter: Optional[str] = None,
    min_budget: Optional[float] = None,
):
    result = customers

    if name:
        result = [c for c in result if name.lower() in c["name"].lower()]

    if source:
        result = [c for c in result if c["source"] == source]

    if status_filter:
        result = [c for c in result if c["status"] == status_filter]

    if min_budget is not None:
        result = [c for c in result if c["budget"] >= min_budget]

    return result


# =========================
# GET BY ID
# =========================


@app.get("/customers/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: int):
    for c in customers:
        if c["id"] == customer_id:
            return c

    raise HTTPException(status_code=404, detail="Customer not found")
