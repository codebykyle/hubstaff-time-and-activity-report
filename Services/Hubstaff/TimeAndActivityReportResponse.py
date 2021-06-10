from decimal import Decimal


class TimeAndActivityReportResponse:
    def __init__(self, params):
        self._params = params
        self._json = None
        self._total_time = None
        self._total_money = None

    def load_from_json(self, json):
        self._json = json

        total_time = 0
        total_money = 0

        for item in self._json['report_data']:
            total_time += item['tracked'] + item['manual']
            total_money += Decimal(item['spent'])

        min, sec = divmod(total_time, 60)
        hour, min = divmod(min, 60)

        self._total_time = "%d:%02d:%02d" % (hour, min, sec)
        self._total_money = total_money

    def total_time(self):
        return self._total_time

    def total_money(self):
        return self._total_money

    def to_array(self):
        return {
            'params': self._params,
            'total_time': self.total_time(),
            'total_money': float(self.total_money())
        }

