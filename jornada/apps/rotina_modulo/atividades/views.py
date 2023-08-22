from django.urls.base import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from unidades.models import Modulo, EntradaAdolescente
from atividades.views import (
    AtividadeListView,
    AtividadeCreateView,
    AtividadeUpdateView,
    AtividadeHistoricoListView,
    AtividadeHistoricoUpdateView,
    AtividadeHistoricoDeleteView,
    AdolescenteHistoricoAtividadeListView,
    AtividadeEnviarAdolescentesView,
    AtividadeEnviarAdolescentesConfirmaView,
    AtividadeRetornarAdolescentesView,
    AtividadeRetornarAdolescentesConfirmaView,
)



class ModuloTimelineAdolescente(
    LoginRequiredMixin,
    AdolescenteHistoricoAtividadeListView
):
    template_name = 'rotina_modulo/atividades/timeline-adolescente.html'
    paginate_by: int = 40
    def get_queryset(self):
        entrada = EntradaAdolescente.objects.get(uuid=self.kwargs['entrada_uuid'])
        return super().get_queryset().filter(
            atividade__unidade = entrada.unidade, 
            adolescente = entrada.adolescente,
            agendado=False
            ).order_by('-data_ida')


class ModuloAtividadeListView(
    LoginRequiredMixin, 
    AtividadeListView
):
    template_name = 'rotina_modulo/atividades/atividade-list.html'

    

class ModuloAtividadeEnviarAdolescentesView(
    LoginRequiredMixin,
    AtividadeEnviarAdolescentesView
):
    template_name='rotina_modulo/atividades/atividade_enviar.html'
    


class ModuloAtividadeEnviarAdolescentesConfirmaView(
    LoginRequiredMixin,
    AtividadeEnviarAdolescentesConfirmaView
):
    template_name='rotina_modulo/atividades/atividade_enviar_confirmacao.html'
    
    def get_success_url(self):
        return reverse('rotina_modulo:modulo-atividades', kwargs={"modulo_uuid": self.modulo.uuid})
        


class ModuloAtividadeRetornarAdolescentesView(
    LoginRequiredMixin,
    AtividadeRetornarAdolescentesView
):
    template_name='rotina_modulo/atividades/atividade_retornar.html'



class ModuloAtividadeRetornarAdolescentesConfirmaView(
    LoginRequiredMixin,
    AtividadeRetornarAdolescentesConfirmaView
):
    template_name='rotina_modulo/atividades/atividade_retornar_confirmacao.html'
    
    def get_success_url(self):
        return reverse('rotina_modulo:modulo-atividades', kwargs={"modulo_uuid": self.modulo.uuid})
        


class ModuloAtividadeHistoricoListView(
    LoginRequiredMixin,
    AtividadeHistoricoListView
):
    template_name = 'rotina_modulo/atividades/historico_list.html'

    def get_queryset(self):
        modulo = Modulo.objects.get(uuid=self.kwargs.get('modulo_uuid'))
        return super().get_queryset().filter(adolescente__id__in=modulo.ids_adolescentes_lotados).exclude(agendado=True, em_atividade=False, realizada=False)



class ModuloAtividadeHistoricoUpdateView(
    LoginRequiredMixin,
    AtividadeHistoricoUpdateView
):
    template_name = 'rotina_modulo/atividades/historico_form.html'

    def get_success_url(self):
        return reverse(
                'rotina_modulo:modulo-atividade-historico', 
                kwargs={
                    "modulo_uuid": self.kwargs.get("modulo_uuid"),
                    "atividade_uuid": self.object.atividade.uuid
                }
            )

class ModuloAtividadeHistoricoDeleteView(
    LoginRequiredMixin,
    AtividadeHistoricoDeleteView
):
    def get_success_url(self):
        return reverse(
            'rotina_modulo:modulo-atividade-historico', 
            kwargs={
                "modulo_uuid": self.kwargs.get("modulo_uuid"),
                "atividade_uuid": self.object.atividade.uuid
            }
        )

class AdministradorAtividadeListView(
    LoginRequiredMixin, 
    AtividadeListView
):
    template_name = 'rotina_modulo/atividades/atividade-list.html'


class AdministradorAtividadeCreateView(
    LoginRequiredMixin, 
    AtividadeCreateView
):
    template_name = 'rotina_modulo/atividades/atividade-form.html'

    def get_success_url(self):
        return reverse('rotina_modulo:atividade-list', kwargs={"unidade_uuid": self.kwargs.get("unidade_uuid")})


class AdministradorAtividadeUpdateView(
    LoginRequiredMixin, 
    AtividadeUpdateView
):  
    template_name = 'rotina_modulo/atividades/atividade-form.html'

    def get_success_url(self):
        return reverse('rotina_modulo:atividade-list', kwargs={"unidade_uuid": self.kwargs.get("unidade_uuid")})

    

    