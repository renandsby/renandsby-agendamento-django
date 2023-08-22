import os, shutil
from django.apps import apps

# SCRIPT QUE REMOVE TODAS AS MIGRATIONS DE TODOS OS APPS DO SISTEMA


# COMO UTILIZAR ?
# 1 - colocar o CSV dentro da pasta scripts
# 2 - make restart
# 3 - docker-compose exec -T django django-admin shell < ../scripts/remove_migrations.py

print("removing migrations...")
for app in apps.app_configs.keys():
    
    if os.path.isdir(os.path.join('jornada','apps', app,'migrations')):    
        folder = os.path.join('jornada','apps', app,'migrations')
        if app != "custom_auth":
            for file in os.listdir(folder):
                
                if file != "__init__.py":
                    file_to_delete = os.path.join(folder,file)
                    
                    if os.path.isdir(file_to_delete):
                        shutil.rmtree(file_to_delete)
                        
                    if os.path.isfile(file_to_delete):
                        os.remove(file_to_delete)