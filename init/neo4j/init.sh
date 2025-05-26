#!/bin/bash
echo "Ищем лидера и пытаемся исполнить init.cypher..."

for i in {1..60}; do
  for host in neo4j1 neo4j2 neo4j3; do
    echo "Пробуем $host..."
    docker exec -i "$host" cypher-shell -u neo4j -p password -d neo4j < ./init/neo4j/init.cypher 2>&1 | tee /tmp/cypherlog

    if ! grep -q "Failed to connect to neo4j://localhost:7687, fallback to bolt://localhost:7687" /tmp/cypherlog && ! grep -q "refused" /tmp/cypherlog; then
      echo "Успешно исполнено на $host"
      exit 0
    fi
  done
  echo "Повтор через 3 сек..."
  sleep 3
done

echo "Не удалось исполнить init.cypher на лидере"
exit 1