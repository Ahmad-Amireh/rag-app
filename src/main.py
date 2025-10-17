from fastapi import FastAPI
from routes import base, data
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings

app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    settings = get_settings()
    app.mongo_client = AsyncIOMotorClient(settings.MONGODB_URL)
    app.db = app.mongo_client[settings.MONGODB_DATABASE]

@app.on_event("shutdown")  # Changed from "startup" to "shutdown"
async def shutdown_db_client():
    app.mongo_client.close()


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
