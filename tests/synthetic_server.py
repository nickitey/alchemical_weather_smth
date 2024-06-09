import json
import os
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask, request

load_dotenv()
TOKEN = os.getenv("TOKEN")

if os.getcwd().endswith("tests"):
    base_path = "./"
else:
    base_path = "./tests/"

date_format = "%d/%m/%Y"
time_format = "%H:%M:%S"

app = Flask(__name__)


@app.route("/rostov")
def return_rostov_json():
    query_template = "lat={}&lon={}&lang=ru&units=metric&appid={}"
    lat = 47.2213858
    lon = 39.7114196
    expected_query = query_template.format(lat, lon, TOKEN)
    sent_query = request.query_string.decode()
    if sent_query == expected_query:
        with open(f"{base_path}Ростов-на-Дону.json") as rostov:
            rostov_json = rostov.read()
        return rostov_json
    cur_day = datetime.now()
    cur_time = datetime.now()
    response = {
        "date": cur_day.strftime(date_format),
        "time": cur_time.strftime(time_format),
        "headers": dict(request.headers),
        "sent_query": sent_query,
        "body": "Test is failed, wrong request is made.",
    }
    return json.dumps(response)


@app.route("/ubud")
def return_ubud_json():
    query_template = "lat={}&lon={}&lang=ru&units=metric&appid={}"
    lat = -8.5068977
    lon = 115.2622931
    expected_query = query_template.format(lat, lon, TOKEN)
    sent_query = request.query_string.decode()
    if sent_query == expected_query:
        with open(f"{base_path}Убуд.json") as ubud:
            ubud_json = ubud.read()
        return ubud_json
    cur_day = datetime.now()
    cur_time = datetime.now()
    response = {
        "date": cur_day.strftime(date_format),
        "time": cur_time.strftime(time_format),
        "headers": dict(request.headers),
        "sent_query": sent_query,
        "body": "Test is failed, wrong request is made.",
    }
    return json.dumps(response)


app.run(debug=True)
