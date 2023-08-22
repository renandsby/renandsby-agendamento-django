from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls.base import reverse
from core.decorators import grupos_permitidos, cbv_decorator

from solicitacoes.views import (
    SolicitacaoCreateView,
    SolicitacaoListView,
    SolicitacaoUpdateView,
    SolicitacaoDeleteView
)

class SolicitacaoTJDFTListView(
    LoginRequiredMixin, 
    SolicitacaoListView
):
    template_name = "tjdft/solicitacao/solicitacao_list.html"
    
    def get_queryset(self):
        return super().get_queryset().filter(criado_por__groups__name="TJDFT")
        

class SolicitacaoTJDFTCreateView(
    LoginRequiredMixin,
    SolicitacaoCreateView
):
    template_name = "tjdft/solicitacao/solicitacao_form.html"
    
    def get_success_url(self):
        return reverse('tjdft:solicitacao-list')
    

class SolicitacaoTJDFTUpdateView(
    LoginRequiredMixin,
    SolicitacaoUpdateView
):
    template_name = "tjdft/solicitacao/solicitacao_form.html"
    
    def get_success_url(self):
        return reverse('tjdft:solicitacao-list')
    

class SolicitacaoTJDFTDeleteView(
    LoginRequiredMixin,
    SolicitacaoDeleteView
):    
    def get_success_url(self):
        return reverse('tjdft:solicitacao-list')
    



