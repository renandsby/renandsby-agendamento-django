from django.urls import include, path

from . import (
    views,
    agendamentos,
    atividades,
    ocorrencias,
    visitas,
    chegadas_saidas, 
    historico_unidade,
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
                
                # Timeline de Atividades do Adolescente
                path(
                    "entrada/<uuid:entrada_uuid>/timelineatividades/",
                    atividades.views.ModuloTimelineAdolescente.as_view(),
                    name="adolescente-historico-atividade",
                ),
                ### ENVIO DE ADOLESCENTES PARA ATIVIDADES
                # Lista de Atividades do Módulo
                path(
                    "atividade/",
                    views.ModuloAtividadeListView.as_view(),
                    name="modulo-atividades",
                ),
                # Primeira Tela de Envio de Adolescentes para Atividade
                path(
                    "atividade/<uuid:atividade_uuid>/enviaradolescentes/",
                    atividades.views.ModuloAtividadeEnviarAdolescentesView.as_view(),
                    name="modulo-atividade-enviar-adolescentes",
                ),
                # Segunda Tela de Envio de Adolescentes para Atividade
                path(
                    "atividade/<uuid:atividade_uuid>/enviarmultiplos/",
                    atividades.views.ModuloAtividadeEnviarAdolescentesConfirmaView.as_view(),
                    name="modulo-atividade-enviar-multiplos-adolescentes",
                ),
                # Segunda Tela de Retorno de Adolescentes de Atividade
                path(
                    "atividade/<uuid:atividade_uuid>/retornaradolescentes/",
                    atividades.views.ModuloAtividadeRetornarAdolescentesView.as_view(),
                    name="modulo-atividade-retornar-adolescentes",
                ),
                # Segunda Tela de Retorno de Adolescentes de Atividade
                path(
                    "atividade/<uuid:atividade_uuid>/retornarmultiplos/",
                    atividades.views.ModuloAtividadeRetornarAdolescentesConfirmaView.as_view(),
                    name="modulo-atividade-retornar-multiplos-adolescentes",
                ),
                ### CRUD HISTORICO DE ATIVIDADE
                # Lista o Histórico de Idas para uma Atividade
                path(
                    "atividade/<uuid:atividade_uuid>/historico/",
                    atividades.views.ModuloAtividadeHistoricoListView.as_view(),
                    name="modulo-atividade-historico",
                ),
                # Edita o Histórico de Ida para uma Atividade
                path(
                    "historico/<uuid:historico_uuid>/update",
                    atividades.views.ModuloAtividadeHistoricoUpdateView.as_view(),
                    name="modulo-atividade-historico-update",
                ),
                # Deleta o Histórico de Ida para uma Atividade
                path(
                    "historico/<uuid:historico_uuid>/delete/",
                    atividades.views.ModuloAtividadeHistoricoDeleteView.as_view(),
                    name="modulo-atividade-historico-delete",
                ),
                ### AGENDAMENTOS
                # Cadastro Multiplo de Agendamento
                path(
                    "cadastraragendamento/",
                    agendamentos.views.ModuloAgendamentoCriaMultiplosView.as_view(),
                    name="modulo-atividade-cadastrar-agendamentos",
                ),
                # Listar Agendamentos
                path(
                    "listaragendamento/",
                    agendamentos.views.ModuloAgendamentoListView.as_view(),
                    name="modulo-listar-agendamentos",
                ),
                # Editar Agendamento Único
                path(
                    "historico/<uuid:historico_uuid>/editaagendamento",
                    agendamentos.views.ModuloAgendamentoUpdateView.as_view(),
                    name="modulo-agendamento-editar",
                ),
                # Deletar Agendamento
                path(
                    "historico/<uuid:historico_uuid>/agendamentodelete/",
                    agendamentos.views.ModuloAgendamentoDeleteView.as_view(),
                    name="modulo-agendamento-delete",
                ),
                # Enviar Adolescente a partir de Agendamento
                path(
                    "historico/<uuid:historico_uuid>/enviaragendado",
                    agendamentos.views.ModuloAgendamentoEnviarUpdateView.as_view(),
                    name="modulo-agendamento-enviar",
                ),
                # Retornar Adolescente a partir de Agendamento
                path(
                    "historico/<uuid:historico_uuid>/retornaragendado",
                    agendamentos.views.ModuloAgendamentoRetornarUpdateView.as_view(),
                    name="modulo-agendamento-retornar",
                ),
                ### OCORRÊNCIAS
                # Listar Ocorrências
                path(
                    "ocorrencia/",
                    ocorrencias.views.ModuloOcorrenciaListView.as_view(),
                    name="modulo-ocorrencia-list",
                ),
                # Criar Ocorrência
                path(
                    "ocorrencia/create/",
                    ocorrencias.views.ModuloOcorrenciaCreateView.as_view(),
                    name="modulo-ocorrencia-create",
                ),
                # Editar Ocorrência
                path(
                    "ocorrencia/<uuid:ocorrencia_uuid>/update/",
                    ocorrencias.views.ModuloOcorrenciaUpdateView.as_view(),
                    name="modulo-ocorrencia-update",
                ),
                
                ### VISITAS
                # Listar Visitas
                path(
                    "visita/",
                    visitas.views.ModuloVisitaListView.as_view(),
                    name="modulo-visita-list",
                ),
                # Criar Visita
                path(
                    "visita/create/",
                    visitas.views.ModuloVisitaCreateView.as_view(),
                    name="modulo-visita-create",
                ),
                # Editar Visita
                path(
                    "visita/<uuid:visita_uuid>/update/",
                    visitas.views.ModuloVisitaUpdateView.as_view(),
                    name="modulo-visita-update",
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
                    "historico/",
                    historico_unidade.views.HistoricoUnidadeListView.as_view(),
                    name="historico-unidade",
                ),
                # Listagem de Módulos
                path(
                    "modulos/",
                    views.HomeModuloView.as_view(),
                    name="home-modulos",
                ),
                ### CHEGADAS PREVISAS
                path(
                    "acautelamento/",
                    chegadas_saidas.views.AdministradorAcautelamentoListView.as_view(),
                    name="acautelamento-list",
                ),
                path(
                    "acautelamento/<uuid:entrada_uuid>/",
                    chegadas_saidas.views.AdministradorAcautelamentoUpdateView.as_view(),
                    name="acautelamento",
                ),
                
                ### SAIDAS PREVISTAS
                path(
                    "saida/",
                    chegadas_saidas.views.AdministradorSaidaListView.as_view(),
                    name="saida-list",
                ),
                path(
                    "saida/<uuid:entrada_uuid>/saida/",
                    chegadas_saidas.views.AdministradorSaidaView.as_view(),
                    name="saida",
                ),
                
                ### EDITAR ATIVIDADES
                path(
                    "editaratividade/",
                    atividades.views.AdministradorAtividadeListView.as_view(),
                    name="atividade-list",
                ),
                path(
                    "editaratividade/create/",
                    atividades.views.AdministradorAtividadeCreateView.as_view(),
                    name="atividade-create",
                ),
                path(
                    "editaratividade/<uuid:atividade_uuid>/update/",
                    atividades.views.AdministradorAtividadeUpdateView.as_view(),
                    name="atividade-update",
                ),
                
              
                ### EFETIVO GERAL
                path(
                    "efetivo_geral/",
                    chegadas_saidas.views.EfetivoGeralListView.as_view(),
                    name="efetivo-geral-list",
                ),
                path(
                    "entrada/<uuid:entrada_uuid>/update/",
                    chegadas_saidas.views.AdministradorEntradaUpdateView.as_view(),
                    name="efetivo-geral-update-entrada",
                ),    
                
            ]
        ),
    ),
]
