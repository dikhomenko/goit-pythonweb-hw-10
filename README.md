# goit-pythonweb-hw-08

# Docker

docker run --name my_postgres_task -e POSTGRES_PASSWORD=567234 -p 5432:5432 -d postgres
docker exec -it my_postgres_task psql -U postgres
CREATE DATABASE my_postgres_task_08;
\q

docker exec -it my_postgres_task psql -U postgres -c "\l"
docker exec -it my_postgres_task psql -U postgres -d my_postgres_task_08 -c "\dt"

# Alembic

alembic init migrations
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head

# Run application

uvicorn app.main:app --reload // or we could set reload=true

# Swagger is available by following url

http://127.0.0.1:8000/docs
