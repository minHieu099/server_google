from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    from .routes import main
    from .services import service
    app.register_blueprint(main)
    app.register_blueprint(service)
    
    return app
