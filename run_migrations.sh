#!/bin/sh

echo "Waiting for database to be ready..."
sleep 2

echo "Running migrations..."
alembic upgrade head

echo "Migrations completed!"

