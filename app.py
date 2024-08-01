from flask import Flask
from dotenv import load_dotenv
import os
import jwt
import bcrypt
import psycopg2, psycopg2.extras
from flask_cors import CORS
from src.blueprints.auth_blueprint import authentication_blueprint
from src.blueprints.expenses_blueprint import expenses_blueprint
from src.blueprints.settings_blueprint import settings_blueprint
from src.blueprints.category_budgets_blueprint import category_budgets_blueprint


load_dotenv()

app = Flask(__name__)
app.register_blueprint(authentication_blueprint)
app.register_blueprint(expenses_blueprint)
app.register_blueprint(settings_blueprint)
app.register_blueprint(category_budgets_blueprint)

app.run()
