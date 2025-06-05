# api/repositories/neo4j_repo.py

from neo4j import READ_ACCESS
from api.deps import neo4j_driver

class Neo4jRepo:
    def __init__(self):
        self.driver = neo4j_driver()

    def shortest_route(self, src_code: str, dst_code: str):
        """
        Ищет самый короткий путь (по количеству пересадок) между двумя узлами Airport с code=src_code и code=dst_code.
        Возвращает {'hops': [...], 'legs': <int>} или None, если путь не найден.
        """
        query = """
        MATCH (src:Airport {code:$src}), (dst:Airport {code:$dst})
        MATCH path = shortestPath((src)-[:ROUTE_TO*]-(dst))
        RETURN
          [n IN nodes(path) WHERE exists(n.code) | n.code] AS hops,
          size(relationships(path)) AS legs
        """

        with self.driver.session(default_access_mode=READ_ACCESS) as sess:
            record = sess.run(query, src=src_code, dst=dst_code).single()
            return record.data() if record else None
