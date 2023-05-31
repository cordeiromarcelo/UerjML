from flask import Flask
from app.routes import platform as platform_module
from app.routes.index import index_bp as index_module
from app.routes.preprocess import preprocess_bp as preprocess_module
from app.routes.train import train_bp as train_module
from app.routes.evaluate import evaluate_bp as evaluate_module

app = Flask(__name__)

app.config.from_object('config')

app.register_blueprint(platform_module)
app.register_blueprint(index_module)
app.register_blueprint(preprocess_module)
app.register_blueprint(train_module)
app.register_blueprint(evaluate_module)