from fastapi import FastAPI

from app.routers import auth

app = FastAPI(title="FastAPI Auth JWT")

app.include_router(auth.router)


@app.get("/")
def root():
    return {"msg": "Auth API is running"}
