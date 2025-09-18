#!/bin/bash
echo "Starting SETUP..."

echo "Creating migrations..."
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py makemigrations app

echo "Aplying migrations..."
docker-compose exec web python manage.py migrate

echo "Creating users..."
docker-compose exec web python app/create_users.py

echo "Simulating 100 conversations..."
docker-compose exec web python app/simulate.py 15

echo "SetUp finish"
echo ""
echo "   Admin: http://localhost:8000/admin/"
echo "   Usuario: admin / admin123"
echo "   Usuario normal: user / user123"
echo "   API: http://localhost:8000/api/vegans/"
echo ""