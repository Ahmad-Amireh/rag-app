from fastapi import FastAPI, Depends, APIRouter, UploadFile, status
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings 
from controllers import DataController, ProjectController
import aiofiles
import os
from models import ResponseSignal

data_router = APIRouter(
    prefix = "/api/v1/data",
    tags =["api_v1","data"]
)

@data_router.post("/upload/{project_id}") #for each tenant
async def upload_data(project_id: str, file: UploadFile, app_settings: Settings = Depends(get_settings)):
    
    #validate the file properties
    is_valid, result_signal = DataController().validate_upload_file(file= file)
    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": result_signal
            })

    project_dir_path = ProjectController().get_project_path(project_id= project_id)
    file_path = os.path.join(project_dir_path, file.filename) # the file that write on disk
    async with aiofiles.open(file_path, "wb") as f :
        while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
            await f.write(chunk)
        return JSONResponse(
        content={
            "signal": ResponseSignal.FILE_UPLOAD_SUCCESS.value
        })

