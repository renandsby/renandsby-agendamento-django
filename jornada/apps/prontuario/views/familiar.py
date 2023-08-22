from django.urls.base import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from .prontuario_base import (
    AdolescenteFilterMixin, 
    AdolescenteFormBindMixin
)

from adolescentes.views import (
    FamiliarCreateView,
    FamiliarListView,
    FamiliarUpdateView
)



class FamiliarProntuarioListView(
    LoginRequiredMixin, 
    AdolescenteFilterMixin,
    FamiliarListView
):
    template_name = 'prontuario/familiar/familiar_list.html'
    
    
class FamiliarProntuarioCreateView(
    LoginRequiredMixin,
    AdolescenteFormBindMixin,
    FamiliarCreateView
):
    template_name = "prontuario/familiar/familiar_form.html"

    def get_success_url(self):
        return reverse('prontuario:familiar-list', kwargs={"adolescente_uuid": self.kwargs.get("adolescente_uuid")})


class FamiliarProntuarioUpdateView(
    LoginRequiredMixin, 
    FamiliarUpdateView
):
    template_name = "prontuario/familiar/familiar_form.html"
    
    def get_success_url(self):
        return reverse('prontuario:familiar-list', kwargs={"adolescente_uuid": self.kwargs.get("adolescente_uuid")})