from flask import Flask
from dotenv import load_dotenv
import os
import os
import jwt
import bcrypt
import psycopg2, psycopg2.extras
from flask_cors import CORS
from auth_blueprint import authentication_blueprint


load_dotenv()

app = Flask(__name__)
app.register_blueprint(authentication_blueprint)

app.run()
