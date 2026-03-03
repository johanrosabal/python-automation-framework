# api_mock/main.py
from fastapi import FastAPI
from routes.user_routes import router as user_router
from routes.category_routes import router as category_router
from routes.product_routes import router as product_router

# uvicorn main:app --reload --port 8000
app = FastAPI(
    title="Test Automation Mock API",
    description="Mock REST API for testing automation scripts",
    version="1.0.0"
)


# Welcome Root
@app.get("/", summary="Root endpoint", tags=["Root"])
def read_root():
    return {
        "message": "Welcome to the Test Automation Mock API Crowley !",
        "docs": "/docs"
    }


# Include routes
app.include_router(user_router)
app.include_router(category_router)
app.include_router(product_router)
