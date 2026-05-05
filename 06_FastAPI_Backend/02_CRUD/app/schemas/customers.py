from pydantic import BaseModel, Field


class Customer(BaseModel):
    name: str = Field(..., min_length=2)
    phone: str
    budget: float = Field(..., gt=0)


class CustomerResponse(Customer):
    id: int
