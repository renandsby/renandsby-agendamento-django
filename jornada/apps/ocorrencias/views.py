from django.views.generic import ListView, CreateView, UpdateView

from core.forms.mixins import InlineFormsetMixin
from core.views import FilteredViewMixin, UUIDViewMixin
from unidades.models import Modulo, Unidade

from .models import Ocorrencia
from .forms import OcorrenciaForm, AnexoOcorrenciaFormSet
from .filters  import OcorrenciaFilterSet

class OcorrenciaListView(FilteredViewMixin,ListView):
    paginate_by = 10
    filterset_class = OcorrenciaFilterSet
    model = Ocorrencia
    context_object_name = 'ocorrencias'

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        if 'unidade_uuid' in self.kwargs:
            qs = qs.filter(unidade__uuid=self.kwargs.get('unidade_uuid'))
        if 'modulo_uuid' in self.kwargs:
            qs = qs.filter(modulo__uuid=self.kwargs.get('modulo_uuid'))
        return qs


class OcorrenciaCreateView(
    InlineFormsetMixin, 
    CreateView
):
    model = Ocorrencia
    form_class = OcorrenciaForm
    inlineformset_classes = {
        "anexos" : AnexoOcorrenciaFormSet
    }


    def get_form_kwargs(self, **kwargs):
        kwargs = super().get_form_kwargs()
        if 'modulo_uuid' in self.kwargs:
            kwargs['modulo'] = Modulo.objects.get(uuid=self.kwargs.get('modulo_uuid'))
        return kwargs


class OcorrenciaUpdateView(
    InlineFormsetMixin,
    UUIDViewMixin,
    UpdateView 
):
    model = Ocorrencia
    form_class = OcorrenciaForm
    uuid_url_kwarg = "ocorrencia_uuid"
    inlineformset_classes = {
        "anexos": AnexoOcorrenciaFormSet
    }

    def get_form_kwargs(self, **kwargs):
        kwargs = super().get_form_kwargs()
        if 'modulo_uuid' in self.kwargs:
            kwargs['modulo'] = Modulo.objects.get(uuid=self.kwargs.get('modulo_uuid'))
        return kwargs

