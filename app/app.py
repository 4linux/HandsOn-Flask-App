from flask import Flask
from .routes.usuario import usuario
from .routes.produto import produto
from .commands.userCommands import userCommands
from .extentions import database


def create_app(config_object="app.settings"):
    app = Flask(__name__)
    app.config.from_object(config_object)
    database.init_app(app)
    
    app.register_blueprint(usuario)
    app.register_blueprint(produto)
    app.register_blueprint(userCommands)
    
    return app
