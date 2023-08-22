from django.contrib import admin
from django.apps import apps
from dominios.models import Cor
app_models = apps.get_app_config('dominios').get_models()
for model in app_models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
