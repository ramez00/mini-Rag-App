from fastapi import FastAPI , APIRouter , Depends , UploadFile , File
from fastapi.responses import JSONResponse
from helpers.config import get_settings , Settings
from controllers import DataController
from models import ResponseConstants

base_router = APIRouter(
    prefix="/api/data",
    tags=["api_v1","data"],
)

@base_router.get("/upload/{project_id}")
async def upload_data(project_id: str, file: UploadFile,
                        settings: Settings = Depends(get_settings)):

   is_valid, result_signal = DataController().validate_uploaded_file(file=file)

   if not is_valid:
        return JSONResponse(
            status_code=ResponseConstants.BAD_REQUEST.value,
            content={
                "message": result_signal
                }
            )


   return {
        "is_valid": is_valid,
         "signal": result_signal
    }
