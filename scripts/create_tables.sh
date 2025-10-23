#!/bin/bash
# This script waits for the database to be ready and then creates the tables.

echo "Waiting for the database to initialize..."
sleep 15

echo "Creating database tables..."
docker-compose exec app python -c "from db_setup.run_db_setup import run; run()"
echo "Table creation process finished."
