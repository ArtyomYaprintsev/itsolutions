from fastapi import FastAPI

from server.core.exceptions import CustomException, exception_handler
from server.routers import router

app = FastAPI()

app.add_exception_handler(CustomException, exception_handler)  # type: ignore

app.include_router(router, prefix='/api')
