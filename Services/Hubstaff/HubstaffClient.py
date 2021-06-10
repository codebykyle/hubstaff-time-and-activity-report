import requests
from bs4 import BeautifulSoup

from Services.Hubstaff.TimeAndActivityReportResponse import TimeAndActivityReportResponse


class HubstaffClient:
    def __init__(self, username, password, timezone, org_id):
        self._username = username
        self._password = password
        self._timezone = timezone
        self._org_id = org_id
        self._session = requests.session()

    def authenticate(self):
        get_login_page_response = self._session.get("https://account.hubstaff.com/login")
        get_login_page_html = get_login_page_response.content
        get_login_page_soup = BeautifulSoup(get_login_page_html, 'html.parser')

        authenticity_token = get_login_page_soup.find('input', {'name': 'authenticity_token'}).get('value')

        post_login_data = {
            'utf-8': "✓",
            'authenticity_token': authenticity_token,
            'invite_token': None,
            'ab': None,
            'user[email]': self._username,
            'user[password]': self._password,
            'time_zone': self._timezone,
            'button': None
        }

        post_login_page_response = self._session.post('https://account.hubstaff.com/login', post_login_data)

        if 'Invalid email or password' in str(post_login_page_response.content):
            raise Exception("Unable to authenticate")

        check_account_response = self._session.get('https://account.hubstaff.com/')

        if 'Welcome,' not in str(check_account_response.content):
            raise Exception("Unable to find string")

        get_dashboard_url = 'https://app.hubstaff.com/login_now'
        get_dashboard_response = self._session.get(get_dashboard_url)

        return get_dashboard_response.status_code == 200

    def timeAndActivityReport(self, start_date, end_date):
        get_report_url = "https://app.hubstaff.com/reports/{org_id}/my/time_and_activities.json".format(org_id=self._org_id)

        get_report_data = {
            'date': start_date,
            'date_end': end_date,
            'group_by': 'date',
            'filters[include_archived]': 1,
            'filters[show_activity]': 1,
            'filters[show_notes]': 1,
            'filters[show_spent]': 1,
            'filters[show_tasks]': 1,
            'filters[show_manual]': True
        }

        get_report_response = self._session.get(
            get_report_url,
            params=get_report_data,
        )

        if get_report_response.status_code != 200:
            raise Exception("Unable to get report data")

        response_obj = TimeAndActivityReportResponse(get_report_data)
        response_obj.load_from_json(get_report_response.json())

        return response_obj
