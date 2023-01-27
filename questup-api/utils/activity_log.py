from datetime import date


class ActivityDataObject:
    cw = None
    time = None

    def _get_cw_for_year(self, year):
        last_week = date(year, 12, 28)
        return last_week.isocalendar().week

    def _get_all_cw(self, year):
        cw_names = []
        for week_number in range(1, self._get_cw_for_year(year)):
            cw_names.append(f"cw{week_number}")
        return cw_names

    def generate_initial_cw_for_year(self):
        init_log = {}
        calender_weeks = self._get_all_cw()
        for week in calender_weeks:
            init_log[week] = [None] * 5
        return init_log

    def serialize_cw_log_to_graph_data(self, cw_log):
        z = []
        x = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        y = []
        for cw in cw_log:
            y.append(cw)
            z.append(cw_log.get(cw))
        return {"z": z, "x": x, "y": y}
