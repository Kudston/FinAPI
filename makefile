init-alembic:
	alembic init ./src/

run-migrations:
	docker compose -f ./docker/local/docker-compose-dev.yml run -v ./src/:/usr/src/fin-api --remove-orphans fin-api alembic upgrade head

downgrade-alembic:
	docker compose -f ./docker/local/docker-compose-dev.yml run -v ./src/:/usr/src/fin-api --remove-orphans fin-api alembic downgrade head

create-revision:
	make run-migrations
	docker compose -f ./docker/local/docker-compose-dev.yml run -v ./src/:/usr/src/fin-api --remove-orphans fin-api alembic revision --autogenerate -m "${message}"

build-dev:
	docker compose -f ./docker/local/docker-compose-dev.yml up -d --build

run-dev:
	make run-migrations
	docker compose -f ./docker/local/docker-compose-dev.yml up -d

kill-dev:
	docker compose -f ./docker/local/docker-compose-dev.yml down

create-network:
	docker network create finapi-network

follow-dev-logs:
	docker container logs -f fin-api


# TEST FUNCTIONS
build-test:
	docker compose -f docker/test/docker-compose-test.yml build 

kill-test:
	make kill-dev
	docker compose -f docker/test/docker-compose-test.yml down

run-tests:
	make kill-dev
	make kill-test

	make run-migrations

	docker compose -f docker/local/docker-compose-dev.yml run --remove-orphans fin-api python -m pytest -s

	make kill-test