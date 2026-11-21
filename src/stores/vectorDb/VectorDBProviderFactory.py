from .providers import QdrantDB
from .VectorDBEnums import VectorDBEnums
from controllers.BaseController import BaseController

class VectorDBProviderFactory():
    def __init__(self,config):
        self.config = config
        self.base_controller = self.base_controller()


    def create(self, provider: str):
        if provider == VectorDBEnums.QDRANT.value:
            db_path = self.base_controller.get_database_path(self.config.VECTOR_DB_PATH)
            return QdrantDB(
                db_path = db_path,
                distance_method = None
            )
