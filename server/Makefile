.PHONY: seed dev run db_upgrade

seed:
	@uv run python -m app.seed.main

dev:
	@uv run fastapi dev app.main --port 8001

run:
	@uv run fastapi run app.main --port 8001

db_upgrade:
	@uv run alembic upgrade head