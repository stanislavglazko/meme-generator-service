APP_NAME="meme_generator"
LOCAL_DB_PORT?=5432

build_api:
	cd ./server && \
	docker build \
		--target base \
		-t ${APP_NAME}-api:latest \
		.

run_api:
	docker-compose up -d

migrate_database:
	docker-compose run --rm api ./manage.py migrate

init:
	docker-compose build
	docker-compose up -d
	docker-compose run --rm api ./manage.py migrate
	docker-compose run --rm api ./manage.py createsuperuser

stop:
	docker-compose down

.PHONY: build_api run_api migrate_database
