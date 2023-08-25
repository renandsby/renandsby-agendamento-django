import django_filters
from django.db.models import Q
from .models import Agendamento


def multiple_search(queryset, name, value):
    return queryset.filter(Q(agendamento__name__icontains=value))

