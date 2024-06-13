import sys

import pytest

sys.path.append("../weatherapp")
sys.path.append("../")

import weatherapp.orm_runner as orm

test_counter = 0


@pytest.fixture()
def get_user_id():
    return 123456789


@pytest.fixture()
def get_user_city():
    return "Moscow"


@pytest.fixture()
def get_weather_example():
    """
    Возвращает кортеж тестовых данных о погоде в city_name
    (за основу взят Белград 13 июня 2024 г.)
    :return: Название города, температура, "ощущается как", скорость ветра,
    атмосферное давление
    """
    return "Белград", "21.19", "21.3", "0", "760"


def test_add_tg_user(get_user_id):
    orm.add_user(get_user_id)
    session = orm.Session()
    test_user_query = (
        session.query(orm.User).filter_by(tg_id=get_user_id).first()
    )
    assert test_user_query.tg_id == get_user_id
    global test_counter
    test_counter += 1
    print(f"Test # {test_counter} passed. New user is added.")


def test_add_user_city(get_user_id, get_user_city):
    orm.add_city(get_user_id, get_user_city)
    session = orm.Session()
    test_user_query = (
        session.query(orm.User).filter(orm.User.tg_id == get_user_id).first()
    )
    assert test_user_query.city == get_user_city
    global test_counter
    test_counter += 1
    print(f"Test # {test_counter} passed. User's city is updated.")


def test_get_user_city():
    new_user = 987654321
    orm.add_user(new_user)
    new_user_city = orm.get_user_city(new_user)
    assert new_user_city == "Город пользователя не задан."
    global test_counter
    test_counter += 1
    print(f"Test # {test_counter} passed. User's city has got correctly.")


def test_get_all_users(get_user_id):
    users_list = orm.get_all_users(tg_id=True)
    assert get_user_id in users_list and 987654321 in users_list
    global test_counter
    test_counter += 1
    print(f"Test # {test_counter} passed. All users ids have got correctly.")


def test_add_weather_report(get_user_id, get_weather_example):
    city, temp, feels_like, wind_speed, pressure_mm = get_weather_example
    orm.add_weather_report(
        get_user_id, city, temp, feels_like, wind_speed, pressure_mm
    )
    session = orm.Session()
    test_weather_query = (
        session.query(orm.WeatherReport)
        .filter(orm.WeatherReport.city == city)
        .first()
    )
    assert (
        test_weather_query.temp == temp
        and test_weather_query.feels_like == feels_like
        and test_weather_query.pressure_mm == pressure_mm
    )
    global test_counter
    test_counter += 1
    print(f"Test # {test_counter} passed. User's city is updated.")


def test_get_user_reports(get_user_id, get_weather_example):
    city, temp, feels_like, wind_speed, pressure_mm = get_weather_example
    orm.add_weather_report(
        get_user_id, city, temp, feels_like, wind_speed, pressure_mm
    )
    reports = orm.get_users_reports(get_user_id)
    last_report = reports[-1]
    assert last_report.city == city and last_report.pressure_mm == pressure_mm
    global test_counter
    test_counter += 1
    print(f"Test # {test_counter} passed. All reports for user are collected"
          f" correctly.")
