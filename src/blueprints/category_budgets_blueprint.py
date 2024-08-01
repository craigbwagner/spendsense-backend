import psycopg2, psycopg2.extras
from flask import Blueprint, jsonify, request, g
from src.services.db_helpers import get_db_connection
from src.middleware.auth_middleware import token_required

category_budgets_blueprint = Blueprint("category_budgets_blueprint", __name__)


def create_category_budgets(user_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        monthly_income = 0
        monthly_budget = 0
        savings_goal = 0
        cursor.execute(
            """
                            INSERT INTO settings (monthly_income, monthly_budget, savings_goal, user_id)
                            VALUES (%s, %s,%s,%s,%s)
                            RETURNING *
                        """,
            (
                monthly_income,
                monthly_budget,
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
