import db
from utils.prediction import GradePredictionController
from utils.activity_log import ActivityDataObject


class ScoresPageHandler:
    def __init__(self, user_id, teacher_id):
        self.student = user_id
        self.teacher = teacher_id
        self.personal = self.update_predicted_grade()

    def _get_user_scores(self):
        return db.get_student_selected_scores(self.student)

    def _count_completed_quests(self):
        return db.count_student_completed_quests(self.student)

    def _count_total_quests(self):
        return db.count_total_quests(self.teacher)

    def _get_user_personal_data(self):
        return db.get_student_selected_personal(self.student)

    def _store_predicted_grade(self, grade):
        return db.store_student_predicted_grade(self.student, grade)

    def update_predicted_grade(self):
        personal = self._get_user_personal_data()
        controller = GradePredictionController(
            input_arr=[personal[0].get("studytime"), personal[0].get("failures"),
                       personal[0].get("absences"), personal[0].get("g1"),
                       personal[0].get("g2"), personal[0].get("freetime"),
                       personal[0].get("goout"), personal[0].get("traveltime")])
        grade = controller.predict()
        result = self._store_predicted_grade(grade)
        return personal

    def get_page_data(self):
        error = []
        payload = None
        try:
            payload = self._get_user_scores()
            payload[0]["total_quests_completed"] = self._count_completed_quests()
            payload[0]["total_quests_available"] = self._count_total_quests()
            payload[0]["user_personal"] = self.personal
            payload[0]["activity_log"] = ActivityDataObject().serialize_cw_log_to_graph_data(
                payload[0].get("activity_log"))
        except Exception as err:
            error = {"error": [f"Unexpected {err=}, {type(err)=}"]}
        finally:
            return {"error": error, "payload": payload}
