db_up:
	docker-compose --env-file ./.env up -d

db_down:
	docker-compose down --volumes

db_start:
	docker-compose start db

db_stop:
	docker-compose stop db

db_logs: db_start
	docker-compose logs -f db

db_destroy: db_stop db_down
	docker volume rm jornada_pg_data --force

network:
	docker network create --driver=bridge jornada_backend