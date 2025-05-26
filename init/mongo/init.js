db = db.getSiblingDB("airport");

db.createCollection("flights");
db.flights.createIndex({ departure_time: 1 });

db.createCollection("airports");
db.airports.createIndex({ code: 1 }, { unique: true });

db.createCollection("aircrafts");
db.aircrafts.createIndex({ model: 1 });

db.createCollection("crew");
db.crew.createIndex({ flight_id: 1 });

db.createCollection("passengers");
db.passengers.createIndex({ passport_number: 1 }, { unique: true });

db.createCollection("tickets");
db.tickets.createIndex({ passenger_id: 1, flight_id: 1 }, { unique: true });

db.createCollection("boarding_passes");
db.boarding_passes.createIndex({ ticket_id: 1 }, { unique: true });

db.createCollection("baggage");
db.baggage.createIndex({ passenger_id: 1, flight_id: 1 });

db.createCollection("gates");
db.gates.createIndex({ airport_code: 1, gate_number: 1 }, { unique: true });

db.createCollection("delays");
db.delays.createIndex({ flight_id: 1 });
