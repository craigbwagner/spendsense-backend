import psycopg2, psycopg2.extras
from flask import Blueprint, jsonify, request, g
from db_helpers import get_db_connection
from auth_middleware import token_required

settings_blueprint = Blueprint("settings_blueprint", __name__)


def create_settings(user_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        monthly_income = 0
        monthly_budget = 0
        weekly_budget = 0
        savings_goal = 0
        cursor.execute(
            """
                            INSERT INTO settings (monthly_income, monthly_budget, weekly_budget, savings_goal, user_id)
                            VALUES (%s, %s,%s,%s,%s)
                            RETURNING *
                        """,
            (
                monthly_income,
                monthly_budget,
                weekly_budget,
                savings_goal,
                (user_id,),
            ),
        )
        created_settings = cursor.fetchone()
        connection.commit()
        connection.close()
        return jsonify({"expense": created_settings}), 201
    except Exception as e:
        return jsonify({"Error": str(e)}), 400


@settings_blueprint.route("/settings", methods=["PUT"])
@token_required
def update_settings():
    try:
        updated_settings_data = request.json
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        user_id = g.user["id"]
        cursor.execute("SELECT * FROM settings WHERE user_id = %s", (user_id,))
        settings_to_update = cursor.fetchone()
        if settings_to_update is None:
            return jsonify({"error": "User settings not found"}), 404
        connection.commit()
        if settings_to_update["user_id"] is not user_id:
            return ({"error": "Unauthorized"}), 401
        cursor.execute(
            """
                UPDATE settings SET monthly_income = %s, monthly_budget = %s, weekly_budget = %s, savings_goal = %s WHERE user_id = %s RETURNING *
            """,
            (
                updated_settings_data["monthly_income"],
                updated_settings_data["monthly_budget"],
                updated_settings_data["weekly_budget"],
                updated_settings_data["savings_goal"],
                user_id,
            ),
        )
        updated_settings = cursor.fetchone()
        print(updated_settings)
        connection.commit()
        connection.close()
        return jsonify({"settings": updated_settings}), 200
    except Exception as e:
        return jsonify({"Error": str(e)}), 400
