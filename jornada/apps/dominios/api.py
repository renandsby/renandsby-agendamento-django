from rest_framework import generics
from rest_framework import serializers
from dominios.models import Cidade, Bairro

class CidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cidade
        fields = ('codigo', 'nome', 'uf',)
        

class CidadeViewSet(generics.ListAPIView):
    queryset = Cidade.objects.all()
    serializer_class = CidadeSerializer
    filter_fields = ('codigo', 'nome', 'uf',)
    
    def paginate_queryset(self, queryset):
        if self.paginator and self.request.query_params.get(self.paginator.offset_query_param, None) is None:
            return None
        return super().paginate_queryset(queryset)
        

class BairroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bairro
        fields = ('id', 'nome', 'cidade', 'codigo',)


class BairroViewSet(generics.ListAPIView):
    queryset = Bairro.objects.all()
    serializer_class = BairroSerializer
    filter_fields = ('id', 'nome', 'cidade', 'codigo',)
    
    def paginate_queryset(self, queryset):
        if self.paginator and self.request.query_params.get(self.paginator.offset_query_param, None) is None:
            return None
        return super().paginate_queryset(queryset)