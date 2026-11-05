from .BaseController import BaseController

class DataController(BaseController):
    def __init__(self):
        super().__init__()

    def validate_uploaded_file(self, file):

        if not file:
            return False, "No file provided"

        if file.content_type not in self.app_settings.FILE_ALLOWED_EXTENSIONS:
            return False, "Invalid content type."

        if file.size > self.app_settings.FILE_MAX_SIZE:
            return False, "File size exceeds the maximum limit."    

        return True,"File Uploaded successfully"