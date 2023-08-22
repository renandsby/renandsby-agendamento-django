from django.conf.urls import include
from django.urls import path

from . import views

app_name = "prontuario"

urlpatterns = [
    # DADOS PESSOAIS
    path(
        "adolescente/",
        include(
            [
                path(
                    "",
                    views.AdolescenteProntuarioListView.as_view(),
                    name="adolescente-list",
                ),
                path(
                    "create/",
                    views.AdolescenteProntuarioCreateView.as_view(),
                    name="adolescente-create",
                ),
                path(
                    "<uuid:adolescente_uuid>/update",
                    views.AdolescenteProntuarioUpdateView.as_view(),
                    name="adolescente-update",
                ),
                path(
                    "<uuid:adolescente_uuid>/detail",
                    views.AdolescenteProntuarioDetailView.as_view(),
                    name="adolescente-detail",
                ),
                path(
                    "<uuid:adolescente_uuid>/detail-to-print",
                    views.AdolescenteProntuarioToPrintDetailView.as_view(),
                    name="adolescente-detail-to-print",
                ),
            ]
        ),
    ),
    # ENDERECOS
    path(
        "adolescente/<uuid:adolescente_uuid>/endereco/",
        include(
            [
                path(
                    "", views.EnderecoProntuarioListView.as_view(), name="endereco-list"
                ),
                path(
                    "create/",
                    views.EnderecoProntuarioCreateView.as_view(),
                    name="endereco-create",
                ),
                path(
                    "<uuid:endereco_uuid>/update",
                    views.EnderecoProntuarioUpdateView.as_view(),
                    name="endereco-update",
                ),
            ]
        ),
    ),


    # ATENDIMENTO PSICOSSOCIAL
    path(
        "adolescente/<uuid:adolescente_uuid>/atendimento-psicossocial/",
        include(
            [
                path(
                    "",
                    views.AtendimentoPsicossocialProntuarioListView.as_view(),
                    name="atendimento-psicossocial-list",
                ),
                path(
                    "create/",
                    views.AtendimentoPsicossocialProntuarioCreateView.as_view(),
                    name="atendimento-psicossocial-create",
                ),
                path(
                    "<uuid:atend_uuid>/update",
                    views.AtendimentoPsicossocialProntuarioUpdateView.as_view(),
                    name="atendimento-psicossocial-update",
                ),
            ]
        ),
    ),
    # EDUCACAO
    path(
        "adolescente/<uuid:adolescente_uuid>/educacao/",
        include(
            [
                path(
                    "", views.EducacaoProntuarioListView.as_view(), name="educacao-list"
                ),
                path(
                    "create/",
                    views.EducacaoProntuarioCreateView.as_view(),
                    name="educacao-create",
                ),
                path(
                    "<uuid:edu_uuid>/update",
                    views.EducacaoProntuarioUpdateView.as_view(),
                    name="educacao-update",
                ),
            ]
        ),
    ),
    # HISTÓRICO ENTRADA EM UNIDADES
    path(
        "adolescente/<uuid:adolescente_uuid>/historico/",
        include(
            [
                path("", views.HistoricoListView.as_view(), name="historico-list"),
            ]
        ),
    ),
    
     # HISTÓRICO Ocorrencias
    path(
        "adolescente/<uuid:adolescente_uuid>/ocorrencia/",
        include(
            [
                path("", views.OcorrenciaProntuarioListView.as_view(), name="ocorrencia-list"),
                # ver ocorrencia
                path("<uuid:ocorrencia_uuid>/detail/", views.OcorrenciaProntuarioDetailView.as_view(), name="ocorrencia-detail"),
            ]
        ),
    ),

    # PROCESSOS
    path(
        "adolescente/<uuid:adolescente_uuid>/processo/",
        include(
            [
                path(
                    "", views.ProcessoProntuarioListView.as_view(), name="processo-list"
                ),
                path(
                    "create/",
                    views.ProcessoProntuarioCreateView.as_view(),
                    name="processo-create",
                ),
                path(
                    "<uuid:processo_uuid>/update",
                    views.ProcessoProntuarioUpdateView.as_view(),
                    name="processo-update",
                ),
                path(
                    "<uuid:processo_uuid>/delete",
                    views.ProcessoProntuarioDeleteView.as_view(),
                    name="processo-delete",
                ),
            ]
        ),
    ),
    # RISCO
    path(
        "adolescente/<uuid:adolescente_uuid>/risco/",
        include(
            [
                path("", views.RiscoProntuarioListView.as_view(), name="risco-list"),
                path(
                    "create/",
                    views.RiscoProntuarioCreateView.as_view(),
                    name="risco-create",
                ),
                path(
                    "<uuid:risco_uuid>/update",
                    views.RiscoProntuarioUpdateView.as_view(),
                    name="risco-update",
                ),
            ]
        ),
    ),
    ## RELATÓRIOS
    path(
        "adolescente/<uuid:adolescente_uuid>/relatorio/",
        include(
            [
                path("", views.RelatorioProntuarioListView.as_view(), name='relatorio-list'),
                path(
                    "create/",
                    views.RelatorioProntuarioCreateView.as_view(),
                    name='relatorio-create',
                ),
                path(
                    "<uuid:relatorio_uuid>/update",
                    views.RelatorioProntuarioUpdateView.as_view(),
                    name='relatorio-update',
                ),
                path(
                    "<uuid:relatorio_uuid>/delete",
                    views.RelatorioProntuarioDeleteView.as_view(),
                    name="relatorio-delete",
                ),
            ]
        ),
    )
]
