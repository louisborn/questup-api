from datetime import datetime, date


def get_minutes(seconds):
    """
    Calculates the amount of minutes from seconds.
    """
    SECONDS_PER_MINUTE = 60
    return round((seconds / SECONDS_PER_MINUTE), 0) if seconds is not None else seconds


class ActivityDataObject:
    """
    """

    cw = None
    time = None

    def _get_total_number_of_cw_by_year(self, year):
        last_week = date(year, 12, 28)
        return last_week.isocalendar().week

    def _get_cw_by_year(self, year=datetime.today().strftime('%Y')):
        cw_names = []
        for week_number in range(1, self._get_total_number_of_cw_by_year(year)):
            cw_names.append(f"cw{week_number}")
        return cw_names

    def init_student_activity_log_by_year(self):
        """
        Initializes an empty activity log for the current year.
        """
        init_log = {}
        calender_weeks = self._get_cw_by_year()
        for week in calender_weeks:
            init_log[week] = [None] * 5
        return init_log

    def serialize_student_activity_log_to_graph_data(self, cw_log):
        """
        Serializes the raw student activity log to heatmap graph data.
        """
        z = []  # The z-axis data, representing the student activity in minutes.
        x = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']  # The x-axis data, representing the week days.
        y = []  # The y-axis data, representing the calendar weeks.
        for cw in cw_log:
            y.append(cw)
            z.append([get_minutes(x) for x in cw_log.get(cw)])
        return {"z": z, "x": x, "y": y}
