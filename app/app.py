from flask import Flask
from app.config.config import get_config_by_name
from app.initialize_functions import (
    initialize_route,
    initialize_db,
    initialize_auth,
    start_scheduler,
)


def create_app(config=None) -> Flask:
    """
    Create a Flask application.

    Args:
        config: The configuration object to use.

    Returns:
        A Flask application instance.
    """
    app = Flask(__name__)
    if config:
        app.config.from_object(get_config_by_name(config))

    start_scheduler(app)

    # Initialize extensions
    initialize_db(app)

    initialize_auth(app)

    # Register blueprints
    initialize_route(app)

    return app
