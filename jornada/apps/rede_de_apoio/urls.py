from django.urls import path
from . import views

app_name = "rede_de_apoio"

urlpatterns = [                
    path('rede/', views.RedeDeApoioListView.as_view(), name='rede-list'),
    path('rede/create/', views.RedeDeApoioCreateView.as_view(), name='rede-create'),
    path('rede/<uuid:unidade_de_apoio_uuid>/update/', views.RedeDeApoioUpdateView.as_view(), name="rede-update"),
]
