from flask import Flask

from flask_migrate import Migrate


from .views import healthcheck_blueprint, user_blueprint, category_blueprint, record_blueprint, currency_blueprint

from my_app.db import db


def create_app():
    app = Flask(__name__)

    app.config.from_pyfile('config.py', silent=True)
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:3228@localhost:5432/mydb'

    # db = SQLAlchemy(app)
    db.init_app(app)
    migrate = Migrate(app, db)

    # app.app_context().push()

    with app.app_context():
        db.create_all()

    app.register_blueprint(healthcheck_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(category_blueprint)
    app.register_blueprint(record_blueprint)
    app.register_blueprint(currency_blueprint)

    return app
