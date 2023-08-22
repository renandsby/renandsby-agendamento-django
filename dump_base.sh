#!/bin/bash
docker-compose exec django django-admin dumpdata dominios --natural-foreign --natural-primary > ../fixtures/base/1-dominios.json
docker-compose exec django django-admin dumpdata auth.group --natural-foreign --natural-primary > ../fixtures/base/2-auth.json
docker-compose exec django django-admin dumpdata custom_auth.customuser --natural-foreign --natural-primary > ../fixtures/base/3-users.json
docker-compose exec django django-admin dumpdata unidades.unidade unidades.vagaunidade unidades.modulo unidades.quarto > ../fixtures/base/4-base_unidades.json
docker-compose exec django django-admin dumpdata servidores --natural-foreign --natural-primary > ../fixtures/base/5-servidores.json