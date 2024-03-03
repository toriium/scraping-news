import os

from dotenv import find_dotenv, load_dotenv

env_path = find_dotenv('../env.env')
load_dotenv(env_path)

SPLASH_URL = 'http://localhost:8050/render.html'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGES_PATH = f"{BASE_DIR}/images/"


class DatabaseEnv:
    DB_HOST: str = os.getenv('DB_HOST')
    DB_USER: str = os.getenv('DB_USER')
    DB_PORT: str = os.getenv('DB_PORT')
    DB_NAME: str = os.getenv('DB_NAME')
    DB_PASSWORD: str = os.getenv('DB_PASSWORD')
