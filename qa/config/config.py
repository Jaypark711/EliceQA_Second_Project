from data.user_data import VALID_USER

TIMEOUT = 10
BASE_URL = "http://119.59.0.44:8080/"
SIGNIN_URL = f"{BASE_URL}login"
SIGNUP_URL = f"{BASE_URL}register"
SETTINGS_URL = f"{BASE_URL}settings"
MY_PROFILE_URL = f"{BASE_URL}@{VALID_USER['username']}"
FAVORITED_ARTICLES_URL = f"{MY_PROFILE_URL}/favorites"
