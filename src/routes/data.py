from fastapi import FastAPI , APIRouter , Depends , UploadFile , File
from helpers.config import get_settings , Settings
from controllers import DataController

base_router = APIRouter(
    prefix="/api/data",
    tags=["api_v1","data"],
)

@base_router.get("/upload/{project_id}")
async def upload_data(project_id: str, file: UploadFile,
                        settings: Settings = Depends(get_settings)):

   is_valid = DataController().validate_uploaded_file(file=file)

   return is_valid
