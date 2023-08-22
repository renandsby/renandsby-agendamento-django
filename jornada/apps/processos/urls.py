from django.urls import path
from .api import ProcessoViewSet


urlpatterns = [ path("", ProcessoViewSet.as_view(), name='api-processo-list') ]
