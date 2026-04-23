import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    BASE_URL = "https://lmsk.wyb.ac.lk"
    LOGIN_URL = f"{BASE_URL}/login/index.php"
    DASHBOARD_URL = f"{BASE_URL}/my/"
    CALENDAR_EXPORT_URL = f"{BASE_URL}/calendar/export.php"
    NOTIFICATIONS_URL = f"{BASE_URL}/message/output/popup/notifications.php"

    LMS_USERNAME = os.getenv("LMS_USERNAME", "").strip()
    LMS_PASSWORD = os.getenv("LMS_PASSWORD", "").strip()

    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

    DATA_DIR = "Data"
    DATA_FILE = f"{DATA_DIR}/data.json"
    CALENDAR_FILE = f"{DATA_DIR}/calendar.ics"

    # API Configuration
    API_URL = os.getenv("API_URL", "http://127.0.0.1:5000")
    API_ENABLED = os.getenv("API_ENABLED", "true").lower() == "true"
