import os

from .BaseController import BaseController
from .ProjectController import ProjectController
from fastapi import UploadFile
from models import ResponseConstants
import re

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

    def generate_unique_filename(self, original_filename: str, project_id: str) -> str:

        random_filename = self.generate_random_filename()
        project_path = ProjectController().get_project_path(project_id=project_id)

        clean_file_name = self.get_clean_filename(filename=original_filename)

        new_file_path = os.path.join(project_path, random_filename + "_" + clean_file_name)

        while os.path.exists(new_file_path):
            random_filename = self.generate_random_filename()
            new_file_path = os.path.join(project_path, random_filename + "_" + clean_file_name)
            
        return new_file_path


    def get_clean_filename(self, filename: str) -> str:
        # Remove any special characters except underscores and .
        clean_filename = re.sub(r"[^\w. ]", "", filename.strip())

        # Replace spaces with underscores
        clean_filename = clean_filename.replace(' ', '_')

        return clean_filename    