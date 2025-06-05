-- Создание keyspace
CREATE KEYSPACE IF NOT EXISTS airport
WITH REPLICATION = {
  'class': 'SimpleStrategy',
  'replication_factor': 2
};

USE airport;

-- Таблица рейсов (по аэропорту)
CREATE TABLE flights_by_airport (
    airport_code TEXT,
    flight_id TEXT,
    departure_time TIMESTAMP,
    arrival_time TIMESTAMP,
    airline TEXT,
    status TEXT,
    PRIMARY KEY ((airport_code), departure_time, flight_id)
) WITH CLUSTERING ORDER BY (departure_time DESC);

-- Таблица рейсов (по авиакомпании)
CREATE TABLE flights_by_airline (
    airline TEXT,
    flight_id TEXT,
    departure_airport TEXT,
    arrival_airport TEXT,
    departure_time TIMESTAMP,
    arrival_time TIMESTAMP,
    PRIMARY KEY (airline, departure_time)
) WITH CLUSTERING ORDER BY (departure_time DESC);

-- Таблица пассажиров по рейсу
CREATE TABLE passengers_by_flight (
    flight_id TEXT,
    passenger_id TEXT,
    name TEXT,
    passport_number TEXT,
    seat TEXT,
    PRIMARY KEY (flight_id, passenger_id)
);

-- Таблица багажа по рейсу
CREATE TABLE baggage_by_flight (
    flight_id TEXT,
    baggage_id TEXT,
    passenger_id TEXT,
    weight INT,
    status TEXT,
    PRIMARY KEY (flight_id, baggage_id)
);

-- Таблица задержек по аэропорту
CREATE TABLE delays_by_airport (
    airport_code TEXT,
    flight_id TEXT,
    delay_time INT,
    reason TEXT,
    PRIMARY KEY (airport_code, flight_id)
);

-- Таблица билетов пассажира
CREATE TABLE tickets_by_passenger (
    passenger_id TEXT,
    ticket_id TEXT,
    flight_id TEXT,
    seat TEXT,
    price DECIMAL,
    PRIMARY KEY (passenger_id, ticket_id)
);

-- Таблица экипажа на рейсе
CREATE TABLE crew_by_flight (
    flight_id TEXT,
    crew_id TEXT,
    name TEXT,
    role TEXT,
    PRIMARY KEY (flight_id, crew_id)
);

-- Таблица выходов на посадку
CREATE TABLE gates_by_flight (
    flight_id TEXT,
    gate_number TEXT,
    terminal TEXT,
    status TEXT,
    PRIMARY KEY (flight_id, gate_number)
);

-- Таблица самолетов по модели
CREATE TABLE aircrafts_by_model (
    model TEXT,
    aircraft_id TEXT,
    capacity INT,
    airline TEXT,
    PRIMARY KEY (model, aircraft_id)
);

-- Таблица логов событий аэропорта
CREATE TABLE log_events (
    event_id UUID PRIMARY KEY,
    flight_id TEXT,
    event_type TEXT,
    timestamp TIMESTAMP,
    details TEXT
);
