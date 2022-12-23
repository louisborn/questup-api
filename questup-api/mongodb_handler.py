import pymongo


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


class MongoDBClients:
    """
    A class to handle the database client access
    """
    def __init__(self):
        self.db_conn = 'mongodb+srv://testDB:test123@cluster0.rj3hvso.mongodb.net/test'
        self.collection_quests = pymongo.MongoClient(self.db_conn).quest_up.quests
        self.collection_annual_rewards = pymongo.MongoClient(self.db_conn).quest_up.annual_rewards
        self.collection_students = pymongo.MongoClient(self.db_conn).quest_up.students
        self.collection_shop_items = pymongo.MongoClient(self.db_conn).quest_up.shop_items

    def get_client_for_quests(self):
        return self.collection_quests

    def get_client_for_annual_rewards(self):
        return self.collection_annual_rewards

    def get_client_for_students(self):
        return self.collection_students

    def get_client_for_shop_items(self):
        return self.collection_shop_items


class MongoDBHandler(MongoDBClients):
    """
    A class to handle CRUD database operations
    """
    def __init__(self):
        super().__init__()

    def get_quests(self, teacher_id, subject_id):
        client = MongoDBClients.get_client_for_quests(self)
        QUERY = {'$and': [{'teacher_id': {'$eq': teacher_id}}, {'subject_id': {'$eq': subject_id}}]}
        return [stringify_id(x) for x in client.find(QUERY)]

    def get_annual_rewards(self, teacher_id):
        client = MongoDBClients.get_client_for_annual_rewards(self)
        QUERY = {'teacher_id': {'$eq': teacher_id}}
        return [stringify_id(x) for x in client.find(QUERY)]

    def get_student(self, student_id):
        client = MongoDBClients.get_client_for_students(self)
        QUERY = {'student_id': {'$eq': student_id}}
        return [stringify_id(x) for x in client.find(QUERY)]

    def get_shop_items(self, teacher_id):
        client = MongoDBClients.get_client_for_shop_items(self)
        QUERY = {'teacher_id': {'$eq': teacher_id}}
        return [stringify_id(x) for x in client.find(QUERY)]
