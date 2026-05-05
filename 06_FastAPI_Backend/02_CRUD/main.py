from fastapi import FastAPI

from app.routers import customers

app = FastAPI(title="API CRUD Customers")

app.include_router(customers.router)


@app.get("/")
def root():
    return {"msg": "API is running"}
