import psycopg2, psycopg2.extras
from flask import Blueprint, jsonify, request
from db_helpers import get_db_connection

expenses_blueprint = Blueprint("expenses_blueprint", __name__)


@expenses_blueprint.route("/expenses")
def expenses_index():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute("SELECT * FROM expenses")
        expenses = cursor.fetchall()
        return jsonify(expenses)
    except Exception as e:
        return jsonify({"Error": str(e)}), 500
    finally:
        connection.close()
