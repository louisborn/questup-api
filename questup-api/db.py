import pymongo
from bson import ObjectId
from datetime import datetime
from utils.prediction import GradePredictionController


def stringify_id(value):
    """
    Converts an ObjectId into a str

    Parameters
    ----------
    :param value: the dict object
    :return: the data object with '_id' of type str
    """
    value["_id"] = str(value["_id"])
    return value


def format_timestamp(value, key):
    """
    Converts a timestamp into a formatted datetime

    Parameters
    ----------
    :param: the dict object with the timestamp
    """
    date_from_timestamp = datetime.fromtimestamp(value[key])
    value[key] = datetime.strftime(date_from_timestamp, '%Y-%m-%d')
    return value


def is_timestamp_from_today(value):
    today = datetime.strftime(datetime.today(), '%Y-%m-%d')
    return True if today == datetime.strftime(datetime.fromtimestamp(value), '%Y-%m-%d') else False


def get_db():
    return pymongo.MongoClient('localhost', 27017).questup


def get_quests_by_teacher_and_subject(teacher, subject):
    try:
        return [format_timestamp(stringify_id(x), key='publish_date') for x in get_db().quests.find(
            {'$and': [{'teachers_id': {'$eq': teacher}}, {'subjects_id': {'$eq': int(subject)}}]})]
    except (Exception, ValueError) as err:
        print(f"Unexpected {err=}, {type(err)=}")
        return err


def get_annual_rewards_by_teacher(teacher):
    try:
        return [stringify_id(x) for x in get_db().annual_rewards.find({'teachers_id': {'$eq': teacher}})]
    except (Exception, ValueError) as err:
        print(f"Unexpected {err=}, {type(err)=}")
        return err


def get_shop_items_by_teacher(teacher):
    try:
        return [stringify_id(x) for x in get_db().shop_items.find({'teachers_id': {'$eq': teacher}})]
    except (Exception, KeyError) as err:
        print(f"Unexpected {err=}, {type(err)=}")
        return err


def get_student_completed_quests(student):
    try:
        return [stringify_id(x) for x in
                get_db().students_completed_quests.find({'students_id': {'$eq': student}}, {'quests_id': 1})]
    except (Exception, KeyError) as err:
        print(f"Unexpected {err=}, {type(err)=}")
        return err


def add_student_completed_quest(quest):
    try:
        return {"inserted_id": str(get_db().students_completed_quests.insert_one(quest).inserted_id)}
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        return err


def increment_points_balance(student, value):
    try:
        return {"updated_count": str(get_db().students_scores.update_one({'students_id': student}, {
            '$inc': {"points_balance": value, "total_gained_points": value}}).modified_count)}
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        return err


def decrement_points_balance(student, value):
    try:
        return {"updated_count": str(get_db().students_scores.update_one({'students_id': student}, {
            '$inc': {"points_balance": -value}}).modified_count)}
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        return err


def get_student_scores_by_selected(student, selection):
    try:
        return [stringify_id(x) for x in get_db().students_scores.find({'students_id': {'$eq': student}},
                                                                       selection)]
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        return err


def get_student_selected_personal(student):
    try:
        return [stringify_id(x) for x in get_db().students.find(
            {'_id': {'$eq': ObjectId(student)}},
            {"absences": 1, "failures": 1, "freetime": 1, "g1": 1, "g2": 1, "goout": 1, "studytime": 1,
             "traveltime": 1})]
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        return err


def count_student_completed_quests(student):
    try:
        return get_db().students_completed_quests.count_documents(
            {'students_id': {'$eq': student}})
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        return err


def count_total_quests(teacher):
    try:
        return get_db().quests.count_documents(
            {'$and': [{'teachers_id': {'$eq': teacher}}, {'subjects_id': 0}]})
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        return err


def add_student_predicted_grade(student, value):
    try:
        return get_db().students_scores.update_one({'students_id': {'$eq': student}},
                                                   {'$set': {"predicted_grade": value}}).modified_count
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        return err


def buy_shop_item(student, item, price):
    try:
        buy = {"updated_count": str(
            get_db().students_scores.update_one({'students_id': student}, {'$push': {'bought_items': item}}))}
        dec = decrement_points_balance(student, value=price)
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        return err
