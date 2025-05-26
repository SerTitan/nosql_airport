#!/bin/bash
set -e

echo "Снос старого кластера..."
docker compose down -v

echo "Запуск кластера Docker Compose..."
docker-compose up -d

echo "Ожидание Neo4j Leader и запуск init.cypher..."
init/neo4j/init.sh

echo "Кластер с тремя узлами готов к работе"
