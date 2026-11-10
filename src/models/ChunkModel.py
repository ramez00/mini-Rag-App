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

    async def create_chunk(self,chunk:data_chunk):
          result = await self.collection.insert_one(chunk.dict())
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
                              InsertOne(chunk.dict())
                              for chunk in chunks
                        ]
        
                        await self.collection.bulk_write(operations)
                        
                        return len(chunks)

