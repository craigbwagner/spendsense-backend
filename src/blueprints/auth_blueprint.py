import os
import jwt
import bcrypt
import psycopg2, psycopg2.extras
from flask import Blueprint, jsonify, request
from src.services.db_helpers import get_db_connection
from src.blueprints.settings_blueprint import create_settings
from src.blueprints.category_budgets_blueprint import create_category_budgets

authentication_blueprint = Blueprint("authentication_blueprint", __name__)


@authentication_blueprint.route("/auth/signup", methods=["POST"])
def signup():
    try:
        new_user_data = request.get_json()
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(
            "SELECT * FROM users WHERE username = %s;", (new_user_data["username"],)
        )
        existing_user = cursor.fetchone()
        if existing_user:
            cursor.close()
            return jsonify({"error": "Username already taken"}), 400
        hashed_password = bcrypt.hashpw(
            bytes(new_user_data["password"], "utf-8"), bcrypt.gensalt()
        )
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s) RETURNING id, username",
            (new_user_data["username"], hashed_password.decode("utf-8")),
        )
        created_user = cursor.fetchone()
        connection.commit()
        token = jwt.encode(created_user, os.getenv("JWT_SECRET"))
        created_user_id = dict(created_user)["id"]
        create_settings(created_user_id)
        create_category_budgets(created_user_id)
        return jsonify({"token": token, "user": created_user}), 201
    except Exception as error:
        return jsonify({"error": str(error)}), 401
    finally:
        connection.close()


@authentication_blueprint.route("/auth/signin", methods=["POST"])
def signin():
    try:
        sign_in_form_data = request.get_json()
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(
            "SELECT * FROM users WHERE username = %s;", (sign_in_form_data["username"],)
        )
        existing_user = cursor.fetchone()
        if existing_user is None:
            return jsonify({"error": "Invalid username or password"}), 401
        password_is_valid = bcrypt.checkpw(
            bytes(sign_in_form_data["password"], "utf-8"),
            bytes(existing_user["password"], "utf-8"),
        )
        if not password_is_valid:
            return jsonify({"error": "Invalid username or password"}), 401
        token = jwt.encode(
            {"username": existing_user["username"], "id": existing_user["id"]},
            os.getenv("JWT_SECRET"),
        )
        return jsonify({"token": token}), 201
    except Exception as error:
        return jsonify({"error": "Invalid username or password"}), 401
    finally:
        connection.close()
