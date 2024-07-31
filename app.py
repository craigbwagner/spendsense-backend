from flask import Flask, request, jsonify, g, Blueprint
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

def get_db_connection():
    connection = psycopg2.connect(
        host="localhost",
        database="flask_auth_db",
        user=os.getenv("POSTGRES_USERNAME"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )
    return connection

app.run()
