from fastapi import FastAPI
from routes import base, data, nlp
from helpers.config import get_settings
from stores.llm.LLMFactory import LLMProviderFactory
app = FastAPI()
from stores.vectordb.VectorDBProviderFactory import VectorDBProviderFactory
from stores.llm.templates import TemplateParser
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

@app.on_event("startup")
async def startup_span():
    settings = get_settings()
    postgres_conn = f"postgresql+asyncpg://{settings.POSTGERS_USERNAME}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DATABASE}" 
    app.db_engine = create_async_engine(postgres_conn)
    app.db_client = sessionmaker(app.db_engine,class_= AsyncSession, expire_on_commit= False)


    llm_provider_factory = LLMProviderFactory(settings)
    vectodb_provider_factory = VectorDBProviderFactory(settings)

    # generation client
    app.generation_client = llm_provider_factory.create(provider=settings.GENERATION_BACKEND)
    app.generation_client.set_generation_model(model_id = settings.GENERATION_MODEL_ID)

    # embdedding client 
    app.embedding_client = llm_provider_factory.create(provider=settings.EMBEDDING_BACKEND)
    app.embedding_client.set_embedding_model(embedding_model_id = settings.EMBEDDING_MODEL_ID, embedding_size=settings.EMBEDDING_MODEL_SIZE)

    # vectordb client 
    app.vectordb_client = vectodb_provider_factory.create(
        provider = settings.VECTOR_DB_BACKEND
    )
    app.vectordb_client.connect()

    app.template_parser= TemplateParser(
        language = settings.PRIMARY_LANG,
        default_language = settings.DEFAULT_LANG
    )


@app.on_event("shutdown")  # Changed from "startup" to "shutdown"
async def shutdown_span():
    app.db_engine.dispose()
    app.vectordb_client.disconnect()


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Startup
#     settings = get_settings()
#     app.mongo_client = AsyncIOMotorClient(settings.MONGODB_URL)
#     app.db = app.mongo_client[settings.MONGODB_DATABASE]
#     yield
#     # Shutdown
#     app.mongo_client.close()

# app = FastAPI(lifespan=lifespan)



app.include_router(base.base_router)
app.include_router(data.data_router)
app.include_router(nlp.nlp_router)
