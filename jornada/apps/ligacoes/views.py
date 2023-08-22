from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.shortcuts import redirect
from core.views import FilteredViewMixin, UUIDViewMixin
from unidades.models import Modulo
from .forms import LigacaoForm
from .models import Ligacao
from .filters import LigacaoFilterset


class LigacaoListView(
    FilteredViewMixin,
    ListView
):
    paginate_by = 10
    model = Ligacao
    context_object_name = 'ligacoes'
    filterset_class = LigacaoFilterset
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        if 'modulo_uuid' in self.kwargs:
            qs = qs.filter(modulo__uuid=self.kwargs.get('modulo_uuid'))
        return qs


class LigacaoCreateView(                     
    CreateView
):
    model = Ligacao
    form_class = LigacaoForm
    
    def get_form_kwargs(self, **kwargs):
        kwargs = super().get_form_kwargs()
        if 'modulo_uuid' in self.kwargs:
            kwargs['modulo'] = Modulo.objects.get(uuid=self.kwargs.get('modulo_uuid'))
        return kwargs


class LigacaoUpdateView(
    UUIDViewMixin,
    UpdateView 
):
    model = Ligacao
    form_class = LigacaoForm
    uuid_url_kwarg = "ligacao_uuid"

    def get_form_kwargs(self, **kwargs):
        kwargs = super().get_form_kwargs()
        if 'modulo_uuid' in self.kwargs:
            kwargs['modulo'] = Modulo.objects.get(uuid=self.kwargs.get('modulo_uuid'))
        return kwargs


class LigacaoDeleteView(
    UUIDViewMixin,
    DeleteView
):    
    model = Ligacao
    http_method_names = ['delete', 'post']
    uuid_url_kwarg = "ligacao_uuid"

    def form_valid(self, form):
        try:
            self.object.delete()
            messages.success(self.request, f'{self.object.__class__.__name__} deletado com sucesso.')
        except Exception as e:    
            from core.exceptions import get_error_message
            messages.error(self.request, f'{self.object.__class__.__name__} não pôde ser deletado. {get_error_message}')
            return redirect(self.request.META.get('HTTP_REFERER'))
        
        return redirect(self.get_success_url())
    