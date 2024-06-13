import os
import logging
from dotenv import load_dotenv

from database_config import Base, User, WeatherReport, get_db_connection
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


load_dotenv()

db_username = os.getenv('PSQL_USER')
db_pswd = os.getenv('PSQL_PSWD')
db_host = os.getenv('PSQL_HOST')
db_port = os.getenv('PSQL_PORT')
db_name = os.getenv('PSQL_DB_NAME')


db_url = get_db_connection(
    db_username, db_pswd, db_host, db_port, db_name)

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
