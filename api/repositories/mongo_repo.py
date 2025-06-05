from .. import deps
from pymongo import ASCENDING
import os

class MongoRepo:
    def __init__(self):
        client = deps.mongo_db()
        # берём имя базы из переменной окружения (airport)
        self.db = client[os.getenv("MONGO_DB", "airport")]
        self.coll = self.db["passengers"]

    def add_passenger(self, p):
        self.coll.insert_one(p.model_dump())

    def list_passengers(self, flight_id):
        return list(self.coll.find({"flight_id": flight_id}, {"_id": 0}))

    def top_destinations(self, limit=5):
        # db.eval устарел → делаем ту же агрегацию в коде
        pipeline = [
            {"$group": {"_id": "$flight_id", "cnt": {"$sum": 1}}},
            {"$sort": {"cnt": -1}},
            {"$limit": limit},
        ]
        return list(self.coll.aggregate(pipeline))
