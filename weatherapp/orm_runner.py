import logging
import os

from database_config import Base, User, WeatherReport, get_db_connection
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from weather_app import MyWeatherappException

load_dotenv()

db_username = os.getenv("PSQL_USER")
db_pswd = os.getenv("PSQL_PSWD")
db_host = os.getenv("PSQL_HOST")
db_port = os.getenv("PSQL_PORT")
db_name = os.getenv("PSQL_DB_NAME")

db_url = get_db_connection(db_username, db_pswd, db_host, db_port, db_name)

engine = create_engine(db_url, echo=False)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)


def add_user(tg_id):
    session = Session()
    user = session.query(User).filter(User.tg_id == tg_id).first()
    if user is None:
        new_user = User(tg_id=tg_id)
        session.add(new_user)
        session.commit()


def add_city(tg_id, city_name):
    session = Session()
    add_user(tg_id)
    user = session.query(User).filter(User.tg_id == tg_id).first()
    user.city = city_name
    session.commit()


def get_user_city(tg_id):
    session = Session()
    user = session.query(User).filter(User.tg_id == tg_id).first()
    if user.city is None:
        return "Город пользователя не задан."
    return user.city


def get_all_users(personal_id=None, tg_id=None):
    if personal_id is None and tg_id is None:
        err_msg = (
            "Необходимо выбрать, какие данные пользователей "
            "необходимо вывести"
        )
        logging.exception(err_msg)
        raise MyWeatherappException(err_msg)
    session = Session()
    users = session.query(User).all()
    if personal_id:
        return [user.id for user in users]
    return [user.tg_id for user in users]


def add_weather_report(tg_id, city, temp, feels_like, wind_speed, pressure_mm):
    session = Session()
    user = session.query(User).filter(User.tg_id == tg_id).first()
    new_report = WeatherReport(
        owner=user.id,
        city=city,
        temp=temp,
        feels_like=feels_like,
        wind_speed=wind_speed,
        pressure_mm=pressure_mm,
    )
    session.add(new_report)
    session.commit()


def get_users_reports(tg_id):
    session = Session()
    user = session.query(User).filter(User.tg_id == tg_id).first()
    return user.reports

