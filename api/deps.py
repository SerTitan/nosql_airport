import os
from functools import lru_cache

from cassandra.cluster import Cluster, NoHostAvailable
from cassandra import InvalidRequest
from pymongo import MongoClient
from neo4j import GraphDatabase
import time


RETRY_SECS = 5
MAX_TRIES  = 60


@lru_cache
def cassandra_session():
    hosts = os.getenv("CASSANDRA_HOSTS", "cass1").split(",")
    cluster = Cluster(hosts)

    for attempt in range(1, MAX_TRIES + 1):
        try:
            # сначала без keyspace
            sess = cluster.connect()
            # пробуем переключиться
            sess.set_keyspace("airport")
            return sess
        except InvalidRequest:
            # keyspace ещё нет
            print(f"[{attempt}/{MAX_TRIES}] keyspace not ready, retrying…")
        except NoHostAvailable:
            # ноды ещё не слушают
            print(f"[{attempt}/{MAX_TRIES}] nodes unavailable, retrying…")
        time.sleep(RETRY_SECS)

    raise RuntimeError("Cassandra still unreachable after retries")


@lru_cache
def mongo_db():
    uri = os.getenv("MONGO_URI", "mongodb://mongo1:27017")
    db_name = os.getenv("MONGO_DB", "airport")
    client = MongoClient(uri)
    return client[db_name]


@lru_cache
def neo4j_driver():
    """
    Возвращает Neo4j-драйвер, используя переменные окружения:
      - NEO4J_URI  (то есть bolt://neo4j1:7687)
      - NEO4J_USER (например, 'neo4j')
      - NEO4J_PASS (например, 'password')
    """
    uri  = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    user = os.getenv("NEO4J_USER", "neo4j")
    pwd  = os.getenv("NEO4J_PASS", "password")
    # Отключаем шифрование, чтобы драйвер не пытался TLS проверять
    return GraphDatabase.driver(uri, auth=(user, pwd), encrypted=False)
