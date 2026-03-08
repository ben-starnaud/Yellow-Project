from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from db.db import engine, Base
from routes.products import router as product_router
from routes.applications import router as app_router
import models.models # This MUST be imported so Base knows the tables

app = FastAPI(title="Yellow API")

# Ensure uploads directory exists
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# CORS Configuration
origins = [
    "http://localhost:9000", 
    "http://127.0.0.1:9000",
    "http://192.168.0.110:9000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include Routers
app.include_router(app_router)
app.include_router(product_router)

@app.get("/")
def root():
    return {"status": "Yellow Loan API is running"}