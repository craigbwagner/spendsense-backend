import psycopg2, psycopg2.extras
from flask import Blueprint, jsonify, request, g
from db_helpers import get_db_connection
from auth_middleware import token_required
import json

expenses_blueprint = Blueprint("expenses_blueprint", __name__)


@expenses_blueprint.route("/expenses")
@token_required
def expenses_index():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        user_id = g.user["id"]
        cursor.execute("SELECT * FROM expenses WHERE user_id = %s", (user_id,))
        expenses = cursor.fetchall()
        return jsonify(expenses)
    except Exception as e:
        return jsonify({"Error": str(e)}), 500
    finally:
        connection.close()


@expenses_blueprint.route("/expenses", methods=["POST"])
@token_required
def create_expense():
    try:
        expense_data = request.json
        expense_data["user_id"] = g.user["id"]
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(
            """
                        INSERT INTO expenses (name, amount, date, category, user_id)
                        VALUES (%s, %s,%s,%s,%s)
                        RETURNING *
                       """,
            (
                expense_data["name"],
                expense_data["amount"],
                expense_data["date"],
                expense_data["category"],
                expense_data["user_id"],
            ),
        )
        created_expense = cursor.fetchone()
        connection.commit()
        connection.close()
        return jsonify({"expense": created_expense}), 201
    except Exception as e:
        return jsonify({"Error": str(e)}), 400
