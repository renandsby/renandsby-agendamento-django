from django.urls import include, path

from . import (
    views,
)

app_name = "rotina_modulo"

urlpatterns = [
    # Redireciona para a Unidade do usuário que fez o request
    path("", views.UnidadeRedirectView.as_view(), name="home"),
    
    # Listagem de Unidades
    path(
        "unidade/",
        views.HomeUnidadeView.as_view(),
        name="home-unidades",
    ),
    # MÓDULO
  
    
    # UNIDADE
    path(
        "unidade/<uuid:unidade_uuid>/",
        include(
            [   

                # Listagem de Módulos
                path(
                    "painel/",
                    views.HomeModuloView.as_view(),
                    name="home-modulos",
                ),
              
              
            ]
        ),
    ),
]
