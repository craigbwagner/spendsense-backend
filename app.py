from flask import Flask
from dotenv import load_dotenv
import os

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
