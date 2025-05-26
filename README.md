# ✈️ NoSQL Airport Cluster

Проект разворачивает кластер из MongoDB, Cassandra и Neo4j (Enterprise) с автоматической инициализацией структуры и данных. Используется тема "Аэропорт" с примерами CRUD-операций.

## 🚀 Быстрый запуск

Убедитесь, что вы дали права на выполнение скриптам:

```bash
sudo chmod 400 init/mongo/mongo.key
sudo chown 999:999 ./init/mongo/mongo.key
chmod +x cluster_init.sh init/neo4j/init.sh
```

Затем запустите:

```bash
./cluster_init.sh
```

Скрипт:

* останавливает старый кластер
* запускает `docker-compose`
* ожидает появления лидера в Neo4j
* выполняет `init.cypher`

## 🧪 Проверка всех кластеров

### 🔷 MongoDB — Репликация и Данные

```bash
docker exec -it mongo1 mongosh --username root --password example
```

Проверка статуса реплики:

```javascript
rs.status()
```

Проверка баз данных:

```javascript
show dbs
```

### 🔶 Cassandra — Кластер и Таблицы

```bash
docker exec -it cass1 cqlsh
```

Проверка keyspace и таблиц:

```sql
DESCRIBE KEYSPACES;
USE airport;
DESCRIBE TABLES;
SELECT * FROM flights_by_airport LIMIT 5;
```

### 🟦 Neo4j — Кластер, Роль и Данные

Подключение к лидеру (или любому узлу):

```bash
docker exec -it neo4j1 cypher-shell -u neo4j -p password
```

Проверка ролей и состояния:

```cypher
SHOW DATABASES YIELD name, address, role WHERE name = 'neo4j' RETURN address, role;
```

Проверка данных:

```cypher
MATCH (n) RETURN labels(n) AS labels, count(*) AS count ORDER BY count DESC;
```

Проверка связей:

```cypher
MATCH (f:Flight)-[:DEPARTS_FROM]->(a:Airport)
RETURN f.id, a.name
LIMIT 5;
```

## 🛠️ Примечания

* Neo4j: кластер из 3 CORE-узлов (Enterprise), с автоинициализацией через `init.sh`.
* MongoDB: `keyFile` и полноценная репликация `rs0`.
* Cassandra: `airport` keyspace и все таблицы создаются автоматически.
* Инициализация выполняется **только после подтверждения, что лидер Neo4j найден**.
