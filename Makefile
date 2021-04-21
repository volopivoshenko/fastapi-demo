db_container_name = postgres
db_pwd = docker
db_port = 5432

run-postgres:
	echo 'DB_CONNECTION_STRING=postgresql://$(db_container_name):$(db_pwd)@localhost:$(db_port)/$(db_container_name)' >> .env
	docker run --rm --name $(db_container_name) -e POSTGRES_PASSWORD=$(db_pwd) -d -p $(db_port):$(db_port) -v ~/postgres:/var/lib/postgresql/data postgres

create-env:
	conda env create -f conda-environment.yaml
	conda activate fastapi-demo

populate-db:
	python src/populate.py