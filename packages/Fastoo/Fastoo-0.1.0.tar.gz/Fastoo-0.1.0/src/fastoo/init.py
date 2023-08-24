from config import profiles 
from functools import lru_cache

settings = profiles["development"]()

@lru_cache()
def get_settings():
    return settings