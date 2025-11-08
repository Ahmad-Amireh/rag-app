from pydantic_settings import BaseSettings , SettingsConfigDict
class Settings(BaseSettings):

    APP_NAME : str 
    APP_VERSION : str 
    FILE_ALLOWED_TYPES: list
    FILE_MAX_SIZE: int
    FILE_DEFAULT_CHUNK_SIZE: int
    MONGODB_URL: str
    MONGODB_DATABASE: str
    GENERATION_BACKEND: str
    EMBEDDING_BACKEND: str

    OPEN_API_KEY:str =None
    OPEN_API_URL:str = None
    COHERE_API_KEY:str = None

    GENERATION_MODEL_ID: str = None
    EMBEDDING_MODEL_ID:str = None
    EMBEDDING_MODEL_SIZE:int = None

    default_input_max_characters:int = None
    default_generation_max_output_token:int = None
    default_generation_temperature:float = None

    
    VECTOR_DB_BACKEND: str
    VECTOR_DB_PATH: str 
    VECTOR_DB_DISTANCE_METHOD: str = None

    DEFAULT_LANG: str = "en"
    PRIMARY_LANG: str = "en"


    class Config:  # or model_config = SettingsConfigDict(env_file=".env")
        env_file = ".env"

def get_settings ():
    return Settings()