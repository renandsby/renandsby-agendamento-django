from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls.base import reverse
from .prontuario_base import AdolescenteFilterMixin, AdolescenteFormBindMixin
from core.forms.mixins import InlineFormsetMixin
from core.views import UUIDViewMixin
from pia.models import Pia
from pia.forms import ( 
    PiaForm,
    AnexoPia,
    AnexoPiaFormSet
)

class PiaListView(
    LoginRequiredMixin,
    AdolescenteFilterMixin,
    ListView
):
    model = Pia
    template_name = 'prontuario/pia/pia_list.html'


class PiaCreateView(
    AdolescenteFormBindMixin,
    LoginRequiredMixin,
    InlineFormsetMixin, 
    CreateView
):
    model = Pia
    form_class = PiaForm
    template_name = "prontuario/pia/pia_form.html"
    inlineformset_classes = {
        "anexos" : AnexoPiaFormSet
    }
    def get_success_url(self):
        return reverse('prontuario:pia-list', kwargs={"adolescente_uuid": self.kwargs.get("adolescente_uuid")})
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if hasattr(self.request.user, 'servidor') and self.request.user.servidor is not None and self.request.user.servidor.unidade is not None:
            kwargs["unidade"] = self.request.user.servidor.unidade
        return kwargs
                    
class PiaUpdateView(
    LoginRequiredMixin,
    InlineFormsetMixin,
    UUIDViewMixin,
    UpdateView
):
    model = Pia
    form_class = PiaForm
    template_name = "prontuario/pia/pia_form.html"
    uuid_url_kwarg = "pia_uuid"
    inlineformset_classes = {
        "anexos" : AnexoPiaFormSet
    }
    
    def get_success_url(self):
        return reverse('prontuario:pia-list', kwargs={"adolescente_uuid": self.kwargs.get("adolescente_uuid")})
