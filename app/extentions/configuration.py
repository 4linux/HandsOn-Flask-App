from dynaconf import FlaskDynaconf


def init_app(app):
    conf = FlaskDynaconf(app)
    return conf
