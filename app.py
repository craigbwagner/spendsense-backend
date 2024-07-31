from flask import Flask, request, jsonify, g
from dotenv import load_dotenv
import os
import os
import jwt
import psycopg2, psycopg2.extras
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)


def get_db_connection():
    connection = psycopg2.connect(
        host="localhost",
        database="flask_auth_db",
        user=os.getenv("POSTGRES_USERNAME"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )
    return connection

app.run()
