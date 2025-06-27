import os
from dotenv import load_dotenv

load_dotenv()

def get_env_variable(name: str) -> str:
    value = os.getenv(name)
    if value is None or value == "":
        raise ValueError("Please set an environment variable")
    return value

# Variáveis carregadas e validadas
BASE_URL = get_env_variable("BASE_URL")
MONGO_URI = get_env_variable("MONGO_URI")