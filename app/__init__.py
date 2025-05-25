from flask import Flask
from app.config import Config
from app.database import db
from app.routes.user_routes import user_blueprint
from app.routes.product_routes import product_blueprint

def create_app():
    #app = Flask(__name__)


    # app.register_blueprint(user_blueprint)
    # app.register_blueprint(product_blueprint)


    from flask import Flask
    from flasgger import Swagger
    from app.routes.user_routes import user_blueprint
    from app.routes.product_routes import product_blueprint

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    swagger = Swagger(app)

    # Подключение роутов
    app.register_blueprint(user_blueprint, url_prefix='/users')
    app.register_blueprint(product_blueprint, url_prefix='/products')
    return app
