from flask import Flask, render_template
from app.platform.routes import platform as platform_module

app = Flask(__name__)

app.config.from_object('config')

app.register_blueprint(platform_module)