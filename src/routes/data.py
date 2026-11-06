import os
import aiofiles
from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings
from controllers import DataController, ProjectController
from models import ResponseConstants

data_router = APIRouter(
    prefix="/api/data",
    tags=["api_v1", "data"],
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str, file: UploadFile,
                      app_settings: Settings = Depends(get_settings)):

    is_valid, result_signal = DataController().validate_uploaded_file(file=file)

    if not is_valid:
        return JSONResponse(
            status_code=ResponseConstants.BAD_REQUEST.value,
            content={"message": result_signal}
        )

    project_path = ProjectController().get_project_path(project_id=project_id)
    file_path = os.path.join(project_path, file.filename)

    async with aiofiles.open(file_path, "wb") as f:
        while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
            await f.write(chunk)

    return {
        "is_valid": is_valid,
        "signal": ResponseConstants.FILE_UPLOAD_SUCCESS.value
            }