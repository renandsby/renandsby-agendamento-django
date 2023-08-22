from django.urls import path, include
from . import views 

app_name = "uama"

urlpatterns = [                

        # Redireciona para a Unidade do usuário que fez o request
        path('modulo/<modulo_uuid>/uamaadolescentes', views.AdolescenteListView.as_view(), name="adolescente-list"),
        
]