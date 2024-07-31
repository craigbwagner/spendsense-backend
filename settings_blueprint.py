import psycopg2, psycopg2.extras
from flask import Blueprint, jsonify, request, g
from db_helpers import get_db_connection
from auth_middleware import token_required

settings_blueprint = Blueprint("settings_blueprint", __name__)


@settings_blueprint.route("/settings", methods=["POST"])
@token_required
def create_settings():
    try:
        settings_data = request.json
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        user_id = g.user["id"]
        cursor.execute(
            """
                            INSERT INTO settings (monthly_income, monthly_budget, weekly_budget, savings_goal, user_id)
                            VALUES (%s, %s,%s,%s,%s)
                            RETURNING *
                        """,
            (
                settings_data["monthly_income"],
                settings_data["monthly_budget"],
                settings_data["weekly_budget"],
                settings_data["savings_goal"],
                (user_id,),
            ),
        )
        created_expense = cursor.fetchone()
        connection.commit()
        connection.close()
        return jsonify({"expense": created_expense}), 201
    except Exception as e:
        return jsonify({"Error": str(e)}), 400
