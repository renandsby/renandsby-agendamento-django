from django.urls.base import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from unidades.models import Modulo, Unidade

from atividades.views import (
    AtividadeHistoricoDeleteView,
    AgendamentoCriaMultiplosView,
    AgendamentoListView,
    AgendamentoEnviarUpdateView,
    AgendamentoRetornarUpdateView,
    AgendamentoUpdateView
)



class ModuloAgendamentoCriaMultiplosView(
    LoginRequiredMixin,
    AgendamentoCriaMultiplosView
):
    template_name='rotina_modulo/agendamentos/agendamento_multiplos_form.html'
    
    def get_success_url(self):
        return reverse('rotina_modulo:modulo-listar-agendamentos', kwargs={"modulo_uuid": self.modulo.uuid})
        
  



class ModuloAgendamentoListView(
    LoginRequiredMixin,
    AgendamentoListView
):
    template_name = 'rotina_modulo/agendamentos/agendamento_list.html'

    def get_queryset(self):
        modulo = Modulo.objects.get(uuid=self.kwargs.get('modulo_uuid'))
        return super().get_queryset().filter(
            adolescente__id__in = modulo.ids_adolescentes_lotados
        )



class ModuloAgendamentoUpdateView(
    LoginRequiredMixin,
    AgendamentoUpdateView
):
    template_name = 'rotina_modulo/agendamentos/agendamento_form.html'

    def get_success_url(self):
        return reverse('rotina_modulo:modulo-listar-agendamentos', kwargs={"modulo_uuid": self.kwargs.get('modulo_uuid')})
        
  

class ModuloAgendamentoDeleteView(
    LoginRequiredMixin,
    AtividadeHistoricoDeleteView
):

    def get_success_url(self):
        return reverse('rotina_modulo:modulo-listar-agendamentos', kwargs={"modulo_uuid": self.kwargs.get('modulo_uuid')})
              



class ModuloAgendamentoEnviarUpdateView(
    LoginRequiredMixin,
    AgendamentoEnviarUpdateView
):
    template_name = 'rotina_modulo/agendamentos/agendamento_enviar_form.html'

    def get_success_url(self):
        return reverse('rotina_modulo:modulo-listar-agendamentos', kwargs={"modulo_uuid": self.kwargs.get('modulo_uuid')})
        
  


class ModuloAgendamentoRetornarUpdateView(
    LoginRequiredMixin,
    AgendamentoRetornarUpdateView
):
    template_name = 'rotina_modulo/agendamentos/agendamento_retornar_form.html'

    def get_success_url(self):
        return reverse('rotina_modulo:modulo-listar-agendamentos', kwargs={"modulo_uuid": self.kwargs.get('modulo_uuid')})
        
  
