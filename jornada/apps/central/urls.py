from django.urls import path
from . import views, painel_vagas
from .painel_vagas import views as painel_vagas_views

app_name = "central"



urlpatterns = [            
        # PAINEL DE VAGAS    
        path('vagas/', painel_vagas_views.VagasView.as_view(), name="resumo-vagas"),
        path('unidade/<uuid:unidade_uuid>/adolescentes/', painel_vagas_views.UnidadeAdolescentesView.as_view(), name="unidade-adolescentes"),
        

        # VINCULAÇÃO
        path('vinculacao/', views.VinculacaoCentralListView.as_view(), name='vinculacao-list'),
        path('vinculacao/create/', views.VinculacaoCentralCreateView.as_view(), name='vinculacao-create'),
        path('vinculacao/<uuid:vinculacao_uuid>/vincular', views.VincularCentralView.as_view(), name="vinculacao-vincular"),
        path('vinculacao/<uuid:vinculacao_uuid>/update/', views.VinculacaoCentralUpdateView.as_view(), name="vinculacao-update"),
        path('vinculacao/<uuid:vinculacao_uuid>/delete/', views.VinculacaoCentralDeleteView.as_view(), name="vinculacao-delete"),
        path('vinculacao/<uuid:vinculacao_uuid>/desfazer', views.VinculacaoCentralDesfazerView.as_view(), name="vinculacao-desfazer"),
        path('vinculacao/<uuid:vinculacao_uuid>/cancelar', views.VinculacaoCentralCancelarView.as_view(), name="vinculacao-cancelar"),


        # TRANSFERÊNCIA
        path('transferencia/', views.TransferenciaCentralListView.as_view(), name='transferencia-list'),
        path('transferencia/create/', views.TransferenciaCentralCreateView.as_view(), name='transferencia-create'),
        path('transferencia/<uuid:transferencia_uuid>/transferir', views.TransferirCentralView.as_view(), name="transferencia-transferir"),
        path('transferencia/<uuid:transferencia_uuid>/update/', views.TransferenciaCentralUpdateView.as_view(), name="transferencia-update"),
        path('transferencia/<uuid:transferencia_uuid>/delete/', views.TransferenciaCentralDeleteView.as_view(), name="transferencia-delete"),
        path('transferencia/<uuid:transferencia_uuid>/desfazer/', views.TransferenciaCentralDesfazerView.as_view(), name="transferencia-desfazer"),
        path('transferencia/<uuid:transferencia_uuid>/cancelar/', views.TransferenciaCentralCancelarView.as_view(), name="transferencia-cancelar"),

        # DESVINCULAÇÃO
        path('desvinculacao/', views.DesvinculacaoCentralListView.as_view(), name='desvinculacao-list'),
        path('desvinculacao/create/', views.DesvinculacaoCentralCreateView.as_view(), name='desvinculacao-create'),
        path('desvinculacao/<uuid:desvinculacao_uuid>/desvincular', views.DesvincularCentralView.as_view(), name="desvinculacao-desvincular"),
        path('desvinculacao/<uuid:desvinculacao_uuid>/update/', views.DesvinculacaoCentralUpdateView.as_view(), name="desvinculacao-update"),
        path('desvinculacao/<uuid:desvinculacao_uuid>/delete/', views.DesvinculacaoCentralDeleteView.as_view(), name="desvinculacao-delete"),
        path('desvinculacao/<uuid:desvinculacao_uuid>/desfazer/', views.DesvinculacaoCentralDesfazerView.as_view(), name="desvinculacao-desfazer"),
        path('desvinculacao/<uuid:desvinculacao_uuid>/cancelar/', views.DesvinculacaoCentralCancelarView.as_view(), name="desvinculacao-cancelar"),

]
