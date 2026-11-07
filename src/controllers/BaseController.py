from helpers.config import get_settings , Settings
import os
import random
import string

class BaseController:
    def __init__(self):
        self.app_settings = get_settings()
        self.base_directory = os.path.dirname((os.path.dirname(__file__)))
        self.file_directory = os.path.join(self.base_directory, self.app_settings.UPLOAD_DIRECTORY)

    def generate_random_filename(self, length: int = 12) -> str:
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))