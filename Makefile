.PHONY: alembic build up stop env venv push

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

venv:
	apt install python3.12-venv && source .venv/bin/activate && pip install -r requirements.txt

push:
	git add . && git commit -m "Commit += 1" && git push
