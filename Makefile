## @ Docker Commands
.PHONY: build up down run restart
build: ## Create the image of dockerfile
	docker-compose build

up: ## Start the application
	docker-compose up -d

down: ## Remove the docker images and containers
	docker-compose down

run: ## Build and run the application
	docker-compose --env-file ./env.env -f docker-compose.yml up --build -d

run_dev: ## Build and run the application in dev mode
	docker-compose --env-file ./env.env -f docker-compose.dev.yml up --build -d
	export PYTHONPATH="${PYTHONPATH}:$PWD" && poetry run python ./src/main.py

run_local: ## Build and run the application in local mode !!you need run the application by yorself!!
	docker-compose --env-file ./env.env -f docker-compose.dev.yml up --build -d

restart: down run ## Rebuild all application

## @ Migration Commands
upgrade:
	poetry run alembic upgrade head

revision:
	poetry run alembic revision --autogenerate

## @ Tests Commands
test: ## Run tests
	poetry run pytest -v

## @ Utils Commands
requirements: ## Update requirements.txt
	poetry export --without  dev --output requirements.txt --without-hashes

format: ## Run autoformatting and linting
	poetry run ruff check ./ --fix
