from fastapi import APIRouter, status
from app.schemas.customers import Customer, CustomerResponse
from app.services import customer_service

router = APIRouter(prefix="/customer", tags=["Customers"])


@router.get("/", response_model=list[CustomerResponse])
def get_customers(name: str | None = None, min_budget: float | None = None):
    return customer_service.get_all_customers(name, min_budget)


@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: int):
    return customer_service.get_customer_by_id(customer_id)


@router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(customer: Customer):
    return customer_service.create_customer(customer)


@router.put("/", response_model=CustomerResponse)
def update_customer(customer_id: int, customer: Customer):
    return customer_service.update_customer(customer_id, customer)


@router.delete("/{customer_id}")
def delete_customer(customer_id: int):
    return customer_service.delete_customer(customer_id)
