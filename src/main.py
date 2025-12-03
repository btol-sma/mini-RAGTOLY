from fastapi import FastAPI 

from routes import base, data
from motor.motor_asyncio import AsyncIOMotorClient
from helper.config import get_settings
from stores.llm.LLMProviderFactory import LLMProviderFactory

app = FastAPI()
async def startup_db_client():
    setting = get_settings()
    app.mongo_conn = AsyncIOMotorClient(setting.MONGODB_URL)
    app.db_client = app.mongo_conn[setting.MONGODB_DATABASE]

    llm_provider_factory = LLMProviderFactory(setting)
    app.generation_client = llm_provider_factory.create( provider= setting.GENERATION_BACKEND )
    app.generation_client.set_generation_model(model_id= setting.GENERATION_MODEL_ID)

    app.client_embedding = llm_provider_factory.create( provider= setting.EMBEDDING_BACKEND)
    app.client_embedding.set_embedding_model(model_id=setting.EMBEDDING_MODEL_ID , embedding_size= setting.EMBEDDING_MODEL_SIZE)

async def shutdown_db_client():
    app.mongo_conn.close()

app.router.lifespan.on_startup.append(startup_db_client)
app.router.lifespan.on_shutdown.append(shutdown_db_client)
app.include_router(base.baseRouter)
app.include_router(data.dataRouter)