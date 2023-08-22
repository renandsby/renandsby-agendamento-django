from rest_framework import generics
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from adolescentes.models import Adolescente
from dominios.models import TipoVagaUnidade
from .models import Quarto, Unidade


class QuartoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quarto
        fields = '__all__'


class QuartoViewSet(generics.ListAPIView):
    queryset = Quarto.objects.all()
    serializer_class = QuartoSerializer
    filter_fields = ('modulo',)


class UnidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unidade
        fields = ('id', 'sigla')


class TipoVagaUnidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoVagaUnidade
        fields = ('id', 'descricao')

def tipo_vaga_unidade(request):
    unidade_id = request.GET.get('unidade', None)
    if unidade_id:
        unidade = get_object_or_404(Unidade, pk=unidade_id)
        tipos_de_vaga_serializer = TipoVagaUnidadeSerializer(unidade.tipos_de_vaga).data
    return JsonResponse(tipos_de_vaga_serializer, safe=False)

def unidade_adolescente(request):
    adol_id = request.GET.get('adolescente', None)
    if adol_id:
        adolescente = get_object_or_404(Adolescente, pk=adol_id)
        unidade = UnidadeSerializer(adolescente.unidade_atual).data
    return JsonResponse(unidade, safe=False)

