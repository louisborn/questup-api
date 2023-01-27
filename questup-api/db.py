import pymongo

from bson import ObjectId
from datetime import datetime


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
    :return: the converted date string
    """
    date_from_timestamp = datetime.fromtimestamp(value[key])
    value[key] = datetime.strftime(date_from_timestamp, '%Y-%m-%d')
    return value


def is_timestamp_from_today(value):
    """
    Checks if a given date is equal to today`s date

    Parameters
    ----------
    :param value: the timestamp value
    :return: the boolean if the timestamp is equal to today`s date
    """
    today = datetime.strftime(datetime.today(), '%Y-%m-%d')
    return True if today == datetime.strftime(datetime.fromtimestamp(value), '%Y-%m-%d') else False


def get_db():
    return pymongo.MongoClient('localhost', 27017).questup


def get_quests_by_teacher_and_subject(teacher, subject):
    """
    Finds and returns quests by teacher and subject.
    Returns a list of dictionaries, each dictionary contains a calendar week, publish date, difficulty,
    points, content, subjects id, teachers id, image src and _id.
    """
    try:
        return [format_timestamp(stringify_id(x), key='publish_date') for x in get_db().quests.find(
            {'$and': [{'teachers_id': {'$eq': teacher}}, {'subjects_id': {'$eq': int(subject)}}]})]
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        return err


def get_annual_rewards_by_teacher(teacher):
    """
    Finds and returns annual rewards by teacher.
    Returns a list of dictionaries, each dictionary contains a teachers' id, rewards and _id.
    """
    try:
        return [stringify_id(x) for x in get_db().annual_rewards.find({'teachers_id': {'$eq': teacher}})]
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        return err


def get_shop_items_by_teacher(teacher):
    """
    Finds and returns shop items by teacher.
    Returns a list of dictionaries, each dictionary contains a title, usage amount, price, teachers id and _id.
    """
    try:
        return [stringify_id(x) for x in get_db().shop_items.find({'teachers_id': {'$eq': teacher}})]
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        return err


def get_student_completed_quests(student):
    """
    Finds and returns completed quests by student.
    Returns a list of dictionaries, each dictionary contains a score, results, quests id, students id and _id.
    """
    try:
        return [stringify_id(x) for x in
                get_db().students_completed_quests.find({'students_id': {'$eq': student}}, {'quests_id': 1})]
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        return err


def add_student_completed_quest(quest):
    """
    Inserts a completed quest into the student completed quests collection with the following fields:

    - "students_id"
    - "quests_id"
    - "score"
    - "results"

    Results is a list of question results as string.
    The score is null and could be updated by a teacher depending on the results quality.
    """
    try:
        return {"inserted_id": str(get_db().students_completed_quests.insert_one(quest).inserted_id)}
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        return err


def increment_points_balance(student, value):
    """
    Increments the points balance of a student by the value.

    Also increments the total gained points of a student.
    """
    try:
        return {"updated_count": str(get_db().students_scores.update_one({'students_id': student}, {
            '$inc': {"points_balance": value, "total_gained_points": value}}).modified_count)}
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        return err


def decrement_points_balance(student, value):
    """
    Decrements the points balance of a student by the value.
    """
    try:
        return {"updated_count": str(get_db().students_scores.update_one({'students_id': student}, {
            '$inc': {"points_balance": -value}}).modified_count)}
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        return err


def get_student_scores_by_selected(student, selection):
    """
    Finds and returns student scores by a selection filter.

    The selection filter indicates which field values are returned.
    Returns a list of dictionary, containing the selection filtered values.
    """
    try:
        return [stringify_id(x) for x in get_db().students_scores.find({'students_id': {'$eq': student}},
                                                                       selection)]
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        return err


def get_student_personal_by_selected(student, selection):
    """
    Finds and returns student personal data by a selection filter.

    The selection filter indicates which field values are returned.
    Returns a list of dictionary, containing the selection filtered values.
    """
    try:
        return [stringify_id(x) for x in get_db().students.find({'_id': {'$eq': ObjectId(student)}}, selection)]
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        return err


def count_student_completed_quests(student):
    """
    Counts the total completed quests by a student.
    Returns an integer containing the amount of counted documents.
    """
    try:
        return get_db().students_completed_quests.count_documents(
            {'students_id': {'$eq': student}})
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        return err


def count_total_quests(teacher):
    """
    Counts the total available quests of a teacher.
    Returns an integer containing the amount of counted documents.
    """
    try:
        return get_db().quests.count_documents(
            {'$and': [{'teachers_id': {'$eq': teacher}}, {'subjects_id': 0}]})
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        return err


def add_student_predicted_grade(student, value):
    """
    Inserts the predicted grade of a student into the students scores collection.
    """
    try:
        return get_db().students_scores.update_one({'students_id': {'$eq': student}},
                                                   {'$set': {"predicted_grade": value}}).modified_count
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        return err


def buy_shop_item(student, item, price):
    """
    Performs two main operations:

    1. Updating the bought items of a student
    2. Decrementing the point balance of a student
    """
    try:
        buy = {"updated_count": str(
            get_db().students_scores.update_one({'students_id': student}, {'$push': {'bought_items': item}}))}
        dec = decrement_points_balance(student, value=price)
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        return err
