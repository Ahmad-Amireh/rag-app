from fastapi import FastAPI, Depends, APIRouter, UploadFile 
from helpers.config import get_settings, Settings 
from controllers import DataController

data_router = APIRouter(
    prefix = "/api/v1/data",
    tags =["api_v1","data"]
)

@data_router.post("/upload/{project_id}") #for each tenant
async def upload_data(project_id: str, file: UploadFile, app_settings: Settings = Depends(get_settings)):
    
    #validate the file properties
    is_valid, result_signal = DataController().validate_upload_file(file= file)
    return {"signal":result_signal}