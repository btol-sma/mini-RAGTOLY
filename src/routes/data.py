from fastapi import FastAPI, APIRouter, Depends, UploadFile
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
    is_valid = DataController().validate_uplodes(file=file)

    return is_valid