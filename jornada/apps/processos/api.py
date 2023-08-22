from rest_framework import generics
from rest_framework import serializers
from processos.models import Processo

class ProcessoSerializer(serializers.ModelSerializer):
    adolescente = serializers.SerializerMethodField()
    str_sem_nome = serializers.ReadOnlyField()                  
    
    class Meta:
        model = Processo
        fields = ('id', 'adolescente', 'numero', 'str_sem_nome')
        
    def get_adolescente(self, obj):
        return obj.adolescente.nome


class ProcessoViewSet(generics.ListAPIView):
    queryset = Processo.objects.all()
    serializer_class = ProcessoSerializer
    filter_fields = ('id', 'adolescente','numero',)