import os
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from Services.Hubstaff.HubstaffClient import HubstaffClient
from datetime import date
from Services.DateHelper import parse_date, get_month_date_range

load_dotenv()

app = Flask(__name__)

@app.route('/')
def getTimeTotal():
    calendar_start, calendar_end = get_month_date_range(date.today().isoformat())

    start_date_input = request.args.get('start_date', default=calendar_start)
    end_date_input = request.args.get('end_date', default=calendar_end)

    hubstaff_client = HubstaffClient(
        os.environ['HUBSTAFF_USERNAME'],
        os.environ['HUBSTAFF_PASSWORD'],
        os.environ['HUBSTAFF_TIMEZONE'],
        os.environ['HUBSTAFF_ORGANIZATION_ID'],
    )

    if hubstaff_client.authenticate():
        time_report = hubstaff_client.timeAndActivityReport(
            start_date_input,
            end_date_input
        )

        print("Total Time: " + time_report.total_time())
        print("Total Money: $" + str(time_report.total_money()))

    else:
        raise Exception("Unable to authenticate")

    return jsonify(time_report.to_array())

