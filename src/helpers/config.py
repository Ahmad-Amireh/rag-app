from pydantic_settings import BaseSettings , SettingsConfigDict
class Settings(BaseSettings):

    APP_NAME : str 
    APP_VERSION : str 

    class Config:  # or model_config = SettingsConfigDict(env_file=".env")
        env_file = ".env"

def get_settings ():
    return Settings()