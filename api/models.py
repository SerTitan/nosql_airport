from datetime import datetime
from pydantic import BaseModel, Field


class FlightIn(BaseModel):
    airport_code: str = Field(..., max_length=4, example="SFO")
    flight_id: str    = Field(..., example="UA100")
    departure_time: datetime
    arrival_time: datetime
    airline: str


class FlightOut(FlightIn):
    pass


class PassengerIn(BaseModel):
    flight_id: str
    passenger_id: str
    name: str
    passport_number: str
    seat: str


class FlightTimes(BaseModel):
    """Тело запроса для обновления только времени рейса"""
    departure_time: datetime
    arrival_time:   datetime