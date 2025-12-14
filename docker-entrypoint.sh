#!/bin/sh

DJANGO_MANAGE="/app/manage.py"

MAX_TRIES=15
TRIES=0
echo "Waiting for database connection..."
while [ $TRIES -lt $MAX_TRIES ]; do
    if python $DJANGO_MANAGE check --database default; then
        echo "Database is ready."
        break
    fi
    echo "Database is unavailable - waiting..."
    sleep 2
    TRIES=$((TRIES+1))
done

if [ $TRIES -eq $MAX_TRIES ]; then
    echo "Error: Database connection failed after multiple attempts."
    exit 1
fi

# 2. Run database migrations
echo "Applying database migrations..."
python $DJANGO_MANAGE migrate --noinput

exec "$@"