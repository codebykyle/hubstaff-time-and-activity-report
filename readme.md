# Hubstaff Time and Activity Report

This is an unofficial self-hosted API for retrieving the Time and Activity report.

## Getting started

Copy `.env.example` to `.env`

Fill in your details as follows:

```dotenv
HUBSTAFF_USERNAME=
HUBSTAFF_PASSWORD=
HUBSTAFF_TIMEZONE=
HUBSTAFF_ORGANIZATION_ID=
```

## Run from the command line
Install python dependencies (consider doing this in a venv):

`pip install -r requirements.txt`

Then run flask

`flask run`


## Run as a docker container

`cp .env.example .env`

Edit your ENV

build the container

`docker-compose build`


Start the container

`docker-compose up`

## API

Make a GET request to the index of the application, eg

`http://127.0.0.1:5000/`

Supports the `start_date` and `end_date` filter to generate a report between two days.

If `start_date` or `end_date` are left blank, they will use the first and last day of the current month respectively.

This returns an object with the following format:

```json
{
    "params": {
        "date": "2021-06-01",
        "date_end": "2021-06-30",
        "filters[include_archived]": 1,
        "filters[show_activity]": 1,
        "filters[show_manual]": true,
        "filters[show_notes]": 1,
        "filters[show_spent]": 1,
        "filters[show_tasks]": 1,
        "group_by": "date"
    },
    "total_money": 1234567.89,
    "total_time": "99:99:99"
}
```
