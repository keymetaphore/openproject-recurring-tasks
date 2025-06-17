import os
from dotenv import load_dotenv

load_dotenv()

OIDC_ENABLED = os.getenv("OIDC_ENABLED", "false").lower() == "true"
SECRET_KEY = os.getenv("SECRET_KEY", "")
OIDC_CLIENT_ID = os.getenv("OIDC_CLIENT_ID", "")
OIDC_CLIENT_SECRET = os.getenv("OIDC_CLIENT_SECRET", "")
OIDC_ISSUER_URL = os.getenv("OIDC_ISSUER_URL", "")
OIDC_REDIRECT_URI = os.getenv("OIDC_REDIRECT_URI", "")
API_TOKEN = os.getenv("OPENPROJECT_API_TOKEN")
BASE_URL = os.getenv("OPENPROJECT_BASE_URL")
APP_NAME = os.getenv("APP_NAME", "OpenProject Task Manager")
APP_LOGO_URL = os.getenv("APP_LOGO_URL", "")
DB_PATH = "/data/recurring.db"
