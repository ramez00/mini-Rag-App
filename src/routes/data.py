import os
import aiofiles
from fastapi import APIRouter, Depends, UploadFile , Request
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings
from controllers import DataController, ProjectController , ProcessController
from models import ResponseConstants
import logging
from .schemes.data import ProcessRequest
from models.ProjectModel import ProjectModel

logger = logging.getLogger("uvicorn.error")

data_router = APIRouter(
    prefix="/api/data",
    tags=["api_v1", "data"],
)

@data_router.post("/upload/{project_id}")
async def upload_data(request:Request,project_id: str, file: UploadFile,
                      app_settings: Settings = Depends(get_settings)):

    project_model = ProjectModel(mongodb_client=request.app.mongodb_client)

    project = await project_model.get_project_or_create_one(project_id=project_id)

    data_controller = DataController()

    is_valid, result_signal = data_controller.validate_uploaded_file(file=file)

    if not is_valid:
        return JSONResponse(
            status_code=ResponseConstants.BAD_REQUEST.value,
            content={"message": result_signal}
        )

    project_path = ProjectController().get_project_path(project_id=project_id)
    file_path, file_id = data_controller.generate_unique_filename_fileId(original_filename=file.filename, project_id=project_id)

    try:
        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e:
       logger.error(f"Error occurred while saving the file: {e}")
       return JSONResponse(
                   status_code=ResponseConstants.BAD_REQUEST.value,
                   content={
                       "message": ResponseConstants.FILE_UPLOAD_FAILED.value
                    }
        )

    return {
        "is_valid": is_valid,
        "signal": ResponseConstants.FILE_UPLOAD_SUCCESS.value,
        "file_id": file_id,
        "project_id":str(project._id)
    }

@data_router.post("/process/{project_id}")
async def process_endpoint(project_id: str, request: ProcessRequest):

    file_id = request.file_id
    process_controller = ProcessController(project_id=project_id)
    file_content = process_controller.get_file_content(file_id=file_id)
    chunk_size = request.chunk_size
    chunk_overlap = request.overlap_size

    file_chunks = process_controller.process_file_content(
        file_content=file_content,
        file_id=file_id,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    if file_chunks is None or len(file_chunks) == 0:
        return JSONResponse(
            status_code=ResponseConstants.BAD_REQUEST.value,
            content={"message": ResponseConstants.FILE_PROCESSING_FAILED.value}
        )

    return file_chunks