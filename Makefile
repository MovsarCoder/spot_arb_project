.PHONY: alembic build up stop env

alembic:
	alembic revision --autogenerate -m 'Коммит += 1' && alembic upgrade head

build:
	git pull && docker-compose down && docker-compose up --build -d && docker-compose logs -f bot
up:
	docker-compose up -d --build

down:
	docker-compose down -v

ps:
	docker compose ps

env:
	cp .env.example .env



