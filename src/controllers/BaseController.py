from helpers.config import get_settings , Settings
import os
import random
import string

class BaseController:
    def __init__(self):
        self.app_settings = get_settings()
        self.base_directory = os.path.dirname((os.path.dirname(__file__)))
        self.file_directory = os.path.join(self.base_directory, self.app_settings.UPLOAD_DIRECTORY)

        self.database_dir = os.path.join(
            self.base_directory,
            "assets/database"
        )

    def generate_random_filename(self, length: int = 12) -> str:
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    def get_database_path(self, db_name:str):

        database_path = os.path.join(
            self.database_dir,
            db_name
        )

        if os.path.exists(database_path):
            os.makedirs(database_path)

        return database_path    
