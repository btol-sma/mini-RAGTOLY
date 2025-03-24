from fastapi import FastAPI, APIRouter
import os

baseRouter = APIRouter(
    prefix="/api/v1",
    tags=["api_v1"]
)
@baseRouter.get("/")
async def welcome():
    app_name = os.getenv('APP_NAME')
    app_version = os.getenv('APP_VERSION')

    return {
        "app" : app_name,
        "version": app_version 
    }