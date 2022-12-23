import pymongo


def stringify_id(value):
    """
    Converts an ObjectId into a str

    Parameters
    ----------
    :param value: the dict object
    :return:
    """
    value["_id"] = str(value["_id"])
    return value


class MongoDBClients:
    def __init__(self):
        self.db_conn = 'mongodb+srv://testDB:test123@cluster0.rj3hvso.mongodb.net/test'
        self.collection_quests = pymongo.MongoClient(self.db_conn).quest_up.quests
        self.collection_annual_rewards = pymongo.MongoClient(self.db_conn).quest_up.annual_rewards

    def get_client_for_quests(self):
        return self.collection_quests

    def get_client_for_annual_rewards(self):
        return self.collection_annual_rewards


class MongoDBHandler(MongoDBClients):
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
