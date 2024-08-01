import psycopg2, psycopg2.extras
from flask import Blueprint, jsonify, request, g
from src.services.db_helpers import get_db_connection
from src.middleware.auth_middleware import token_required

category_budgets_blueprint = Blueprint("category_budgets_blueprint", __name__)


def create_category_budgets(user_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        housing_budget = 0
        transportation_budget = 0
        food_groceries_budget = 0
        utilities_budget = 0
        clothing_budget = 0
        medical_budget = 0
        insurance_budget = 0
        personal_budget = 0
        education_budget = 0
        entertainment_budget = 0
        other_budget = 0
        cursor.execute(
            """
                INSERT INTO category_budgets (
                    user_id,
                    housing,
                    transportation,
                    food_groceries,
                    utilities,
                    clothing,
                    medical,
                    insurance,
                    personal,
                    education,
                    entertainment,
                    other)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    RETURNING *
            """,
            (
                (user_id,),
                housing_budget,
                transportation_budget,
                food_groceries_budget,
                utilities_budget,
                clothing_budget,
                medical_budget,
                insurance_budget,
                personal_budget,
                education_budget,
                entertainment_budget,
                other_budget,
            ),
        )
        created_category_budgets = cursor.fetchone()
        connection.commit()
        return jsonify({"category_budgets": created_category_budgets}), 201
    except Exception as e:
        return jsonify({"Error": str(e)}), 400
    finally:
        connection.close()
