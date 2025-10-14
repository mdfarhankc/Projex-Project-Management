.PHONY: seed run dev

seed:
	@python -m app.seed.main

run:
	@fastapi run app.main --port 8001

dev:
	@fastapi dev app.main --port 8001
