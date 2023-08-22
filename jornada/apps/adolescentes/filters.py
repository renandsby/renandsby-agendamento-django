import django_filters
from django.db.models import Q

from .models import Adolescente


class AdolescenteFilterSet(django_filters.FilterSet):
    nome = django_filters.CharFilter(
        field_name="nome", lookup_expr="unaccent__icontains", label="Nome"
    )
    nome_mae = django_filters.CharFilter(
        field_name="nome_mae", lookup_expr="icontains", label="Nome Mãe"
    )

    class Meta:
        model = Adolescente
        fields = ("nome", "data_nascimento", "nome_mae", "sipia")
