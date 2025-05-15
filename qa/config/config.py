from data.user_data import VALID_USER
from dotenv import load_dotenv
import os
load_dotenv(dotenv_path='config/.env')
HOST=os.getenv("DB_HOST")

TIMEOUT = 10
BASE_URL = f"http://{HOST}:4100/"
SIGNIN_URL = f"{BASE_URL}login"
SIGNUP_URL = f"{BASE_URL}register"
SETTINGS_URL = f"{BASE_URL}settings"
MY_PROFILE_URL = f"{BASE_URL}@{VALID_USER['username']}"
FAVORITED_ARTICLES_URL = f"{MY_PROFILE_URL}/favorites"
