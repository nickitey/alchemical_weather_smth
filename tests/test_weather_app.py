import logging
import os
import sys

from dotenv import load_dotenv

sys.path.insert(1, "../weatherapp")

from weatherapp.weather_app import GeoApp, WeatherApp

load_dotenv()
TOKEN = os.getenv("TOKEN")

date_format = "%d/%m/%Y"
time_format = "%H:%M:%S"

logging.basicConfig(
    filemode="w",
    format="%(asctime)s %(levelname)s:%(message)s\n",
    datefmt=f"{date_format} {time_format}",
    filename="weatherapp_test.log",
    encoding="utf-8",
    level=logging.INFO,
)

if os.getcwd().endswith("tests"):
    base_path = "./"
else:
    base_path = "./tests/"

headers = {
    "User-Agent": "Python-Study-App/1.0.0",
    "Content-Type": "application/json",
}

test_counter = 0


def test_get_coordinates():
    geo = GeoApp(api_key=TOKEN, headers=headers)
    Moscow = geo.get_coordinates("Moscow")
    long = 37.6174943
    lat = 55.7504461
    assert Moscow.longitude == long and Moscow.latitude == lat
    global test_counter
    test_counter += 1
    print(
        f"Test #{test_counter} passed. Received Moscow coordinates "
        f"are correct."
    )


def test_get_rostov_forecast():
    weather = WeatherApp(
        root="http://localhost:5000/rostov", api_key=TOKEN, headers=headers
    )
    current_weather = weather.get_forecast("Rostov-on-Don")
    assert current_weather.weather == [
        {
            "id": 500,
            "main": "Rain",
            "description": "небольшой дождь",
            "icon": "10d",
        }
    ]
    global test_counter
    test_counter += 1
    print(f"Test #{test_counter} passed. Frozen Rostov weather is correct.")


def test_get_ubud_forecast():
    weather = WeatherApp(
        root="http://localhost:5000/ubud", api_key=TOKEN, headers=headers
    )
    current_weather = weather.get_forecast("Ubud")
    assert current_weather.weather == [
        {"id": 804, "main": "Clouds", "description": "пасмурно", "icon": "04n"}
    ]
    global test_counter
    test_counter += 1
    print(f"Test #{test_counter} passed. Frozen Ubud weather is correct.")
