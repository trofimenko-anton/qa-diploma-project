import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://ru.yougile.com")
API_URL = f"{BASE_URL}/api-v2"
LOGIN = os.getenv("YOUGILE_LOGIN")
PASSWORD = os.getenv("YOUGILE_PASSWORD")
TOKEN = os.getenv("YOUGILE_TOKEN", "")
BROWSER = os.getenv("BROWSER", "chrome")
