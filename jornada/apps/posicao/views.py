from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls.base import reverse
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db import models
from core.views import FilteredViewMixin, UUIDViewMixin
from dominios.models import Bairro, Cidade
# from .filters import PosicaoFilterSet
from .models import RedeEmpresas, Endereco, Vagas
from .forms import RedeEmpresasForm, EnderecoForm
from django.utils import timezone, dateparse
from django.views.generic import View, ListView






class PosicaoRedirectView(
    LoginRequiredMixin, 
    View
):
    ...



class PosicaoListView(
    LoginRequiredMixin,
    ListView,
):
    model = RedeEmpresas
    form_class = RedeEmpresasForm
    # filterset_class = PosicaoFilterSet
    template_name = "posicao/rede_list.html"
        # return queryset.order_by('-sede', 'id')
    # def get_context_data(self, **kwargs):
    #     context =  Endereco.objects.all()
    #     if 'endereco' in self.request.GET:
    #         if self.request.GET['endereco']:
    #             context['endereco'] = Bairro.objects.get(id=self.request.GET['endereco'])
    #     return context
   
    def get_queryset(self):
        queryset = RedeEmpresas.objects.all()
        print(queryset)
        return queryset.order_by('id')

    def get_success_url(self):
        return reverse('posicao:rede-list')
    


class PosicaoCreateView(
    LoginRequiredMixin,
    CreateView
):
    model = RedeEmpresas
    form_class = RedeEmpresasForm
    template_name = "posicao/rede_form.html"

    def get_success_url(self):
        return reverse('posicao:rede-list')
    
class PosicaoUpdateView(
    LoginRequiredMixin,
    UUIDViewMixin,
    UpdateView
):
    model = RedeEmpresas
    form_class = RedeEmpresasForm
    uuid_url_kwarg = "rede_uuid"
    template_name = "posicao/rede_form.html"
    
    def get_success_url(self):
        return reverse('posicao:rede-list')

    
class PosicaoDeleteView(
    LoginRequiredMixin,
    UUIDViewMixin,
    DeleteView
):
    model = RedeEmpresas
    http_method_names = ['delete', 'post']
    uuid_url_kwarg = "rede_uuid"
    template_name = ""


class EnderecoListView(ListView):
    template_name = ""
    model = Endereco

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('id')

class EnderecoCreateView(
    CreateView
    ):
    model = Endereco
    form_class = EnderecoForm
    template_name = ""

class EnderecoUpdateView(
    UUIDViewMixin, 
    UpdateView
):
    model = Endereco
    form_class = EnderecoForm
    template_name = ""
    uuid_url_kwarg = "endereco_uuid"
    

    

