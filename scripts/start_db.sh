#!/bin/bash

load_env() {
  if [ ! -f .env ]; then
    echo "❌ Error: .env not found"
    exit 1
  fi
  source .env
}

container_exists() {
  docker ps -a --format '{{.Names}}' | grep -q "^${DATABASE__CONTAINER_NAME}$"
}

container_is_running() {
  docker ps --format '{{.Names}}' | grep -q "^${DATABASE__CONTAINER_NAME}$"
}

wait_for_postgres() {
  echo "⏳ Waiting for PostgreSQL..."

  until docker exec "${DATABASE__CONTAINER_NAME}" pg_isready -U postgres > /dev/null 2>&1; do
    sleep 1
  done

  echo "✅ PostgreSQL ready"
}

start_existing_container() {
  echo "📦 Container exists"

  if container_is_running; then
    echo "✅ It is already running"
  else
    echo "▶️  Starting..."

    docker start "${DATABASE__CONTAINER_NAME}"
    wait_for_postgres
  fi
}

create_new_container() {
  echo "🆕 Creating container..."

  docker run -d \
    --name "${DATABASE__CONTAINER_NAME}" \
    -e POSTGRES_PASSWORD="${DATABASE__PASSWORD}" \
    -e POSTGRES_DB="${DATABASE__NAME}" \
    -p "${DATABASE__PORT}:5432" \
    -v "${DATABASE__CONTAINER_NAME}_pgdata:/var/lib/postgresql/data" \
    postgres:15

  wait_for_postgres

  echo "✅ Container created"
}

main() {
  load_env

  if container_exists; then
    start_existing_container
  else
    create_new_container
  fi

  echo "✅ PostgreSQL available at: ${DATABASE__HOST}:${DATABASE__PORT}"
}

main "${@}"
