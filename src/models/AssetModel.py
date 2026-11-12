from .BaseDataModel import BaseDataModel
from .db_schemes import Assets
from .enums.DataBaseEnum import DataBaseEnum
from bson import ObjectId

class AssetModel(BaseDataModel):

     def __init__(self,mongodb_client:object):
        super().__init__(mongodb_client=mongodb_client)
        self.mongodb_client = mongodb_client 
        self.collection = self.mongodb_client[DataBaseEnum.COLLECTION_ASSET_NAME.value]

@classmethod
async def create_instance(cls,mongodb_client:object):
    instance = cls(mongodb_client)
    await instance.init_collection()
    return instance 

async def init_collection(self):
        all_collections = await self.mongodb_client.list_collection_names()
        if DataBaseEnum.COLLECTION_ASSET_NAME.value not in all_collections:
            self.collection = self.mongodb_client[DataBaseEnum.COLLECTION_ASSET_NAME.value]
            indexes = Assets.get_indexes()
            for index in indexes:
                await self.collection.create_index(
                    index["key"],
                    name=index["name"],
                    unique =index["unique"]
                )

async def create_asset(self, asset: Assets):

    result = await self.collection().insert_one(asset.dict(by_alias=True,exclude_unset=True))
    asset._id = result.inserted_id
    return result

async def get_all_project_assets(self, asset_project_id):

    return await self.collection.find({
          "asset_project_id": ObjectId(asset_project_id) if isinstance(asset_project_id,str) else asset_project_id
    }).to_list(length=None)
     