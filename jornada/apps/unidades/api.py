from rest_framework import generics
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from .models import Quarto, Unidade


class QuartoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quarto
        fields = '__all__'




class UnidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unidade
        fields = ('id', 'sigla')





