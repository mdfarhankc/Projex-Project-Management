.PHONY: seed dev run db_upgrade docker_up_build docker_up docker_down

seed:
	@uv run python -m app.seed.main

dev:
	@uv run fastapi dev app.main --port 8001

run:
	@uv run fastapi run app.main --port 8001

db_upgrade:
	@uv run alembic upgrade head

docker_up_build:
	@docker compose up --build

docker_up:
	@docker compose up

docker_down:
	@docker compose down