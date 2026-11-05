from .BaseController import BaseController
from fastapi import UploadFile
from models import ResponseConstants

class DataController(BaseController):
    def __init__(self):
        super().__init__()

    def validate_uploaded_file(self, file):

        if file is None or not file.filename:
            return False, ResponseConstants.FILE_NOT_FOUND.value

        if file.content_type not in self.app_settings.FILE_ALLOWED_EXTENSIONS:
            return False, ResponseConstants.FILE_INVALID_CONTENT_TYPE.value

        if file.size > self.app_settings.FILE_MAX_SIZE:
            return False, ResponseConstants.FILE_SIZE_EXCEEDED.value    

        return True, ResponseConstants.FILE_UPLOAD_SUCCESS.value