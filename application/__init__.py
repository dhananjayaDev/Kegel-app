"""Flask application factory."""

from flask import Flask, request, session

from application.config import Config
from application.services.download_links import resolve_download_links
from application.services.llm_status import llm_status
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

    @app.context_processor
    def _inject_site_context() -> dict:
        if request.args.get("llm_limited") == "1":
            session["llm_limit_notice"] = True
        links = resolve_download_links(app.config)
        return {
            "desktop_app_url": links["desktop_app_url"],
            "mobile_app_url": links["mobile_app_url"],
            "desktop_download_available": links["desktop_download_available"],
            "mobile_download_available": links["mobile_download_available"],
            "mobile_download_message": links["mobile_download_message"],
            "llm_limit_notice": session.get("llm_limit_notice", False),
            "has_saved_assessment": bool(session.get("assessment")),
            "app_deployment": app.config.get("APP_DEPLOYMENT", "web"),
            "llm_status": llm_status(app.config),
            "show_llm_settings": app.config.get("APP_DEPLOYMENT", "web") in ("desktop", "android"),
        }

    app.register_blueprint(main_bp)
    app.register_blueprint(questionnaire_bp, url_prefix="/assessment")

    return app
