.DEFAULT_GOAL := up

.PHONY: up down docker-makemigrations docker-migrate docker-test

up:
	docker compose -f docker/docker-compose.yml up --build

down:
	docker compose -f docker/docker-compose.yml down

docker-makemigrations:
	@cd docker && docker compose exec \
		--user root api bash -lc \
		"cd /app && uv run python manage.py makemigrations"

docker-migrate:
	@cd docker && docker compose exec \
		--user root api bash -lc \
		"uv run python manage.py migrate"

docker-test:
	@cd docker && docker compose \
		-f docker-compose.yml \
		-f docker-compose.test.yml \
		run --rm api