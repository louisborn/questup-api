from flask import Flask, request
from flask_cors import CORS

from mongodb_handler import MongoDBHandler

app = Flask(__name__)
CORS(app)

BASE_URL = '/quest-up/rest/v1/'
_db = MongoDBHandler()


@app.route(BASE_URL + 'teachers/<teacher_id>/subjects/<subject_id>/quests')
def get_quests(teacher_id, subject_id):
    """
    Parameters
    ----------
    :param teacher_id: the unique teacher identifier
    :param subject_id: the unique subject identifier
    :return: the list of quests
    """
    return _db.get_quests(teacher_id, subject_id)


@app.route(BASE_URL + 'annual-rewards/<teacher_id>')
def get_annual_rewards(teacher_id):
    """
    Parameters
    ----------
    :param teacher_id: the unique teacher identifier
    :return: the list of annual rewards
    """
    return _db.get_annual_rewards(teacher_id)


@app.route(BASE_URL + '<student_id>/quests/<quest_id>/submit', methods=['POST'])
def submit_student_quest_result(student_id, quest_id):
    """
    Parameters
    ----------
    :param student_id: the unique student identifier
    :param quest_id: the unique quest identifier
    :return:
    """
    json_data = request.get_json()  # Get the quest data object
    quest = json_data.get("quest")
    data_to_insert = {"students_id": student_id, "quests_id": quest_id, "score": None,
                      "results": quest["results"]}
    return _db.set_student_completed_quests(data_to_insert)


@app.route(BASE_URL + '<student_id>/scores/update', methods=['POST'])
def update_student_scores(student_id):
    json_data = request.get_json()  # Get the quest data object
    score = json_data.get("score")
    return _db.set_student_scores(student_id, score)


@app.route(BASE_URL + '<student_id>/scores/point-balance/update', methods=['POST'])
def update_points_balance(student_id):
    json_data = request.get_json()  # Get the quest data object
    score = json_data.get("points")
    return _db.update_student_points_balance(student_id, score)


@app.route(BASE_URL + 'students/<student_id>')
def get_student(student_id):
    """
    Parameters
    ----------
    :param student_id: the unique student identifier
    :return: the student data object
    """
    return _db.get_student(student_id)


@app.route(BASE_URL + 'shop-items/<teacher_id>')
def get_shop_items(teacher_id):
    """
    Parameters
    ----------
    :param teacher_id: the unique teacher identifier
    :return: the list of available shop items
    """
    return _db.get_shop_items(teacher_id)


@app.route(BASE_URL + 'students/<student_id>/scores')
def get_student_scores(student_id):
    return _db.get_student_scores(student_id)


@app.route(BASE_URL + 'students/<student_id>/completed-quests')
def get_student_completed_quests(student_id):
    return _db.get_student_completed_quests(student_id)


app.run(host="0.0.0.0", port=6009)
