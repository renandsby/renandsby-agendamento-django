from django.shortcuts import redirect
from django.urls.base import reverse
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from core.forms.mixins import InlineFormsetMixin
from core.views import FilteredViewMixin, UUIDViewMixin

from .models import Solicitacao
from .forms import SolicitacaoCentralForm, SolicitacaoUnidadeForm, AnexoSolicitacaoFormSet
from .filters import SolicitacaoFilterSet


class SolicitacaoListView( 
    FilteredViewMixin, 
    ListView
):
    model = Solicitacao
    paginate_by = 20
    filterset_class = SolicitacaoFilterSet
    template_name = ""

        
    
class SolicitacaoCreateView(
    InlineFormsetMixin,
    CreateView
):
    model = Solicitacao
    form_class = SolicitacaoUnidadeForm
    template_name = ""
    inlineformset_classes = { 
        'anexos' : AnexoSolicitacaoFormSet 
    }

    
class SolicitacaoUpdateView(
    InlineFormsetMixin,
    UUIDViewMixin,
    UpdateView
):
    uuid_url_kwarg = 'solicitacao_uuid'
    model = Solicitacao
    form_class = SolicitacaoUnidadeForm
    template_name = ""
    uuid_url_kwarg = 'solicitacao_uuid'
    inlineformset_classes = { 
        'anexos' : AnexoSolicitacaoFormSet 
    }

class SolicitacaoDeleteView(
    UUIDViewMixin,
    DeleteView
):    
    model = Solicitacao
    http_method_names = ['delete', 'post']
    uuid_url_kwarg = 'solicitacao_uuid'

    def form_valid(self, form):
        success_url = self.get_success_url()
        try:
            self.object.delete()
            messages.success(self.request, f'{self.object.__class__.__name__} deletado com sucesso.')
        except Exception as e:
            from core.exceptions import get_error_message
            messages.error(self.request, f'{self.object.__class__.__name__} não pôde ser deletado. {get_error_message(e)}')
        return redirect(success_url)