import django_filters
from django.db.models import Q

from .models import AtendimentoPsicossocial
from dominios.models import TipoAtendimentoPsicossocial,EspecialidadeAtendimentoPsicossocial



def multiple_search(queryset, name, value):
    queryset = queryset.filter(Q(tipo_atendimento__descricao__icontains=value)
            ) 
    return queryset

class AtendimentoPsicossocialFilterSet(django_filters.FilterSet):
    busca = django_filters.CharFilter(label="Buscar", method=multiple_search)
    tipo_atendimento = django_filters.ModelChoiceFilter(label="Tipo Atendimento", queryset=TipoAtendimentoPsicossocial.objects.all(), empty_label="Todos")
    especialidade_atendimento = django_filters.ModelChoiceFilter(label="Especialidade Atendimento", queryset=EspecialidadeAtendimentoPsicossocial.objects.all(), empty_label="Todos")
    class Meta:
        model = AtendimentoPsicossocial
        fields = ("busca",)
