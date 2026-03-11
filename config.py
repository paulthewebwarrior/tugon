import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


class Config:
    """Production configuration."""

    SECRET_KEY = os.environ.get("SECRET_KEY") or os.urandom(32)

    # Disable debug mode
    DEBUG = False
    TESTING = False

    # Cache configuration
    CACHE_TYPE = "simple"
    CACHE_DEFAULT_TIMEOUT = 300

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "postgresql+psycopg2://postgres:postgres@localhost:5432/tugon"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Static files
    SEND_FILE_MAX_AGE_DEFAULT = 31536000  # 1 year

    # Security headers
    X_FRAME_OPTIONS = "SAMEORIGIN"
    X_CONTENT_TYPE_OPTIONS = "nosniff"
    X_XSS_PROTECTION = "1; mode=block"

    # Session
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    # Gzip compression
    COMPRESS_MIMETYPES = [
        "text/html",
        "text/css",
        "text/javascript",
        "application/json",
        "application/javascript",
    ]
    COMPRESS_LEVEL = 6
    COMPRESS_MIN_SIZE = 500


class DevelopmentConfig(Config):
    """Development configuration."""

    DEBUG = True
    SECRET_KEY = "nagkakaisang-tugon-dev-secret"


class ProductionConfig(Config):
    """Production configuration with stricter settings."""

    pass


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
