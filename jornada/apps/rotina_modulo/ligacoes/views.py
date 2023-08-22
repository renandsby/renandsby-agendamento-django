from django.urls.base import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from ligacoes.views import (
    LigacaoListView,
    LigacaoCreateView,
    LigacaoUpdateView,
    LigacaoDeleteView
)

class ModuloLigacaoListView(
    LoginRequiredMixin, 
    LigacaoListView
):
    template_name = 'rotina_modulo/ligacoes/ligacao_list.html'

class ModuloLigacaoCreateView( 
    LoginRequiredMixin,
    LigacaoCreateView
):
    template_name = 'rotina_modulo/ligacoes/ligacao_form.html'

    def get_success_url(self):
        return reverse('rotina_modulo:modulo-ligacao-list', kwargs={"modulo_uuid": self.kwargs.get('modulo_uuid')}) + '?periodo=today'


class ModuloLigacaoUpdateView(
    LoginRequiredMixin,
    LigacaoUpdateView
):
    template_name = 'rotina_modulo/ligacoes/ligacao_form.html'

    def get_success_url(self):
        return reverse('rotina_modulo:modulo-ligacao-list', kwargs={"modulo_uuid": self.kwargs.get('modulo_uuid')}) + '?periodo=today'
        

class ModuloLigacaoDeleteView(
    LoginRequiredMixin,
    LigacaoDeleteView
):
    
    def get_success_url(self):
        return reverse('rotina_modulo:modulo-ligacao-list', kwargs={"modulo_uuid": self.kwargs.get('modulo_uuid')}) + '?periodo=today'