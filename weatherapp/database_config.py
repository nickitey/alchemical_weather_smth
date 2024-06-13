from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger, DateTime
from sqlalchemy.orm import relationship, DeclarativeBase


def get_db_connection(user, password, host, port, dbname):
    return f'postgresql://{user}:{password}@{host}:{port}/{dbname}'


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    tg_id = Column(BigInteger, nullable=False)
    city = Column(String(50))
    connection_date = Column(DateTime, nullable=False, default=datetime.now)
    reports = relationship('WeatherReport', backref='report', lazy=True,
                           cascade='all, delete-orphan')
    def __repr__(self):
        return self.tg_id


class WeatherReport(Base):
    __tablename__ = 'weather_reports'
    id = Column(Integer, primary_key=True)
    owner = Column(Integer, ForeignKey('users.id'))
    date = Column(DateTime, nullable=False, default=datetime.now)
    temp = Column(String(20), nullable=False)
    feels_like = Column(String(20), nullable=True)
    wind_speed = Column(String(20), nullable=False)
    pressure_mm = Column(String(20), nullable=False)
    city = Column(String(50), nullable=False)

    def __repr__(self):
        return f'Отчет о {self.city} за {self.date}.'
