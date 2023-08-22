from django.urls.base import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from visitas.views import (
    VisitaListView,
    VisitaCreateView,
    VisitaUpdateView,
)

class ModuloVisitaListView(
    LoginRequiredMixin, 
    VisitaListView
):
    template_name = 'rotina_modulo/visitas/visita_list.html'

class ModuloVisitaCreateView( 
    LoginRequiredMixin,
    VisitaCreateView
):
    template_name = 'rotina_modulo/visitas/visita_form.html'

    def get_success_url(self):
        return reverse('rotina_modulo:modulo-visita-list', kwargs={"modulo_uuid": self.kwargs.get('modulo_uuid')})


class ModuloVisitaUpdateView(
    LoginRequiredMixin,
    VisitaUpdateView
):
    template_name = 'rotina_modulo/visitas/visita_form.html'

    def get_success_url(self):
        return reverse('rotina_modulo:modulo-visita-list', kwargs={"modulo_uuid": self.kwargs.get('modulo_uuid')})
        
