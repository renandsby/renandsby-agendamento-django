from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls.base import reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.views import FilteredViewMixin, UUIDViewMixin
from dominios.models import Bairro
from .models import RedeDeLocalizacao
from .filters import PosicaoFilterSet
from .forms import RedeDeLocalizacaoForm


class PosicaoListView(
    LoginRequiredMixin,
    FilteredViewMixin,
    ListView,
):
    model = RedeDeLocalizacao
    filterset_class = PosicaoFilterSet
    template_name = "posicao/rede_list.html"

    def get_success_url(self):
        return reverse('posicao:rede-list')
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        if 'bairro' in self.request.GET:
            if self.request.GET['bairro']:
                context['bairro'] = Bairro.objects.get(id=self.request.GET['bairro'])
        return context


class PosicaoCreateView(
    LoginRequiredMixin,
    CreateView
):
    model = RedeDeLocalizacao
    form_class = RedeDeLocalizacaoForm
    template_name = "posicao/rede_form.html"
    
    def get_success_url(self):
        return reverse('posicao:rede-list')
    
class PosicaoUpdateView(
    LoginRequiredMixin,
    UUIDViewMixin,
    UpdateView
):
    model = RedeDeLocalizacao
    form_class = RedeDeLocalizacaoForm
    uuid_url_kwarg = "rede_de_localizacao_uuid"
    template_name = "posicao/rede_form.html"
    
    def get_success_url(self):
        return reverse('posicao:rede-list')

    
class PosicaoDeleteView(
    LoginRequiredMixin,
    UUIDViewMixin,
    DeleteView
):
    model = RedeDeLocalizacao
    http_method_names = ['delete', 'post']
    uuid_url_kwarg = "rede_de_localizacao_uuid"
    template_name = ""