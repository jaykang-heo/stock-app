from fastapi import FastAPI
from stock_controller import router as stock_router
from file_controller import router as file_router
import middleware_controller

app = FastAPI()

app.include_router(stock_router)
app.include_router(file_router)
middleware_controller.add_cors_middleware(app)
