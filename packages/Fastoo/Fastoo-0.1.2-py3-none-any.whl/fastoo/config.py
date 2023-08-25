import os
from pydantic_settings import BaseSettings

base_path = os.path.dirname(os.path.abspath(__file__))

class DefaultSettings(BaseSettings):
    app_name: str = "Awesome API"
    admin_email: str = "admin@domain.com"
    items_per_user: int = 50

class DevelopmentSettings(DefaultSettings):
    pass 

class ProductionSettings(DefaultSettings):
    pass 

class TestingSettings(DefaultSettings):
    pass 


profiles = {
    "development": DevelopmentSettings,
    "production": ProductionSettings,
    "testing": TestingSettings
}