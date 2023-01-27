import random
from db import MongoDBHandler
from datetime import datetime


class DailyChest:
    def __init__(self):
        self.POSSIBLE_WIN_POINTS = [100, 250, 500, 750, 1000, 2500]
        self.PROBABILITIES_TO_WIN_POINTS = [55, 30, 13, 1.5, 0.3, 0.2]
        self._db = MongoDBHandler()
        self.user_win = self._get_quest_win()

    def _get_quest_win(self):
        return random.choices(self.POSSIBLE_WIN_POINTS, self.PROBABILITIES_TO_WIN_POINTS, k=1)

    def update_redeem_date(self, user_id):
        now = int(datetime.timestamp(datetime.today()))
        return self._db.set_student_scores(user_id, {"latest_redeem_date": now})

    def store_quest_win(self, user_id):
        return self._db.increment_points_balance(user_id, score=self.user_win[0])
