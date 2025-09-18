#!/bin/sh
# wait-for-db.sh

set -e

host="$1"
shift
cmd="$@"

until psql "$DATABASE_URL" -c '\q' > /dev/null 2>&1; do
  >&2 echo "PostgreSQL not ready, waiting..."
  sleep 2
done

>&2 echo "PostgreSQL is ready"
exec $cmd