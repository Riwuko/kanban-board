DOCKER_EXEC=docker exec -it web

# Create and setup docker containers
build:
	docker-compose build


# Stop and remove containers
clean:
	docker-compose down


# Run a command inside web container
docker:
	$(DOCKER_EXEC) $(command)

# Run formatting with black and prettier
format:
	pre-commit run -a

# See logs for intranet
logs:
	docker-compose logs -f


rebuild:
	@make clean
	@make build



# Set LOGS=true if you want run dev environment with outputting logs
run:
	docker-compose up


# Docker stop
stop:
	docker-compose stop
