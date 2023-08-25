from django.conf.urls import include
from django.urls import path

from . import views

app_name = "dadosEmpresa"

urlpatterns = [
    # DADOS PESSOAIS
    path(
        "posicao/",
        include(
            [
                path(
                    "",
                    views.RedeDadosEmpresaListView.as_view(),
                    name="rede-list",
                ),
                path(
                    "create/",
                    views.RedeDadosEmpresaCreateView.as_view(),
                    name="rede-create",
                ),
                path(
                    "<uuid:rede_uuid>/update",
                    views.RedeDadosEmpresaUpdateView.as_view(),
                    name="rede-update",
                ),
                
            ]
        ),
    ),
    # ENDERECOS
    path(
        "posicao/<uuid:rede_uuid>/endereco/",
        include(
            [
                path(
                    "", views.EnderecoDadosEmpresaListView.as_view(), name="endereco-list"
                ),
                path(
                    "create/",
                    views.EnderecoDadosEmpresaCreateView.as_view(),
                    name="endereco-create",
                ),
                path(
                    "<uuid:endereco_uuid>/update",
                    views.EnderecoDadosEmpresaUpdateView.as_view(),
                    name="endereco-update",
                ),
            ]
        ),
    ),
   

   
]
