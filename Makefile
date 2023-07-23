#!make


#.PHONY: start
run:
	# Remove all containers and volumes created by this Docker Compose file.
	# docker-compose --env-file ./config/docker/env.dev rm -s -f -v 
	# Prune unused volumes.
	docker volume prune -f
	docker-compose --file docker-compose.yml --env-file ./config/docker/env.dev up \
		--remove-orphans --build --abort-on-container-exit --exit-code-from default

test:
	# Remove all containers and volumes created by this Docker Compose file.
	# docker-compose --env-file ./config/docker/env.dev rm -s -f -v 
	# Prune unused volumes.
	docker volume prune -f
	docker-compose --file docker-compose.test.yml --env-file ./config/docker/env.dev up \
	--remove-orphans --build --abort-on-container-exit --exit-code-from api

black-check:
	docker-compose --file docker-compose.inspect.yml --file docker/overrides/docker-compose.override.black-check.yml --env-file ./config/docker/env.dev up --remove-orphans --build --abort-on-container-exit --exit-code-from api 

black-format:
	docker-compose --file docker-compose.inspect.yml --file docker/overrides/docker-compose.override.black-format.yml up --remove-orphans --build --abort-on-container-exit --exit-code-from api 

mypy:
	docker-compose --file docker-compose.inspect.yml --file docker/overrides/docker-compose.override.mypy.yml up --remove-orphans --build --abort-on-container-exit --exit-code-from api

bandit:
	docker-compose --file docker-compose.inspect.yml --file docker/overrides/docker-compose.override.bandit.yml up --remove-orphans --build --abort-on-container-exit --exit-code-from api

