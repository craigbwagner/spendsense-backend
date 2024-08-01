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


@category_budgets_blueprint.route("/budgets")
@token_required
def category_budgets_index():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        user_id = g.user["id"]
        cursor.execute("SELECT * FROM category_budgets WHERE user_id = %s", (user_id,))
        category_budgets = cursor.fetchone()
        return jsonify(category_budgets)
    except Exception as e:
        return jsonify({"Error": str(e)}), 500
    finally:
        connection.close()


@category_budgets_blueprint.route("/budgets", methods=["PUT"])
@token_required
def update_categories_budget():
    try:
        updated_budgets_data = request.json
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        user_id = g.user["id"]
        cursor.execute("SELECT * FROM category_budgets WHERE user_id = %s", (user_id,))
        settings_to_update = cursor.fetchone()
        if settings_to_update is None:
            return jsonify({"error": "User settings not found"}), 404
        connection.commit()
        if settings_to_update["user_id"] is not user_id:
            return ({"error": "Unauthorized"}), 401
        cursor.execute(
            """
                UPDATE category_budgets SET housing = %s, transportation = %s, food_groceries = %s, utilities = %s, clothing = %s, medical = %s, insurance = %s, personal = %s, education = %s, entertainment = %s, other = %s WHERE user_id = %s RETURNING *
            """,
            (
                updated_budgets_data["housing_budget"],
                updated_budgets_data["transportation_budget"],
                updated_budgets_data["food_groceries_budget"],
                updated_budgets_data["utilities_budget"],
                updated_budgets_data["clothing_budget"],
                updated_budgets_data["medical_budget"],
                updated_budgets_data["insurance_budget"],
                updated_budgets_data["personal_budget"],
                updated_budgets_data["education_budget"],
                updated_budgets_data["entertainment_budget"],
                updated_budgets_data["other_budget"],
                user_id,
            ),
        )
        updated_settings = cursor.fetchone()
        connection.commit()
        connection.close()
        return jsonify({"settings": updated_settings}), 200
    except Exception as e:
        return jsonify({"Error": str(e)}), 400
