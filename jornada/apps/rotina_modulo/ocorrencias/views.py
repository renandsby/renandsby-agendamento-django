from django.urls.base import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from ocorrencias.views import (
    OcorrenciaListView,
    OcorrenciaCreateView,
    OcorrenciaUpdateView,
)

class ModuloOcorrenciaListView(
    LoginRequiredMixin, 
    OcorrenciaListView
):
    template_name = 'rotina_modulo/ocorrencias/ocorrencia_list.html'

class ModuloOcorrenciaCreateView( 
    LoginRequiredMixin,
    OcorrenciaCreateView
):
    template_name = 'rotina_modulo/ocorrencias/ocorrencia_form.html'

    def get_success_url(self):
        return reverse('rotina_modulo:modulo-ocorrencia-list', kwargs={"modulo_uuid": self.kwargs.get('modulo_uuid')})


class ModuloOcorrenciaUpdateView(
    LoginRequiredMixin,
    OcorrenciaUpdateView
):
    template_name = 'rotina_modulo/ocorrencias/ocorrencia_form.html'

    def get_success_url(self):
        return reverse('rotina_modulo:modulo-ocorrencia-list', kwargs={"modulo_uuid": self.kwargs.get('modulo_uuid')})
        
