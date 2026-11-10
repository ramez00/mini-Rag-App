from helpers.config import get_settings, Settings


class BaseDataModel:
    def __init__(self,mongodb_client:object):
        self.db_client = mongodb_client
        self.app_settings = get_settings()
        


