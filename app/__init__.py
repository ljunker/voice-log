from flask import Flask
from .settings import settings
from .routes import bp


def create_app():
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=settings.SECRET_KEY,
        UPLOAD_DIR=settings.UPLOAD_DIR,
        MAX_CONTENT_LENGTH=settings.MAX_CONTENT_LENGTH,
        SQLALCHEMY_DATABASE_URI=settings.SQLALCHEMY_DATABASE_URI,
    )

    app.register_blueprint(bp)

    from .models import Base
    from .db import engine
    with app.app_context():
        Base.metadata.create_all(bind=engine)

    return app
