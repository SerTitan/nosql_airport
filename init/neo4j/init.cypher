// Аэропорты
CREATE (:Airport {code: "SVO", name: "Sheremetyevo", city: "Moscow", country: "Russia"});
CREATE (:Airport {code: "JFK", name: "John F. Kennedy", city: "New York", country: "USA"});

// Рейсы (правильный формат даты)
CREATE (:Flight {
  id: "FL1234",
  airline: "Aeroflot",
  departure_time: datetime("2025-02-23T14:30:00"),
  arrival_time: datetime("2025-02-23T20:45:00"),
  status: "On Time"
});

// Пассажиры
CREATE (:Passenger {id: "P123", name: "Ivan Petrov", passport_number: "123456789", nationality: "Russian"});

// Билеты
CREATE (:Ticket {id: "T789", seat: "12A", price: 450});

// Экипаж
CREATE (:Crew {id: "C456", name: "John Smith", role: "Pilot"});

// Самолёты
CREATE (:Aircraft {id: "A320", model: "Airbus A320", capacity: 180});

// Выходы на посадку (Gates)
CREATE (:Gate {id: "G5", terminal: "A", status: "Open"});

// Багаж
CREATE (:Baggage {id: "B456", weight: 23, status: "Checked-in"});

// Задержки рейсов
CREATE (:Delay {id: "D567", reason: "Weather", delay_time: 90});

// События (Лог аэропорта) - с правильной датой
CREATE (:Event {id: "E999", type: "Boarding", timestamp: datetime("2025-02-23T14:00:00")});

// Рейсы между аэропортами
MATCH (a1:Airport {code: "SVO"}), (a2:Airport {code: "JFK"}), (f:Flight {id: "FL1234"})
CREATE (f)-[:DEPARTS_FROM]->(a1),
       (f)-[:ARRIVES_AT]->(a2);

// Пассажир покупает билет
MATCH (p:Passenger {id: "P123"}), (t:Ticket {id: "T789"})
CREATE (p)-[:HAS_TICKET]->(t);

// Билет относится к рейсу
MATCH (t:Ticket {id: "T789"}), (f:Flight {id: "FL1234"})
CREATE (t)-[:FOR_FLIGHT]->(f);

// Экипаж назначен на рейс
MATCH (c:Crew {id: "C456"}), (f:Flight {id: "FL1234"})
CREATE (c)-[:ASSIGNED_TO]->(f);

// Самолет используется в рейсе
MATCH (ac:Aircraft {id: "A320"}), (f:Flight {id: "FL1234"})
CREATE (ac)-[:USED_IN]->(f);

// Выход на посадку для рейса
MATCH (f:Flight {id: "FL1234"}), (g:Gate {id: "G5"})
CREATE (f)-[:HAS_GATE]->(g);

// Багаж принадлежит пассажиру
MATCH (b:Baggage {id: "B456"}), (p:Passenger {id: "P123"})
CREATE (b)-[:BELONGS_TO]->(p);

// Багаж связан с рейсом
MATCH (b:Baggage {id: "B456"}), (f:Flight {id: "FL1234"})
CREATE (b)-[:LOADED_ON]->(f);

// Задержка связана с рейсом
MATCH (d:Delay {id: "D567"}), (f:Flight {id: "FL1234"})
CREATE (d)-[:AFFECTS]->(f);

// Событие в аэропорту связано с рейсом
MATCH (e:Event {id: "E999"}), (f:Flight {id: "FL1234"})
CREATE (e)-[:RELATED_TO]->(f);
