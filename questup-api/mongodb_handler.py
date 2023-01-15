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


def format_timestamp(value):
    """
    Converts a timestamp into a formatted datetime

    Parameters
    ----------
    :param: the dict object with the timestamp
    """
    date_from_timestamp = datetime.fromtimestamp(value["publish_date"])
    value["publish_date"] = datetime.strftime(date_from_timestamp, '%Y-%m-%d')
    return value


class MongoDBClients:
    """
    A class to handle the database client access
    """

    def __init__(self):
        self.db_conn = 'mongodb+srv://testDB:test123@cluster0.rj3hvso.mongodb.net/test'

    def get_client_for_quests(self):
        return pymongo.MongoClient(self.db_conn).quest_up.quests

    def get_client_for_annual_rewards(self):
        return pymongo.MongoClient(self.db_conn).quest_up.annual_rewards

    def get_client_for_students(self):
        return pymongo.MongoClient(self.db_conn).quest_up.students

    def get_client_for_students_scores(self):
        return pymongo.MongoClient(self.db_conn).quest_up.students_scores

    def get_client_for_students_completed_quests(self):
        return pymongo.MongoClient(self.db_conn).quest_up.students_completed_quests

    def get_client_for_shop_items(self):
        return pymongo.MongoClient(self.db_conn).quest_up.shop_items


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
            return [format_timestamp(stringify_id(x)) for x in client.find(QUERY)]
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
            client = MongoDBClients.get_client_for_students_scores(self)
            QUERY = {'students_id': {'$eq': student_id}}
            return [stringify_id(x) for x in client.find(QUERY)]
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
        try:
            client = MongoDBClients.get_client_for_shop_items(self)
            QUERY = {'teachers_id': {'$eq': teacher_id}}
            return [stringify_id(x) for x in client.find(QUERY)]
        except (Exception, KeyError) as err:
            print(f"Unexpected {err=}, {type(err)=}")
            return self.error_message

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
