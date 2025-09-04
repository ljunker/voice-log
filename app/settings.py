import os


class Settings:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev")
    UPLOAD_DIR = os.environ.get("UPLOAD_DIR", os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "uploads")))
    MAX_CONTENT_LENGTH = int(os.environ.get("MAX_CONTENT_LENGTH", 100 * 1024 * 1024))  # 100MB

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///voice_logs.db")

    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    OPENAI_TRANSCRIBE_MODEL = os.environ.get("OPENAI_TRANSCRIBE_MODEL", "gpt-4o-transcribe")
    OPENAI_TEXT_MODEL = os.environ.get("OPENAI_TEXT_MODEL", "gpt-4o-mini")


settings = Settings()
