import fastapi
import unidecode

customers = [
    {"id": 1, "name": "Anh A", "phone": "0909", "budget": 2_000_000_000},
    {"id": 2, "name": "Chị B", "phone": "0911", "budget": 3_000_000_000},
]


def get_all_customers(name: str | None = None, min_budget: float | None = None):
    result = customers.copy()
    if name:
        keyword = unidecode.unidecode(name.lower())
        result = [
            customer
            for customer in result
            if keyword in unidecode.unidecode(customer["name"].lower())
        ]

    if min_budget is not None:
        result = [customer for customer in result if customer["budget"] >= min_budget]
    return result


def get_customer_by_id(customer_id: int):
    for customer in customers:
        if customer["id"] == customer_id:
            return customer
    raise fastapi.HTTPException(status_code=404, detail="Customer not found")


def create_customer(customer):
    new_customer = {
        "id": len(customers) + 1,
        "name": customer.name,
        "phone": customer.phone,
        "budget": customer.budget,
    }
    customers.append(new_customer)
    return new_customer


def update_customer(customer_id: int, customer):
    for index, old_customer in enumerate(customers):
        if old_customer["id"] == customer_id:
            update_customers = {
                "id": customer_id,
                "name": customer.name,
                "phone": customer.phone,
                "budget": customer.budget,
            }
        customers[index] = update_customers
        return update_customers
    raise fastapi.HTTPException(status_code=404, detail="Customer not found")


def delete_customer(customer_id: int):
    for index, customer in enumerate(customers):
        if customer["id"] == customer_id:
            customers.pop(index)
            return {"msg": "Customer deleted!"}
    raise fastapi.HTTPException(status_code=404, detail="Customer not found!")
