from django.urls import path

from . import views

app_name = 'nai'

urlpatterns = [
        path('modulo/<uuid:modulo_uuid>/efetivonai/', views.EfetivoNaiView.as_view(), name='efetivo-nai'),
        path('modulo/<uuid:modulo_uuid>/entrada/<uuid:entrada_uuid>/saida/', views.NaiSaidaView.as_view(), name='efetivo-nai-retirar'),
        path('modulo/<uuid:modulo_uuid>/entrada/<uuid:entrada_uuid>/editaquarto/', views.NaiEditaQuartoView.as_view(), name='efetivo-nai-edita-quarto'),
        path('modulo/<uuid:modulo_uuid>/acautelamento/create/', views.NaiIncluirAdolescenteEntradaView.as_view(), name='efetivo-nai-incluir'),
]
