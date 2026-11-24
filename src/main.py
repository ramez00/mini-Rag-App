from fastapi import FastAPI
from routes import base, data , nlp
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
from stores.llm.LLMProviderFactory import LLMProviderFactory
from stores.vectorDb.VectorDBProviderFactory import VectorDBProviderFactory

app = FastAPI()

@app.on_event("startup")
async def startup_span():
    settings = get_settings()
    app.mongo_conn = AsyncIOMotorClient(settings.MONGO_URI)
    app.mongodb_client = app.mongo_conn[settings.MONGO_DB_NAME]

    llm_provider_factory = LLMProviderFactory(settings)
    vector_db_provider_factory = VectorDBProviderFactory(settings)

    # Generation Client
    app.generation_client = llm_provider_factory.create(provider = settings.GENERATION_BACKEND)
    app.generation_client.set_generation_model(model_id = settings.GENERATION_MODEL_ID)

    # embedding client
    app.embedding_client = llm_provider_factory.create(provider = settings.EMBEDDING_BACKEND)
    app.embedding_client.set_embedding_model(model_id = settings.EMBEDDING_MODEL_ID,
                                              embedding_size = settings.EMBEDDING_MODEL_SIZE)

    # Define Vector Db 
    app.vector_db_client = vector_db_provider_factory.create(
        provider = settings.VECTOR_DB_BACKEND
    )
    app.vector_db_client.connect()

@app.on_event("shutdown")
async def shutdown_span():
    app.mongo_conn.close()
    app.vector_db_client.disconnect()
    
app.include_router(base.base_router)
app.include_router(data.data_router)
app.include_router(nlp.nlp_router)
