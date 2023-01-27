import db

from flask import Flask, request
from flask_cors import CORS

from utils.daily_chest import DailyChest
from utils.scores_page import ScoresPageHandler
from utils.prediction import GradePredictionController

app = Flask(__name__)
CORS(app)

questup_api_v1_base = '/quest-up/rest/v1/'


@app.route(f"{questup_api_v1_base}teachers/<teacher>/subjects/<subject>/quests")
def get_quests(teacher, subject):
    """
    Parameters
    ----------
    :param teacher: the unique teacher identifier
    :param subject: the unique subject identifier
    :return: the list of quests
    """
    return db.get_quests_by_teacher_and_subject(teacher, subject)


@app.route(f"{questup_api_v1_base}annual-rewards/<teacher>")
def get_annual_rewards(teacher):
    """
    Parameters
    ----------
    :param teacher: the unique teacher identifier
    :return: the list of annual rewards
    """
    return db.get_annual_rewards_by_teacher(teacher)


@app.route(f"{questup_api_v1_base}shop-items/<teacher>")
def get_shop_items(teacher):
    """
    Parameters
    ----------
    :param teacher: the unique teacher identifier
    :return: the list of available shop items
    """
    return db.get_shop_items_by_teacher(teacher)


@app.route(f"{questup_api_v1_base}students/<student>/completed-quests")
def get_student_completed_quests(student):
    return db.get_student_completed_quests(student)


@app.route(f"{questup_api_v1_base}<student>/quests/<quest>/submit", methods=['POST'])
def submit_student_quest_result(student, quest):
    """
    Parameters
    ----------
    :param student: the unique student identifier
    :param quest: the unique quest identifier
    :return:
    """
    json_data = request.get_json()  # Get the quest data object
    body = json_data.get("quest")
    quest = {"students_id": student, "quests_id": quest, "score": None,
             "results": body["results"]}
    return db.add_student_completed_quest(quest)


@app.route(f"{questup_api_v1_base}<student>/scores/point-balance/update", methods=['POST'])
def update_points_balance(student):
    json_data = request.get_json()  # Get the quest data object
    value = json_data.get("points")
    return db.increment_points_balance(student, value)


@app.route(f"{questup_api_v1_base}student/<student>/scores")
def get_scores_page_data(student):
    handler = ScoresPageHandler(student, "63a7172a8883bff3af39eb2e")
    return handler.get_page_data()


@app.route(f"{questup_api_v1_base}predict/level", methods=['POST'])
def get_predicted_level():
    json_data = request.get_json()
    data = json_data.get("payload")
    controller = GradePredictionController(input_arr=data)
    return {"result": controller.predict()}


@app.route(f"{questup_api_v1_base}daily-quest/win/<student_id>")
def get_daily_quest_win(student):
    daily_quest = DailyChest()
    result = daily_quest.store_quest_win(student)
    if result.get("payload").get("updated_count") != 0:
        daily_quest.update_redeem_date(student)
    result.get("payload")["win"] = daily_quest.user_win
    return result


@app.route(f"{questup_api_v1_base}student/<student>/shop/points")
def get_student_points_for_shop(student):
    payload = db.get_student_scores_by_selected(student, selection={"points_balance": 1, "latest_redeem_date": 1,
                                                                    "bought_items": 1})
    payload[0]["latest_redeem_date"] = db.is_timestamp_from_today(payload[0].get("latest_redeem_date"))
    return payload


@app.route(f"{questup_api_v1_base}student/<student>/shop/buy/<item>", methods=["POST"])
def buy_shop_item(student, item):
    json_data = request.get_json()
    price = int(json_data.get("item_price"))
    return db.buy_shop_item(student, item, price)


app.run(host="0.0.0.0", port=6009, threaded=True)
