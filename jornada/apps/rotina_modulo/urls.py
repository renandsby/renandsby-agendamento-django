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
    path(
        "modulo/<uuid:modulo_uuid>/",
        include(
            [
                # Listagem de Quartos
                path(
                    "quartos/",
                    views.ModuloQuartoListView.as_view(),
                    name="quartos-modulo",
                ),
                # Lista Adolescentes do Módulo/Unidade
                path(
                    "entrada/",
                    views.ModuloAdolescenteListView.as_view(),
                    name="modulo-entradas",
                ),
                
                #EDITA QUARTO
                path(
                    'entrada/<uuid:entrada_uuid>/editaquarto/', 
                    views.ModuloEditaQuartoView.as_view(), 
                    name='modulo-entradas-edita-quarto'
                ),
          
               
            
        
      
            ]
        ),
    ),
    
    
    # UNIDADE
    path(
        "unidade/<uuid:unidade_uuid>/",
        include(
            [   

                # Listagem de Módulos
                path(
                    "modulos/",
                    views.HomeModuloView.as_view(),
                    name="home-modulos",
                ),
              
              
            ]
        ),
    ),
]
