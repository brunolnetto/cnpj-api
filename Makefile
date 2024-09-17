.PHONY: build run stop ps host logs

OMIT_PATHS := "*/__init__.py,backend/tests/*,backend/app/repositories/cnpj.py,backend/app/database/base.py,backend/app/api/services/scrapper.py"

define PRINT_HELP_PYSCRIPT
import re, sys

regex_pattern = r'^([a-zA-Z_-]+):.*?## (.*)$$'

for line in sys.stdin:
	match = re.match(regex_pattern, line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

help:
	@python3 -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean-logs: # Removes log info. Usage: make clean-logs
	rm -fr build/ dist/ .eggs/
	find . -name '*.log' -o -name '*.log' -exec rm -fr {} +

clean-test: # Remove test and coverage artifacts
	rm -fr .tox/ .testmondata* .coverage coverage.* htmlcov/ .pytest_cache

clean-cache: # remove test and coverage artifacts
	find . -name '*pycache*' -exec rm -rf {} +
	find . -name '*_pycache*' -exec rm -rf {} +

sanitize: # Remove dangling images and volumes
	docker system prune --volumes -f
	docker images --filter 'dangling=true' -q --no-trunc | xargs -r docker rmi

clean: clean-logs clean-test clean-cache sanitize ## Add a rule to remove unnecessary assets. Usage: make clean

env: ## Creates a virtual environment. Usage: make env
	pip install virtualenv
	virtualenv .venv

install: ## Installs the python requirements. Usage: make install
	pip install uv
	uv pip install -r requirements.txt
	uv pip install -r requirements_dev.txt
	apt install black pylint

run: ## Run the application. Usage: make run
	uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000

search: ## Searchs for a token in the code. Usage: make search token=your_token
	grep -rnw . --exclude-dir=venv --exclude-dir=.git --exclude=poetry.lock -e "$(token)"

replace: ## Replaces a token in the code. Usage: make replace token=your_token
	sed -i 's/$(token)/$(new_token)/g' $$(grep -rl "$(token)" . \
		--exclude-dir=venv \
		--exclude-dir=.git \
		--exclude=poetry.lock)

test: ## Test the application. Usage: make test
	poetry run coverage run --rcfile=.coveragerc -m pytest

test-watch: ## Run tests on watchdog mode. Usage: make ptw-watch
	ptw --quiet --spool 200 --clear --nobeep --config pytest.ini --ext=.py --onfail="echo Tests failed, fix the issues"

report: test ## Generate coverage report. Usage: make report
	coverage report --omit=$(OMIT_PATHS) --show-missing

minimal-requirements: ## Generates minimal requirements. Usage: make requirements
	python3 scripts/clean_packages.py requirements.txt requirements.txt
	
lint: ## Perform inplace lint fixes. Usage: make lint
	@autopep8 --in-place --aggressive --aggressive $(shell git ls-files '*.py')
	@ruff check --unsafe-fixes --fix .
	@black $(shell git ls-files '*.py')

cloc-install: ## Installs row-count tool
	apt install cloc

cloc: ## Row count of code. Usage: make cloc
	cloc --by-percent=cmb --progress-rate=100 .

pylint:
	@pylint backend/

build-test: ## Build the test container image. Usage: make build
	docker compose -f docker-compose.test.yaml build

ps-test: ## List all running test containers. Usage: make ps
	docker compose -f docker-compose.test.yaml ps -a

up-test: ## Start the test application. Usage: make up
	docker compose -f docker-compose.test.yaml up -d

populate-test: ## Populate the test database. Usage: make populate-test
	docker cp data/sample_data.sql db:/var/lib/postgresql/data/sample_data.sql
	docker exec -it db psql -U postgres -d postgres -f /home/sample_data.sql

down-test: ## Stop the application. Usage: make down
	docker compose -f docker-compose.test.yaml down

logs-test: ## Logs the container. Usage: make logs
	docker compose -f docker-compose.test.yaml logs -f

restart-test: down-test build-test up-test ## Restart the test application. Usage: make restart

build: ## Build the container image. Usage: make build
	docker compose build

ps: ## List all running containers. Usage: make ps
	docker compose ps -a

up: ## Start the application. Usage: make up
	docker compose up -d

down: ## Stop the application. Usage: make down
	docker compose down

logs: ## Logs the container. Usage: make logs
	docker compose logs -f

restart: down build up ## Restart the application. Usage: make restart
