from django.urls import path
from .api import QuartoViewSet, unidade_adolescente, tipo_vaga_unidade


urlpatterns = [ 
    path("quarto/", QuartoViewSet.as_view(), name='api-quarto-list'),
    path("unidade/", unidade_adolescente, name="api-unidade-adolescente"),
    path("tiposvagaunidade/", tipo_vaga_unidade, name="api-unidade-tipo-vaga")
]