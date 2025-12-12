#!/bin/sh
# /app/docker-entrypoint.sh

# 1. Robust Wait Loop for Database availability
MAX_TRIES=15
TRIES=0
echo "Waiting for database connection..."
while [ $TRIES -lt $MAX_TRIES ]; do
    if python manage.py check --database default; then
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
python manage.py migrate --noinput

# 3. Execute the main command (gunicorn)
exec "$@"