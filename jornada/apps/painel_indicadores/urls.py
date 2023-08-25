from django.urls import include, path

from . import (
    views,
)

app_name ="painel_indicadores"

urlpatterns = [
    # Redireciona para a Unidade do usuário que fez o request
    path("", views.PainelIndicadoresRedirectView.as_view(), name="home"),
    
    # Listagem de Unidades
    path(
        "", views.HomePainelIndicadorView.as_view(), name="painel-list",
    ),
    
  
    
    # UNIDADE
    path(
        "",
        include(
            [   

                # Listagem de Módulos
                path(
                    "",
                    views.HomeModuloView.as_view(),
                    name="home-modulos",
                ),
              
              
            ]
        ),
    ),
]
