import calendar
from datetime import date, datetime


def parse_date(date):
    return datetime.strptime(date, '%Y-%m-%d').date()


def get_month_date_range(from_date=None):
    '''

    Get a date range from the beginning to the end of the input month. If no month is provided,
    uses this month

    :param from_date: String YYYY-MM-DD format
    :return: (date, date)
    '''
    today = parse_date(from_date) if from_date is not None else date.today()

    first_day_of_month = date(
        today.year,
        today.month,
        1
    )

    number_of_days_this_month = calendar.monthrange(
        today.year,
        today.month
    )

    last_day_of_month = date(
        today.year,
        today.month,
        number_of_days_this_month[1]
    )

    return first_day_of_month.isoformat(), last_day_of_month.isoformat()
