
from core.views import FilteredViewMixin, UUIDViewMixin
from core.forms.mixins import InlineFormsetMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.shortcuts import redirect
from .models import Processo
from .filters import ProcessoFilterSet
from .forms import ProcessoForm, AnexoProcessoFormSet


class ProcessoListView(
    FilteredViewMixin, 
    ListView
):
    model = Processo
    paginate_by = 15
    filterset_class = ProcessoFilterSet
    template_name = ""


class ProcessoCreateView(
    InlineFormsetMixin,
    CreateView
):
    model = Processo
    form_class = ProcessoForm
    inlineformset_classes = {
        "anexos": AnexoProcessoFormSet
    }
    template_name = ""


class ProcessoUpdateView(
    InlineFormsetMixin,
    UUIDViewMixin,
    UpdateView
):
    model = Processo
    form_class = ProcessoForm
    uuid_url_kwarg = "processo_uuid"
    inlineformset_classes = {
        "anexos" : AnexoProcessoFormSet
    }
    template_name = ""


class ProcessoDeleteView(
    UUIDViewMixin,
    DeleteView
):
    model = Processo
    http_method_names = ['delete', 'post']
    uuid_url_kwarg = 'processo_uuid'

    def form_valid(self, form):
        try:
            self.object.delete()
            messages.success(self.request, f'{self.object.__class__.__name__} deletado com sucesso.')
        except Exception as e:
            from core.exceptions import get_error_message
            messages.error(self.request, f'{self.object.__class__.__name__} não pôde ser deletado. {get_error_message(e)}')
            return redirect(self.request.META.get('HTTP_REFERER'))
        return redirect(self.get_success_url())
