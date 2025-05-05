.PHONY: start stop logs clean

start:
	@echo "Starting pipeline..."
	@docker-compose up -d

stop:
	@echo "Stopping pipeline..."
	@docker-compose down

logs:
	@docker logs -f kraken-kafka-producer-1

clean:
	@echo "Cleaning up..."
	@docker-compose down -v --rmi all