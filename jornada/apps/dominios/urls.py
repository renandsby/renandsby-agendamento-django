from django.urls import path, include
from django.apps import apps
from rest_framework import serializers
from rest_framework import generics
from .api import CidadeViewSet, BairroViewSet


urlpatterns = [ 
    path("cidade/", CidadeViewSet.as_view(), name='api-cidade-list'),
    path("bairro/", BairroViewSet.as_view(), name='api-bairro-list'),
]



# Gera urls genericas pra servir todos os dominios automaticamente

class GeneralSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'

class GenericAPIView(generics.ListAPIView):
    
    def dispatch(self, request, *args, **kwargs):
        self.model = kwargs.pop('model')
        self.queryset = self.model.objects.all()
        serializer = GeneralSerializer
        serializer.Meta.model = self.model
        self.serializer_class = serializer
        return super().dispatch(request, *args, **kwargs)

app = apps.get_app_config('dominios')

for model_name, model in app.models.items():
    # URLS de api são geradas automaticamente a partir do nome do model
    # Não gerar para os que foram adicionados anteriormentes
    urlpatterns.append(path(f"{model_name}/", GenericAPIView.as_view(), {'model': model}))
    

