# Here if the command is dump, app or test, the script will capture ARG parameter
ifneq ($(filter $(MAKECMDGOALS), dump app test module),) 
	ARG := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
	$(eval $(ARG):;@:)
endif

setup: destroy destroy_db build start remove_migrations migrations migrate populate_grupos populate_base vincula_randomicos testa_aplicacao
	@echo "Local deploy set up!!"

build:
	docker-compose --env-file ./.env up --build -d

destroy: stop
	docker-compose down --rmi local 

destroy_db: stop
	docker volume rm jornada_pg_data --force


start:
	docker-compose start
	
stop:
	docker-compose stop 

restart: stop start
	@echo "Restarted containers!"

migrations:
	docker-compose exec django django-admin makemigrations 

migrate:
	docker-compose exec django django-admin migrate

superuser:
	docker-compose exec django django-admin createsuperuser --no-input

logs: start
	docker-compose logs -f django

populate_grupos:
	docker-compose exec django django-admin populate -f ./fixtures/grupos

populate_base:
	docker-compose exec django django-admin populate -f ./fixtures/base
	
app:
	docker-compose exec django django-admin startapp $(NAME) \
	&& sudo mv ../$(NAME) ../jornada/apps \
	&& sudo mkdir ../jornada/apps/$(NAME)/templates \
	&& sudo mkdir ../jornada/apps/$(NAME)/templates/$(NAME) \
	&& sudo chown -R $(USER): ../jornada/apps/$(NAME)

dump:
	docker-compose exec django django-admin dumpdata $(ARG) > ../fixtures/$(num)-$(ARG).json

shell: 
	docker-compose exec django django-admin shell_plus

show_urls: 
	docker-compose exec django django-admin show_urls	

test:
	docker-compose exec django django-admin test $(ARG) 

network:
	docker network create --driver=bridge jornada_backend

remove_migrations:
	docker-compose exec -T django django-admin shell < ../scripts/remove_migrations.py


vincula_randomicos:
	docker-compose exec django django-admin vincula_randomicos --qtd 1 --lotado True \
	&& docker-compose exec django django-admin vincula_randomicos --qtd 2

