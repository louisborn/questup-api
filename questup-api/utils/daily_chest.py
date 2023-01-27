import db
import random

from datetime import datetime


class DailyChest:
    """
    A class to handle the daily chest feature.
    """

    def __init__(self):
        self.POSSIBLE_WIN_POINTS = [100, 250, 500, 750, 1000, 2500]  # The possible daily chest wins.
        self.PROBABILITIES_TO_WIN_POINTS = [55, 30, 13, 1.5, 0.3, 0.2]  # The probability to receive the wins.
        self.user_win = self._get_quest_win()

    def _get_quest_win(self):
        """
        Calculates the daily chest win using the possible wins and their probabilities.
        """
        return random.choices(self.POSSIBLE_WIN_POINTS, self.PROBABILITIES_TO_WIN_POINTS, k=1)

    def update_redeem_date(self, student):
        """
        Calculates the current timestamp and updates the student scores using the calculated timestamp.

        Parameters
        ----------
        :param student: The student id
        """
        now = int(datetime.timestamp(datetime.today()))
        return db.add_student_redeem_date(student, now)

    def store_quest_win(self, student):
        """
        Increments the points balance of the student using the daily chest win.

        Parameters
        ----------
        :param student: The student id
        """
        return db.increment_points_balance(student, value=self.user_win[0])
