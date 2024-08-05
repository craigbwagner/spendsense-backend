import psycopg2, psycopg2.extras
from flask import Blueprint, jsonify, request, g
from src.services.db_helpers import get_db_connection
from src.middleware.auth_middleware import token_required
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
        return jsonify(created_expense), 201
    except Exception as e:
        return jsonify({"Error": str(e)}), 500


@expenses_blueprint.route("/expenses/<expense_id>")
@token_required
def show_expense(expense_id):
    try:
        user_id = g.user["id"]
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(
            """
            SELECT * FROM expenses WHERE id = %s AND user_id = %s;
            """,
            (expense_id, user_id),
        )

        expense = cursor.fetchone()
        if expense is not None:
            connection.close()
            return jsonify({"expense": expense}), 200
        else:
            connection.close()
        return jsonify({"Error": "expense not found"}), 404

    except Exception as e:
        return jsonify({"Error": str(e)}), 500


@expenses_blueprint.route("/expenses/<expense_id>", methods=["DELETE"])
@token_required
def delete_expense(expense_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(
            """
            SELECT * FROM expenses WHERE id = %s;
            """,
            (expense_id,),
        )
        expense_to_delete = cursor.fetchone()
        if expense_to_delete is None:
            return jsonify({"error": "expense not found"})
        connection.commit()
        if expense_to_delete["user_id"] is not g.user["id"]:
            return jsonify({"error": "Unauthorized"})

        cursor.execute(
            "DELETE FROM expenses WHERE id = %s;",
            (expense_id,),
        )
        connection.commit()
        connection.close()
        return jsonify({"message": "expense deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@expenses_blueprint.route("/expenses/<expense_id>", methods=["PUT"])
@token_required
def update_expense(expense_id):
    try:
        expense_data = request.json
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute("SELECT * FROM expenses WHERE id = %s", (expense_id,))
        expense_to_update = cursor.fetchone()
        if expense_to_update is None:
            return jsonify({"error": "expense not found"}), 404
        connection.commit()
        if expense_to_update["user_id"] is not g.user["id"]:
            return jsonify({"error": "Unauthorized"})
        cursor.execute(
            "UPDATE expenses SET name = %s, date = %s, amount = %s, category = %s WHERE id = %s RETURNING *",
            (
                expense_data["name"],
                expense_data["date"],
                expense_data["amount"],
                expense_data["category"],
                expense_id,
            ),
        )
        updated_expense = cursor.fetchone()
        connection.commit()
        connection.close()
        return jsonify(updated_expense), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
