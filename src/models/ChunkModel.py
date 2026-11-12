from .BaseDataModel import BaseDataModel
from .db_schemes import data_chunk
from .enums.DataBaseEnum import DataBaseEnum
from bson.objectid import ObjectId
from pymongo import InsertOne

class ChunkModel(BaseDataModel):

    def __init__(self,mongodb_client:object):
            super().__init__(mongodb_client=mongodb_client)
            self.mongodb_client = mongodb_client 
            self.collection = self.mongodb_client[DataBaseEnum.COLLECTION_CHUNK_NAME.value]
    
    # static function to call instractor and call async function to create indexes
    @classmethod
    async def create_instance(cls,mongodb_client:object):
        instance = cls(mongodb_client)
        await instance.init_collection()
        return instance
    
    async def init_collection(self):
                all_collections = await self.mongodb_client.list_collection_names()
                if DataBaseEnum.COLLECTION_CHUNK_NAME.value not in all_collections:
                    self.collection = self.mongodb_client[DataBaseEnum.COLLECTION_CHUNK_NAME.value]
                    indexes = data_chunk.get_indexes()
                    for index in indexes:
                        await self.collection.create_index(
                            index["key"],
                            name=index["name"],
                            unique =index["unique"]
                        )
    
    async def create_chunk(self,chunk:data_chunk):
          result = await self.collection.insert_one(chunk.dict(by_alias=True, exclude_unset=True))
          chunk._id = result._id
          return chunk
    
    async def get_chunk(self, chunk_id:str):
          result = await self.collection.find_one({
                "_id": ObjectId(chunk_id)
          })

          if result is None:
                return None

          return data_chunk(**result)

    async def insert_many_chunks(self, chunks:list, batch_size:int =100):

         for i in range(0 , len(chunks),batch_size):
                        batch = chunks[i:i+batch_size]
        
                        operations = [
                              InsertOne(chunk.dict(by_alias=True, exclude_unset=True))
                              for chunk in chunks
                        ]
        
                        await self.collection.bulk_write(operations)
                        
                        return len(chunks)

    async def delete_chunks_by_project_id(self,project_id:str):
           result = await self.collection.delete_many({
                  "chunk_project_id" : project_id
           })
           
           return result.deleted_count