from django.urls import path
from . import views

app_name = "tjdft"

urlpatterns = [                
        path('solicitacao/', views.SolicitacaoTJDFTListView.as_view(), name='solicitacao-list'),
        path('solicitacao/create/', views.SolicitacaoTJDFTCreateView.as_view(), name='solicitacao-create'),
        path('solicitacao/<uuid:solicitacao_uuid>/update/', views.SolicitacaoTJDFTUpdateView.as_view(), name="solicitacao-update"),
        path('solicitacao/<uuid:solicitacao_uuid>/delete/', views.SolicitacaoTJDFTDeleteView.as_view(), name="solicitacao-delete"),
]
