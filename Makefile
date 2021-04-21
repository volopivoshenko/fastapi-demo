PY = python3
VENV = venv
BIN=$(VENV)/bin
DB_CONTAINER = postgres
DB_PWD = docker
DB_PORT = 5432

ifeq ($(OS), Windows_NT)
    BIN=$(VENV)/Scripts
    PY=python
endif


conda-env:
	conda env create -f conda-environment.yaml
	conda activate fastapi-demo

py-env:
	$(PY) -m venv $(VENV)
	$(BIN)/pip install --upgrade -r requirements.txt
	$(BIN)/activate

run-postgres:
	echo 'DB_CONNECTION_STRING=postgresql://$(DB_CONTAINER):$(DB_PWD)@localhost:$(DB_PORT)/$(DB_CONTAINER)' >> .env
	docker run --rm --name $(DB_CONTAINER) -e POSTGRES_PASSWORD=$(DB_PWD) -d -p $(DB_PORT):$(DB_PORT) -v ~/postgres:/var/lib/postgresql/data postgres

populate-db:
	python src/populate.py

graphql:
	python src/graphql_example.py

ml:
	python src/ml_model_example.py