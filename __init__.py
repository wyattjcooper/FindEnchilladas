from flask import Flask
from flask.ext.login import LoginManager

FindFood = Flask(__name__)
FindFood.config.from_object('FindFood.config.Config')

login_manager=LoginManager()
login_manager.init_app(FindFood)

import views
