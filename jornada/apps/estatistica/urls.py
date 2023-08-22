from django.urls import include, path
from estatistica.views import (
    adolescente_por_genero,
    adolescente_por_ra,
    dashboard_avancado_por_idade,
    dashboard_avancado_situacao_escolar_por_ra,
    dashboard_avancado_situacao_escolar_por_unidade,
    dashboard_avancado_tipo_atividade,
    dashboard_avancado_tipo_entrada,
    dashboard_esp_atividades,
    dashboard_esp_internacao_unidades,
    dashboard_esp_motivo_entrada,
    dashboard_estatistica,
    dashboard_geral,
    dashboard_esp_situacao_escolar,
)

app_name = "estatistica"

urlpatterns = [
    path(
        "dashboard/",
        dashboard_estatistica.DashboardEstatistica.as_view(),
        name="dashboard_estatistica",
    ),
    #    path('dashboard/teste/', dashboard_geral.DashboardGeral.as_view(), name="dashboard_geral",
    #   ),
    path(
        "dashboard/geral/",
        dashboard_geral.DashboardGeral.as_view(),
        name="dashboard_geral",
    ),
    path(
        "dashboard/avancado/tipo_entrada",
        dashboard_esp_motivo_entrada.DashboardEspMotivoEntrada.as_view(),
        name="dashboard_esp_tipo_entrada",
    ),
    path(
        "dashboard/avancado/internacao_unidades",
        dashboard_esp_internacao_unidades.DashboardEspecificoInternacaoUnidades.as_view(),
        name="dashboard_esp_internacao_unidades",
    ),
    path(
        "dashboard/avancado/atividades",
        dashboard_esp_atividades.DashboardEspAtividades.as_view(),
        name="dashboard_esp_atividades",
    ),
    path(
        "dashboard/avancado/poridade/",
        dashboard_avancado_por_idade.DashboardAvancadoPorIdade.as_view(),
        name="dashboard_avancado_por_idade",
    ),
    path(
        "dashboard/avancado/tipoentrada/",
        dashboard_avancado_tipo_entrada.DashboardAvancadoTipoEntrada.as_view(),
        name="dashboard_avancado_tipo_entrada",
    ),
    path(
        "dashboard/avancado/tipoatividade/",
        dashboard_avancado_tipo_atividade.DashboardAvancadoTipoAtividade.as_view(),
        name="dashboard_avancado_tipo_atividade",
    ),
    path(
        "dashboard/avancado/situacao-escolar/",
        dashboard_esp_situacao_escolar.DashboardEspSituacaoEscolar.as_view(),
        name="dashboard_esp_situacao_escolar",
    ),
    path(
        "dashboard/avancado/situacao-escolar-por-unidade/",
        dashboard_avancado_situacao_escolar_por_unidade.DashboardAvancadoSituacaoEscolarPorUnidade.as_view(),
        name="dashboard_avancado_situacao_escolar_por_unidade",
    ),
    #    path(
    #        "dashboard/avancado/situacao-escolar-por-ra/",
    #        dashboard_avancado_situacao_escolar_por_ra.DashboardAvancadoSituacaoEscolarPorRa.as_view(),
    #        name="dashboard_avancado_situacao_escolar_por_ra",
    #    ),
    path(
        "dashboard/avancado/adolescente_ra/",
        adolescente_por_ra.AdolescentePorRa.as_view(),
        name="adolescente_por_ra",
    ),
    path(
        "dashboard/avancado/adolescente_genero/",
        adolescente_por_genero.AdolescentePorGenero.as_view(),
        name="adolescente_por_genero",
    ),
    path("django_plotly_dash/", include("django_plotly_dash.urls")),
]
