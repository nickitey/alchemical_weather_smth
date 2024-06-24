from datetime import datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import (DeclarativeBase, relationship, Mapped,
                            mapped_column, registry)

from typing_extensions import Annotated

str_20 = Annotated[str, 20]
str_30 = Annotated[str, 30]
str_50 = Annotated[str, 50]

intpk = Annotated[int, mapped_column(primary_key=True)]


def get_db_connection(user, password, host, port, dbname):
    return f"postgresql://{user}:{password}@{host}:{port}/{dbname}"


class Base(DeclarativeBase):
    registry = registry(
        type_annotation_map={
            str_20: String(20),
            str_30: String(30),
            str_50: String(50),
        }
    )


class User(Base):
    __tablename__ = "users"
    id: Mapped[intpk]
    tg_id: Mapped[int]
    city: Mapped[str_30 | None]
    connection_date: Mapped[datetime] = mapped_column(default=datetime.now)

    reports = relationship(
        "WeatherReport",
        back_populates="report_owner",
        lazy='selectin',
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return self.tg_id


class WeatherReport(Base):
    __tablename__ = "weather_reports"
    id: Mapped[intpk]
    owner: Mapped[int] = mapped_column(ForeignKey('users.id'))

    date: Mapped[datetime] = mapped_column(default=datetime.now)
    temp: Mapped[str_20]
    feels_like: Mapped[str_20 | None]
    wind_speed: Mapped[str_20 | None]
    pressure_mm: Mapped[str_20]
    city: Mapped[str_50]

    report_owner = relationship(
        'User',
        back_populates='reports',
        lazy='joined'
    )

    def __repr__(self):
        return (f"Отчет о погоде в {self.city} от "
                f"{self.date.strftime('%d.%m.%y %H:%M:%S')}")
