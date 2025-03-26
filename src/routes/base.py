from fastapi import FastAPI, APIRouter, Depends
import os
from helper.config import get_settings, Settings

baseRouter = APIRouter(
    prefix="/api/v1",
    tags=["api_v1"]
)
@baseRouter.get("/")
async def welcome(app_settings: Settings = Depends(get_settings)):
    app_name = app_settings.APP_NAME
    app_version = app_settings.APP_VERSION

    return {
        "app" : app_name,
        "version": app_version 
    }