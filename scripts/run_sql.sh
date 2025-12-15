#!/bin/bash
set -e

SETUP_DIR="app/database/sql"

function check_env() {
  if [ ! -f .env ]; then
    echo "Error: .env not found"
    exit 1
  fi
  set -a
  source .env
  set +a
}

function main() {
  local file path

  file="${1}"

  if [ -z "${file}" ]; then
    echo "Usage: ./scripts/run_sql.sh <filename>"
    exit 1
  fi

  path="${SETUP_DIR}/${file}"

  if [ ! -f "${path}" ]; then
    echo "Error: File not found: ${path}"
    exit 1
  fi

  check_env

  echo "→ Running: ${path}"
  envsubst < "${path}" | docker exec -i "${DATABASE__CONTAINER_NAME}" \
    psql -U "${DATABASE__USER}" -d "${DATABASE__NAME}"

  echo "✓ Done"
}

main "${@}"
