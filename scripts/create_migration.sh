#!/bin/bash

function create_file_safe() {
  local file status
  file="$1"

  set -o noclobber
  : > "$file" 2> /dev/null
  status=$?
  set +o noclobber

  if [ $status -ne 0 ]; then
    echo "Error: $file already exists"
    return 1
  fi
}

function create_migration() {
  local timestamp name filename path

  timestamp=$(date +%Y_%m_%d_%H%M)
  name="$1"
  filename="${timestamp}_${name}.py"
  path="app/migrations/data/${filename}"

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
  local name

  name="$1"

  if [ $# -ne 1 ]; then
    echo "Usage: $0 <migration_name>"
    exit 1
  fi

  create_migration "$name"
}

main "$@"
