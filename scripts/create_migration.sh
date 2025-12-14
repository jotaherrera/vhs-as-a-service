#!/bin/bash

function create_file_safe() {
  local migration_file status
  migration_file="$1"

  set -o noclobber
  : > "$migration_file" 2> /dev/null
  status=$?
  set +o noclobber

  if [ $status -ne 0 ]; then
    echo "Error: $migration_file already exists"
    return 1
  fi
}

function create_migration() {
  local timestamp file_name path migration_folder migration_name

  migration_folder="$1"
  migration_name="$2"

  timestamp=$(date +%Y_%m_%d_%H%M)

  file_name="${timestamp}_${migration_name}.py"
  path="app/migrations/${migration_folder}/${file_name}"

  create_file_safe "$path" || exit 1

  cat << EOF >> "$path"
def main() -> None:
    pass


if __name__ == "__main__":
    main()
EOF

  echo "Migration created: $path"
}

function main() {
  local migration_folder migration_name

  migration_folder="$1"
  migration_name="$2"

  if [ $# -ne 2 ]; then
    echo "Usage: $0 <migration_folder> <migration_name>"
    exit 1
  fi

  create_migration "$migration_folder" "$migration_name"
}

main "$@"
