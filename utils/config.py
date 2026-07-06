import os
from functools import lru_cache

try:
    from dotenv import load_dotenv

    load_dotenv()
except Exception:
    pass


@lru_cache
def get_gemini_api_key() -> str:
    return os.getenv("GEMINI_API_KEY", "").strip()


def has_gemini_key() -> bool:
    return bool(get_gemini_api_key())


def app_mode() -> str:
    return os.getenv("APP_ENV", "development")


def use_vertex_ai() -> bool:
    return os.getenv("USE_VERTEX_AI", "false").strip().lower() in {"1", "true", "yes"}


def gcp_project_id() -> str:
    return os.getenv("GCP_PROJECT_ID", "").strip()


def gcp_location() -> str:
    return os.getenv("GCP_LOCATION", "asia-south1").strip()
