from django.urls import path
from . import views

app_name = "posicao"

urlpatterns = [                
    path('rede/', views.PosicaoListView.as_view(), name='rede-list'),
    path('rede/create/', views.PosicaoCreateView.as_view(), name='rede-create'),
    path('rede/<uuid:rede_de_localizacao_uuid>/update/', views.PosicaoUpdateView.as_view(), name="rede-update"),
]
