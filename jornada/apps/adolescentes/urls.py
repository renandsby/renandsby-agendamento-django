from django.urls import path
from .api import VisitanteViewSet, TelefoneViewSet


urlpatterns = [ 
    path("visitante/", VisitanteViewSet.as_view(), name='api-visitante-list'),
    path("telefone/", TelefoneViewSet.as_view(), name='api-telefone-list'),
]