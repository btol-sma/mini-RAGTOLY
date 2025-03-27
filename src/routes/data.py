from fastapi import FastAPI, APIRouter, Depends, UploadFile , status
from fastapi.responses import JSONResponse
import os
from helper.config import get_settings, Settings
from controllers import DataController

dataRouter = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1","data"]
)
@dataRouter.post("/upload/{project_id}")
async def upload_data(project_id:str, file : UploadFile , app_settings:Settings = Depends(get_settings)):
    
    # validate uploads
    is_valid, signal = DataController().validate_uplodes(file=file)

    if not is_valid:
        return JSONResponse(
            status_code= status.HTTP_400_BAD_REQUEST,
            content= {"signal": signal}
        )