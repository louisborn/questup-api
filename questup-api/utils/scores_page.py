import db
from utils.prediction import GradePredictionController
from utils.activity_log import ActivityDataObject


class ScoresPageHandler:
    """
    A helper class for the scores page.
    """

    def __init__(self, student, teacher):
        self.student = student
        self.teacher = teacher
        self.personal = self.update_predicted_grade()

    def _get_user_scores(self):
        return db.get_student_scores_by_selected(self.student,
                                                 selection={"predicted_grade": 1, "total_gained_points": 1,
                                                            "activity_log": 1})

    def _get_user_personal_data(self):
        return db.get_student_personal_by_selected(self.student,
                                                   selection={"absences": 1, "failures": 1, "freetime": 1, "g1": 1,
                                                              "g2": 1, "goout": 1, "studytime": 1,
                                                              "traveltime": 1})

    def _count_completed_quests(self):
        return db.count_student_completed_quests(self.student)

    def _count_total_quests(self):
        return db.count_total_quests(self.teacher)

    def _store_predicted_grade(self, grade):
        return db.add_student_predicted_grade(self.student, grade)

    def update_predicted_grade(self):
        """
        Predicts and inserts the new student grade into the students scores.

        Parameters
        ----------
        :return personal: The fetched student personal data. Is later used to get the scores' page data.
        """
        personal = self._get_user_personal_data()  # Get the current student personal data.
        controller = GradePredictionController(
            input_arr=[personal[0].get("studytime"), personal[0].get("failures"),
                       personal[0].get("absences"), personal[0].get("g1"),
                       personal[0].get("g2"), personal[0].get("freetime"),
                       personal[0].get("goout"), personal[0].get("traveltime")])
        grade = controller.predict()  # Predict the new grade.
        result = self._store_predicted_grade(grade)  # Store the predicted grade.
        return personal

    def get_page_data_object(self):
        error = []  # The error list of the operation.
        payload = None  # The result payload of the operation.
        try:
            payload = self._get_user_scores()
            payload[0]["total_quests_completed"] = self._count_completed_quests()
            payload[0]["total_quests_available"] = self._count_total_quests()
            payload[0]["user_personal"] = self.personal
            payload[0]["activity_log"] = ActivityDataObject().serialize_student_activity_log_to_graph_data(
                payload[0].get("activity_log"))
        except Exception as err:
            error = {"error": [f"Unexpected {err=}, {type(err)=}"]}
        finally:
            return {"error": error, "payload": payload}
