from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_pagedown import PageDown
from config import config
from app.main import main as main_blueprint



bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()

def create_app(config_name):
    appl = Flask(__name__)
    appl.config.from_object(config[config_name])
    config[config_name].init_app(appl)
    appl.register_blueprint(main_blueprint)
    bootstrap.init_app(appl)
    mail.init_app(appl)
    moment.init_app(appl)
    db.init_app(appl)

    return appl


