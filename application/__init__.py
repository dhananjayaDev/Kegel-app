"""Flask application factory."""

from flask import Flask

from application.config import Config
from application.providers import ProviderRegistry
from application.routes.main import main_bp
from application.routes.questionnaire import questionnaire_bp


def create_app(config_class: type = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

    registry = ProviderRegistry(app.config)
    app.extensions["providers"] = registry

    app.register_blueprint(main_bp)
    app.register_blueprint(questionnaire_bp, url_prefix="/assessment")

    return app
