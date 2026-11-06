from helpers.config import get_settings , Settings
import os

class BaseController:
    def __init__(self):
        self.app_settings = get_settings()
        self.base_directory = os.path.dirname((os.path.dirname(__file__)))
        self.file_directory = os.path.join(self.base_directory, self.app_settings.UPLOAD_DIRECTORY)