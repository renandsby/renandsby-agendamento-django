from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls.base import reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.views import FilteredViewMixin, UUIDViewMixin
from dominios.models import Bairro
from .models import UnidadeDeApoio
from .filters import RedeDeApoioFilterSet
from .forms import UnidadeDeApoioForm


class RedeDeApoioListView(
    LoginRequiredMixin,
    FilteredViewMixin,
    ListView,
):
    model = UnidadeDeApoio
    filterset_class = RedeDeApoioFilterSet
    template_name = "rede_de_apoio/rede_list.html"

    def get_success_url(self):
        return reverse('rede_de_apoio:rede-list')
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        if 'bairro' in self.request.GET:
            if self.request.GET['bairro']:
                context['bairro'] = Bairro.objects.get(id=self.request.GET['bairro'])
        return context


class RedeDeApoioCreateView(
    LoginRequiredMixin,
    CreateView
):
    model = UnidadeDeApoio
    form_class = UnidadeDeApoioForm
    template_name = "rede_de_apoio/rede_form.html"
    
    def get_success_url(self):
        return reverse('rede_de_apoio:rede-list')
    
class RedeDeApoioUpdateView(
    LoginRequiredMixin,
    UUIDViewMixin,
    UpdateView
):
    model = UnidadeDeApoio
    form_class = UnidadeDeApoioForm
    uuid_url_kwarg = "unidade_de_apoio_uuid"
    template_name = "rede_de_apoio/rede_form.html"
    
    def get_success_url(self):
        return reverse('rede_de_apoio:rede-list')

    
class RedeDeApoioDeleteView(
    LoginRequiredMixin,
    UUIDViewMixin,
    DeleteView
):
    model = UnidadeDeApoio
    http_method_names = ['delete', 'post']
    uuid_url_kwarg = "unidade_de_apoio_uuid"
    template_name = ""