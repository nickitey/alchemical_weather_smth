import logging

import requests

WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
GEO_URL = "http://api.openweathermap.org/geo/1.0/direct"


class MyWeatherappException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class ApiRequest(requests.Session):
    def __init__(self, headers=None):
        super().__init__()
        self.max_redirects = 5
        self.timeout = 5.0
        self.headers = headers

    def make_request(self, http_method, path, parse_json=True, **kwargs):
        try:
            response = self.request(
                http_method, path, **kwargs, timeout=self.timeout
            )
            response.raise_for_status()
            if parse_json:
                return response.json()
            else:
                return response
        except requests.JSONDecodeError as err:
            err_msg = f"Incoming JSON is invalid from char {err.pos}"
            raise MyWeatherappException(err_msg)
        except requests.TooManyRedirects:
            err_msg = f"Too much redirects. Allowed: {self.max_redirects}."
            raise MyWeatherappException(err_msg)
        except requests.HTTPError as err:
            err_msg = f"HTTPError is occured, and it is {err}"
            raise MyWeatherappException(err_msg)
        except requests.Timeout:
            err_msg = (
                f"Timeout error. Request is executed over "
                f"{self.timeout} seconds."
            )
            raise MyWeatherappException(err_msg)
        except requests.ConnectionError:
            err_msg = "Connection is lost, try again later."
            raise MyWeatherappException(err_msg)
        except requests.RequestException as err:
            raise MyWeatherappException(err)


class City:
    def __init__(self, data):
        self.latin_name = data["name"]
        try:
            self.ru_name = data["local_names"]["ru"]
        except KeyError:
            self.ru_name = None
        self.latitude = data["lat"]
        self.longitude = data["lon"]
        self.country = data["country"]
        self.state = data["state"]

    def get_coordinates(self):
        return self.latitude, self.longitude


class WeatherForecast:
    def __init__(self, data):
        self.weather = data["weather"]
        self.common = self.weather[0]["main"]
        self.description = self.weather[0]["description"]
        self.main = data["main"]
        self.cur_temp = self.main["temp"]
        self.max_temp = self.main["temp_max"]
        self.min_temp = self.main["temp_min"]
        self.feels_like = self.main["feels_like"]
        self.humidity = self.main["humidity"]
        self.pressure_hpa = self.main["pressure"]
        self.pressure_hg_mm = round(self.pressure_hpa / 1.33322, 0)


class GeoApp(ApiRequest):
    def __init__(self, api_key, root=GEO_URL, headers=None):
        super().__init__(headers)
        self.api_key = api_key
        self.root = root

    def get_coordinates(self, city_name):
        payload = {"q": city_name, "appid": self.api_key}
        response = self.make_request("get", path=self.root, params=payload)
        return City(response[0])


class WeatherApp(ApiRequest):
    def __init__(self, api_key, root=WEATHER_URL, headers=None):
        super().__init__(headers)
        self.api_key = api_key
        self.root = root

    def get_forecast(self, city_name, date=None, units="metric", lang="ru"):
        city_api_app = GeoApp(self.api_key, headers=self.headers)
        city = city_api_app.get_coordinates(city_name)
        payload = {
            "lat": city.latitude,
            "lon": city.longitude,
            "lang": lang,
            "units": units,
            "date": date,
            "appid": self.api_key,
        }
        response = self.make_request("get", path=self.root, params=payload)
        if response["cod"] != 200:
            err_msg = (
                "Something wrong with the response. See the content in log."
            )
            logging.exception(err_msg)
            logging.exception(f"Wrong answer content is: {response}.")
            raise MyWeatherappException(err_msg)
        return WeatherForecast(response)
