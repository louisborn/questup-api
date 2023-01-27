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


def get_student_selected_scores(student):
    try:
        return [stringify_id(x) for x in get_db().students_scores.find({'students_id': {'$eq': student}},
                                                                       {"predicted_grade": 1, "total_gained_points": 1,
                                                                        "activity_log": 1})]
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


def store_student_predicted_grade(student, value):
    try:
        return get_db().students_scores.update_one({'students_id': {'$eq': student}},
                                                   {'$set': {"predicted_grade": value}}).modified_count
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        return err


class MongoDBClients:
    """
    A class to handle the database client access
    """

    def __init__(self):
        self.db_conn = pymongo.MongoClient('localhost', 27017).questup

    def get_client_for_quests(self):
        return self.db_conn.quests

    def get_client_for_annual_rewards(self):
        return self.db_conn.annual_rewards

    def get_client_for_students(self):
        return self.db_conn.students

    def get_client_for_students_scores(self):
        return self.db_conn.students_scores

    def get_client_for_students_completed_quests(self):
        return self.db_conn.students_completed_quests

    def get_client_for_shop_items(self):
        return self.db_conn.shop_items


class MongoDBHandler(MongoDBClients):
    """
    A class to handle CRUD database operations
    """

    def __init__(self):
        super().__init__()
        self.error_message = 'Unexpected Error'

    def get_quests(self, teacher_id, subject_id):
        try:
            client = MongoDBClients.get_client_for_quests(self)
            QUERY = {'$and': [{'teachers_id': {'$eq': teacher_id}}, {'subjects_id': {'$eq': int(subject_id)}}]}
            return [format_timestamp(stringify_id(x), key='publish_date') for x in client.find(QUERY)]
        except (Exception, ValueError) as err:
            print(f"Unexpected {err=}, {type(err)=}")
            return self.error_message

    def get_annual_rewards(self, teacher_id):
        try:
            client = MongoDBClients.get_client_for_annual_rewards(self)
            QUERY = {'teachers_id': {'$eq': teacher_id}}
            return [stringify_id(x) for x in client.find(QUERY)]
        except (Exception, ValueError) as err:
            print(f"Unexpected {err=}, {type(err)=}")
            return self.error_message

    def get_student(self, student_id):
        try:
            client = MongoDBClients.get_client_for_students(self)
            QUERY = {'_id': {'$eq': ObjectId(student_id)}}
            return [stringify_id(x) for x in client.find(QUERY)]
        except (Exception, KeyError) as err:
            print(f"Unexpected {err=}, {type(err)=}")
            return self.error_message

    def get_student_scores(self, student_id):
        try:
            student_data = self.get_student(student_id)
            client = MongoDBClients.get_client_for_students_scores(self)
            QUERY = {'students_id': {'$eq': student_id}}
            student_scores = [stringify_id(x) for x in client.find(QUERY)]
            controller = GradePredictionController(
                input_arr=[student_data[0].get("studytime"), student_data[0].get("failures"),
                           student_data[0].get("absences"), student_data[0].get("g1"),
                           student_data[0].get("g2"), student_data[0].get("freetime"),
                           student_data[0].get("goout"), student_data[0].get("traveltime")])
            predicted_grade = controller.predict()
            self.set_student_scores(student_id, score={"predicted_grade": predicted_grade})
            student_scores[0]["user_personal"] = student_data[0]
            return student_scores
        except (Exception, KeyError) as err:
            print(f"Unexpected {err=}, {type(err)=}")
            return self.error_message

    def get_student_completed_quests(self, student_id):
        try:
            client = MongoDBClients.get_client_for_students_completed_quests(self)
            QUERY = {'students_id': {'$eq': student_id}}
            return [stringify_id(x) for x in client.find(QUERY, {'quests_id': 1})]
        except (Exception, KeyError) as err:
            print(f"Unexpected {err=}, {type(err)=}")
            return self.error_message

    def get_shop_items(self, teacher_id):
        error = []
        payload = None
        try:
            client = MongoDBClients.get_client_for_shop_items(self)
            QUERY = {'teachers_id': {'$eq': teacher_id}}
            payload = [stringify_id(x) for x in client.find(QUERY)]
        except (Exception, KeyError) as err:
            error = f"Unexpected {err=}, {type(err)=}"
        finally:
            return {"error": error, "payload": payload}

    def set_student_completed_quests(self, quest):
        try:
            client = MongoDBClients.get_client_for_students_completed_quests(self)
            return {"inserted_id": str(client.insert_one(quest).inserted_id)}
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            return self.error_message

    def set_student_scores(self, student_id, score):
        try:
            client = MongoDBClients.get_client_for_students_scores(self)
            QUERY = {'students_id': student_id}
            UPDATE = {'$set': {}}
            for entry in score:
                UPDATE['$set'][entry] = score[entry]
            return {"updated_count": str(client.update_one(QUERY, UPDATE).modified_count)}
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            return self.error_message

    # todo split in inc und dec
    def update_student_points_balance(self, student_id, score):
        try:
            client = MongoDBClients.get_client_for_students_scores(self)
            QUERY = {'students_id': student_id}
            if score > 0:
                UPDATE = {'$inc': {"points_balance": score, "total_gained_points": score}}
            else:
                UPDATE = {'$inc': {"points_balance": score}}
            return {"updated_count": str(client.update_one(QUERY, UPDATE).modified_count)}
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            return self.error_message

    def increment_points_balance(self, student_id, score):
        error = []
        updated_count = -1
        try:
            client = MongoDBClients.get_client_for_students_scores(self)
            updated_count = {"updated_count": str(client.update_one({'students_id': student_id}, {
                '$inc': {"points_balance": score, "total_gained_points": score}}).modified_count)}
        except Exception as err:
            error = {"error": [f"Unexpected {err=}, {type(err)=}"]}
        finally:
            return {"error": error, "payload": {"updated_count": updated_count}}

    def decrement_points_balance(self, student_id, value):
        error = []
        updated_count = -1
        try:
            client = MongoDBClients.get_client_for_students_scores(self)
            updated_count = {"updated_count": str(client.update_one({'students_id': student_id}, {
                '$inc': {"points_balance": -value}}).modified_count)}
        except Exception as err:
            error = {"error": [f"Unexpected {err=}, {type(err)=}"]}
        finally:
            return {"error": error, "payload": {"updated_count": updated_count}}

    def get_student_shop_data(self, student_id):
        error = []
        payload = None
        try:
            client = MongoDBClients.get_client_for_students_scores(self)
            QUERY = {'students_id': {'$eq': student_id}}
            payload = [stringify_id(x) for x in
                       client.find(QUERY, {"points_balance": 1, "latest_redeem_date": 1, "bought_items": 1})]
            payload[0]["latest_redeem_date"] = is_timestamp_from_today(payload[0].get("latest_redeem_date"))
        except Exception as err:
            error = {"error": [f"Unexpected {err=}, {type(err)=}"]}
        finally:
            return {"error": error, "payload": payload}

    def buy_shop_item(self, student_id, item_id, price):
        error = []
        payload = None
        try:
            client = MongoDBClients.get_client_for_students_scores(self)
            QUERY = {'students_id': {'$eq': student_id}}
            buy = {"updated_count": str(
                client.update_one({'students_id': student_id}, {'$push': {'bought_items': item_id}}))}
            dec = self.decrement_points_balance(student_id, value=price)
            if buy.get("updated_count") == 1 and dec.get("updated_count") == 1:
                payload = [{"status": 'Okay'}]
        except Exception as err:
            error = {"error": [f"Unexpected {err=}, {type(err)=}"]}
        finally:
            return {"error": error, "payload": payload}
