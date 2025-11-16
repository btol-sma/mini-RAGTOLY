from fastapi import FastAPI, APIRouter, Depends, UploadFile , status,Request
from fastapi.responses import JSONResponse
import os
from helper.config import get_settings, Settings
from controllers import DataController , ProjectController , ProcessController
import aiofiles
from models import ResponseSignal
from routes.Schemes import ProcessRequest
import logging
from models.ProjectModel import ProjectModel
from models.ChunkModel import ChunkModel
from models.db_schemes import DataChunk, Asset
from models.enums.AssetTypeEnum import AssetTpyeEnum

from models.AssetModel import AssetModel

logger = logging.getLogger('uvicorn.error')

dataRouter = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1","data"]
)
@dataRouter.post("/upload/{project_id}")
async def upload_data(request:Request, project_id:str, file : UploadFile , app_settings:Settings = Depends(get_settings)):
    
    project_model = await ProjectModel.create_instance(db_client=request.app.db_client)
    project = await project_model.get_project_or_create_one(project_id=project_id)
    # validate uploads
    data_controller = DataController()
    is_valid, signal = data_controller.validate_uplodes(file=file)

    if not is_valid:
        return JSONResponse(
            status_code= status.HTTP_400_BAD_REQUEST,
            content= {"signal": signal}
        )
    
    project_dir_path = ProjectController().get_project_path(project_id = project_id)
    file_path, file_id= data_controller.generate_filepath(
        filename = file.filename , project_id= project_id 
    )
    try:
        async with aiofiles.open(file_path,"wb") as f:
            while chunck := await file.read(app_settings.FILE_DEFAULT_CHUNCK_SIZE):
                await f.write(chunck)
    except Exception  as e:

        logger.error(f"Error while uploading file : {e}")
    # store asset into db 
    asset_model = await AssetModel.create_instance(db_client= request.app.db_client)
    asset_resource = Asset(
        asset_project_id= project.id,
        asset_type= AssetTpyeEnum.FILE.value,
        asset_name=file_id,
        asset_size=os.path.getsize(file_path)
    )
    asset_record = await asset_model.create_asset(asset=asset_resource)
    return JSONResponse(
        content ={ 
            "signal": ResponseSignal.FILE_UPLOAD_SUCCESS.value,
            "file_id": str(asset_record.id),
            } )
@dataRouter.post("/process/{project_id}")
async  def process_endpoint(request: Request,project_id:str , process_request : ProcessRequest):
    file_id = process_request.file_id
    chunk_size = process_request.chunc_size
    overlap_size = process_request.overlap_size
    do_reset = process_request.reset

    project_model = await ProjectModel.create_instance(db_client=request.app.db_client)
    project = await project_model.get_project_or_create_one(project_id=project_id)
    
    process_controller = ProcessController(project_id=project_id)
    

    file_content = process_controller.get_file_content(file_id=file_id)
    file_chunk = process_controller.process_file_content(
        file_content= file_content,
        file_id= file_id,
        chunck_size=chunk_size,
        overlap_size=overlap_size,
        )
    if file_chunk is None or len(file_chunk)==0:
        return JSONResponse(
            status_code= status.HTTP_400_BAD_REQUEST,
            content = {
                "signal": ResponseSignal.PROCESSING_FAILED.value
            }
        )
    file_chunks_records = [
        DataChunk(
            chunk_text=chunk.page_content,
            chunk_metadata=chunk.metadata,
            chunk_order=i+1,
            chunk_project_id=project.id,
        )
        for i, chunk in enumerate(file_chunk)
    ]

    chunk_model = await ChunkModel.create_instance(
        db_client=request.app.db_client
    )

    if do_reset == 1:
        _ = await chunk_model.delete_chunks_by_project_id(
            project_id=project.id
        )

    no_records = await chunk_model.insert_many_chunks(chunks=file_chunks_records)

    return JSONResponse(
        content={
            "signal": ResponseSignal.PROCESSING_SUCCESS.value,
            "inserted_chunks": no_records
        }
    )