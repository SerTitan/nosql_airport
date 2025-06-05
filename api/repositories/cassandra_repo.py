# api/repositories/cassandra_repo.py
from datetime import datetime

from cassandra.query import SimpleStatement
from api.models import FlightIn
from api import deps


class CassandraRepo:
    """Небольшая обёртка над Cassandra-сессией."""

    def __init__(self) -> None:
        self.session = deps.cassandra_session()

    # ------------------------------------------------------------------ #
    # CRUD по рейсам
    # ------------------------------------------------------------------ #
    def create_flight(self, f: FlightIn, status: str = "scheduled") -> None:
        """
        Создаём запись сразу в двух денормализованных таблицах.
        Вместо '?' в CQL используем '%s' для корректного биндинга параметров.
        """
        # flights_by_airport --------------------------------------------
        self.session.execute(
            """
            INSERT INTO flights_by_airport
                (airport_code, departure_time, flight_id,
                 airline,       arrival_time,  status)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                f.airport_code,
                f.departure_time,
                f.flight_id,
                f.airline,
                f.arrival_time,
                status,
            ),
        )

        # flights_by_airline --------------------------------------------
        # departure_airport у нас — f.airport_code, arrival_airport пока не задан
        self.session.execute(
            """
            INSERT INTO flights_by_airline
                (airline, departure_time, flight_id,
                 departure_airport,       arrival_airport)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                f.airline,
                f.departure_time,
                f.flight_id,
                f.airport_code,
                None,  # arrival_airport
            ),
        )

    # ------------------------------------------------------------------ #
    def get_flight(self, flight_id: str):
        """
        Получаем рейс через ALLOW FILTERING.
        """
        stmt = SimpleStatement(
            "SELECT * FROM flights_by_airport WHERE flight_id = %s ALLOW FILTERING"
        )
        return self.session.execute(stmt, (flight_id,)).one()

    # ------------------------------------------------------------------ #
    def update_flight_times(
        self, flight_id: str, departure_time: datetime, arrival_time: datetime
    ) -> None:
        """
        departure_time входит в clustering-key ⇒ UPDATE обычным SET невозможен.
        Удаляем старую строку и вставляем новую с новыми time.
        """
        old = self.get_flight(flight_id)
        if old is None:
            raise ValueError("flight not found")

        # 1. удаляем старую запись
        self.session.execute(
            """
            DELETE FROM flights_by_airport
             WHERE airport_code = %s AND departure_time = %s AND flight_id = %s
            """,
            (old.airport_code, old.departure_time, flight_id),
        )

        # 2. вставляем новую строку с обновлёнными временами
        self.session.execute(
            """
            INSERT INTO flights_by_airport
                (airport_code, departure_time, flight_id,
                 airline,       arrival_time,  status)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                old.airport_code,
                departure_time,
                flight_id,
                old.airline,
                arrival_time,
                old.status,
            ),
        )

    # ------------------------------------------------------------------ #
    def delete_flight(self, flight_id: str) -> None:
        """
        Сначала находим существующую строку, чтобы узнать partition‐key, затем удаляем её.
        """
        row = self.get_flight(flight_id)
        if row is None:
            raise ValueError("flight not found")

        self.session.execute(
            """
            DELETE FROM flights_by_airport
             WHERE airport_code = %s AND departure_time = %s AND flight_id = %s
            """,
            (row.airport_code, row.departure_time, flight_id),
        )

    # ------------------------------------------------------------------ #
    def flight_duration_ms(self, flight_id: str) -> int:
        """
        duration_ms UDF в кластере нет – считаем продолжительность на стороне приложения.
        """
        row = self.get_flight(flight_id)
        if row is None:
            raise ValueError("flight not found")

        return int((row.arrival_time - row.departure_time).total_seconds() * 1000)
