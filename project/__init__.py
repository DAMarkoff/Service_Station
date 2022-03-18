from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from psycopg2.errors import DatabaseError

from project.config import Config
from loguru import logger

logger.add("logger.log")

mail = Mail()
db = SQLAlchemy()
login_manager = LoginManager()

# TODO Move config to object


def create_app(config_filename=None):
    app = Flask(__name__, static_folder='static', template_folder='templates', instance_relative_config=True)
    # app.config.from_object(Config)
    app.config.from_pyfile(config_filename)
    print(f'using config: {config_filename}')
    initialize_extensions(app)
    register_blueprints(app)
    return app


def initialize_extensions(app):
    db.init_app(app)
    Bootstrap(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    mail.init_app(app)
    
    from project.models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        try:
            user = User.query.get(int(user_id))
        except DatabaseError:
            logger.error(f'DB error during load_user')
            db.session.rollback()
            return None
        else:
            return user
    

def register_blueprints(app):
    from project.auth import auth as auth_blueprint
    from project.main import main as main_blueprint
    from project.profile import profile as profile_blueprint
    from project.errors import errors as errors_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(profile_blueprint, url_prefix='/profile')
    app.register_blueprint(errors_blueprint, url_prefix='/')
    