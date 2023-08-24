from flask import Flask


def init_app(app: Flask):
    from .base import init_models
    init_models(app)
    from .base import engine
    from .models import init_db
    init_db(engine)

