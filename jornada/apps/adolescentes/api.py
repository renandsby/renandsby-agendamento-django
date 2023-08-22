from rest_framework import generics
from rest_framework import serializers
from .models import Familiar, Telefone


class FamiliarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Familiar
        fields = '__all__'

class TelefoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Telefone
        fields = '__all__'

class VisitanteViewSet(generics.ListAPIView):
    queryset = Familiar.objects.all()
    serializer_class = FamiliarSerializer
    filter_fields = ('adolescente',)
    
    def get_queryset(self):
        return super().get_queryset().filter(visitante_autorizado=True)



class TelefoneViewSet(generics.ListAPIView):
    queryset = Telefone.objects.all()
    serializer_class = TelefoneSerializer
    filter_fields = ('adolescente',)
    
    def get_queryset(self):
        return super().get_queryset().filter(autorizado=True)


