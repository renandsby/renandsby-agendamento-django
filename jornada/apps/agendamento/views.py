from typing import Any
from django.db import models
from django.views.generic import ListView, CreateView, UpdateView
from django.views.generic import View, ListView
from core.forms.mixins import InlineFormsetMixin
from core.views import FilteredViewMixin, UUIDViewMixin
from .models import Agendamento
from .forms import AgendamentoForm
from django.shortcuts import redirect, render
from django.urls.base import reverse


class AgendamentoListView(ListView):
    model = Agendamento
    template_name = "agendamento/agendamento_list_body.html"

    def get_queryset(self, **kwargs):
        queryset = Agendamento.objects.all() 
        return queryset.order_by('id')
    
    def get_success_url(self):
        return reverse('agendamento:agendamento-list')

class AgendamentoCreateView(
    CreateView
):
    model = Agendamento
    form_class = AgendamentoForm
    template_name = "agendamento/agendamento_form_body.html"

    def get_queryset(self):
        queryset = Agendamento.objects.all() 
        return queryset.order_by('id')

    def get_success_url(self):
        return reverse('agendamento:agendamento-list')

class AgendamentoUpdateView(
    UUIDViewMixin,
    UpdateView
):
    model = Agendamento
    form_class = AgendamentoForm
    uuid_url_kwarg = "agendamento_uuid"
    template_name = "agendamento/agendamento_form_body.html"
    
    def get_success_url(self):
        return reverse('agendamento:agendamento-list')
