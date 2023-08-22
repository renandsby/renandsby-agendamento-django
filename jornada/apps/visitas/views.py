from django.views.generic import ListView, CreateView, UpdateView
from core.forms.mixins import InlineFormsetMixin
from core.views import FilteredViewMixin, UUIDViewMixin
from unidades.models import Modulo
from .forms import VisitaForm
from .models import Visita
from .filters import VisitaFilterset


class VisitaListView(
    FilteredViewMixin,
    ListView
):
    paginate_by = 10
    model = Visita
    context_object_name = 'visitas'
    filterset_class = VisitaFilterset

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        if 'modulo_uuid' in self.kwargs:
            qs = qs.filter(modulo__uuid=self.kwargs.get('modulo_uuid'))
        return qs


class VisitaCreateView( 
    InlineFormsetMixin,                       
    CreateView
):
    model = Visita
    form_class = VisitaForm
    inlineformset_classes = {"pertences"}
    
    def get_form_kwargs(self, **kwargs):
        kwargs = super().get_form_kwargs()
        if 'modulo_uuid' in self.kwargs:
            kwargs['modulo'] = Modulo.objects.get(uuid=self.kwargs.get('modulo_uuid'))
        return kwargs


class VisitaUpdateView(
    InlineFormsetMixin,
    UUIDViewMixin,
    UpdateView 
):
    model = Visita
    form_class = VisitaForm
    uuid_url_kwarg = "visita_uuid"

    def get_form_kwargs(self, **kwargs):
        kwargs = super().get_form_kwargs()
        if 'modulo_uuid' in self.kwargs:
            kwargs['modulo'] = Modulo.objects.get(uuid=self.kwargs.get('modulo_uuid'))
        return kwargs

