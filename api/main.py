from fastapi import FastAPI, HTTPException, Query
from .models import FlightIn, FlightOut, PassengerIn, FlightTimes
from .repositories.cassandra_repo import CassandraRepo
from .repositories.mongo_repo import MongoRepo
from .repositories.neo4j_repo import Neo4jRepo

app = FastAPI(title="NoSQL-Airport API")

cass_repo = CassandraRepo()
mongo_repo = MongoRepo()
neo_repo  = Neo4jRepo()

# ------------------- Cassandra CRUD --------------------

@app.post("/flights", response_model=FlightOut, summary="Create flight")
def create_flight(flight: FlightIn):
    cass_repo.create_flight(flight)
    return flight


@app.get("/flights/{flight_id}", response_model=FlightOut)
def read_flight(flight_id: str):
    row = cass_repo.get_flight(flight_id)
    if not row:
        raise HTTPException(404)
    return FlightOut(**row._asdict())


@app.put("/flights/{flight_id}")
def update_times(flight_id: str, body: FlightTimes):
    cass_repo.update_flight_times(
        flight_id,
        body.departure_time,
        body.arrival_time,
    )
    return {"status": "updated"}


@app.delete("/flights/{flight_id}")
def delete_flight(flight_id: str):
    cass_repo.delete_flight(flight_id)
    return {"deleted": flight_id}

# ------------ Cassandra UDF-wrapper (обёртка) ----------

@app.get("/flights/{flight_id}/duration")
def flight_duration(flight_id: str):
    dur = cass_repo.flight_duration_ms(flight_id)
    if dur is None:
        raise HTTPException(404, "flight not found")
    return {"flight_id": flight_id, "duration_ms": dur}

# -------------------- Mongo endpoints ------------------

@app.post("/passengers")
def add_passenger(p: PassengerIn):
    mongo_repo.add_passenger(p)
    return {"added": p.passenger_id}


@app.get("/flights/{flight_id}/passengers")
def list_passengers(flight_id: str):
    return mongo_repo.list_passengers(flight_id)


@app.get("/stats/top-destinations")
def stats_top_destinations(limit: int = 5):
    return mongo_repo.top_destinations(limit)

# ---------------- Neo4j “обёрточный” метод -------------

@app.get("/routes/shortest")
def shortest(src: str, dst: str):
    try:
        result = neo_repo.shortest_route(src, dst)
    except Exception as e:
        # Вместо «маскировки» под 503, отправляем текст ошибки в ответ
        raise HTTPException(status_code=500, detail=f"Debug Neo4j Error: {e!r}")

    if not result:
        raise HTTPException(status_code=404, detail="Маршрут не найден")

    return result