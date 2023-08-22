from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from django.views import View
from django.urls.base import reverse
from django.contrib import messages
from core.forms.mixins import InlineFormsetMixin
from core.views import FilteredViewMixin, UUIDViewMixin

from .models import Vinculacao, Transferencia, Desvinculacao
from .forms import (
    VinculacaoForm, 
    AnexoVinculacaoFormSet,
    TransferenciaForm,
    AnexoTransferenciaFormSet,
    DesvinculacaoForm,
    AnexoDesvinculacaoFormSet
)
from .filters import (
    VinculacaoFilterSet,
    TransferenciaFilterSet,
    DesvinculacaoFilterSet
)

## VINCULACAO

class VinculacaoListView(
    FilteredViewMixin, 
    ListView
):
    model = Vinculacao
    paginate_by = 20
    filterset_class = VinculacaoFilterSet
    template_name = ""

    def get_queryset(self):
        return super().get_queryset().order_by('-modificado_em')
    

class VinculacaoCreateView(
    InlineFormsetMixin,
    CreateView
):
    model = Vinculacao
    form_class = VinculacaoForm
    inlineformset_classes = { 'anexos': AnexoVinculacaoFormSet }
    template_name = ""

    
  
class VinculacaoUpdateView(
    InlineFormsetMixin,
    UUIDViewMixin,
    UpdateView
):
    model = Vinculacao
    form_class = VinculacaoForm
    inlineformset_classes = { 'anexos': AnexoVinculacaoFormSet }
    uuid_url_kwarg = 'vinculacao_uuid'
    template_name = ""
    
  
class VinculacaoDeleteView(
    UUIDViewMixin,
    DeleteView
):
    model = Vinculacao
    http_method_names = ['delete', 'post']
    uuid_url_kwarg = 'vinculacao_uuid'

    def form_valid(self, form):
        try:
            self.object.delete()
            messages.success(self.request, f'{self.object.__class__.__name__} deletado com sucesso.')
        except Exception as e:
            from core.exceptions import get_error_message
            messages.error(self.request, f'{self.object.__class__.__name__} não pôde ser deletado. {get_error_message(e)}')
            return redirect(self.request.META.get('HTTP_REFERER'))
        return redirect(self.get_success_url())
    

class VincularView(View):
    def get(self, request, *args, **kwargs):
        vinculacao = Vinculacao.objects.get(uuid = kwargs.get("vinculacao_uuid")) 
        try:
            vinculacao.vincular()
            messages.success(request, f'{vinculacao.adolescente.nome} Vinculado com sucesso!')
            
        except Exception as e:
            from core.exceptions import get_error_message
            messages.error(request, f'Vinculação não pôde ser realizada. {get_error_message(e)}')
            return redirect(request.META.get('HTTP_REFERER'))
    
        return redirect(self.get_success_url())


class VinculacaoDesfazerView(View):
     def get(self, request, **kwargs):
        vinculacao = Vinculacao.objects.get(uuid = kwargs.get("vinculacao_uuid"))
        try:
            vinculacao.desfazer()
        except Exception as e:
            from core.exceptions import get_error_message
            messages.error(request, f"Não foi possível desfazer a Vinculação. {get_error_message(e)}")
            return redirect(request.META.get('HTTP_REFERER'))
        
        return redirect(self.get_success_url())


class VinculacaoCancelarView(View):
     def get(self, request, **kwargs):
        vinculacao = Vinculacao.objects.get(uuid = kwargs.get("vinculacao_uuid"))
        try:
            vinculacao.cancelar()
        except Exception as e:
            from core.exceptions import get_error_message
            messages.error(request, f"Não foi possível cancelar a Vinculação. {get_error_message(e)}")
            return redirect(request.META.get('HTTP_REFERER'))
        
        return redirect(self.get_success_url())



### TRANSFERENCIA

class TransferenciaListView( 
    FilteredViewMixin, 
    ListView
):
    model = Transferencia
    paginate_by = 20
    filterset_class = TransferenciaFilterSet
    template_name = ""

    def get_queryset(self):
        return super().get_queryset().order_by('-modificado_em')
    

class TransferenciaCreateView(
    InlineFormsetMixin,
    CreateView
):
    model = Transferencia
    form_class = TransferenciaForm
    inlineformset_classes = { 'anexos' : AnexoTransferenciaFormSet }
    template_name = ""

  
class TransferenciaUpdateView(
    InlineFormsetMixin,
    UpdateView
):
    model = Transferencia
    form_class = TransferenciaForm
    inlineformset_classes = { 'anexos' : AnexoTransferenciaFormSet }
    # TODO alterar todos que usam UUIDViewMixin por essa solução mais elegante
    slug_url_kwarg = 'transferencia_uuid'
    slug_field = 'uuid'
    template_name = ""
    
  
class TransferenciaDeleteView(
    UUIDViewMixin,
    DeleteView
):
    model = Transferencia
    http_method_names = ['delete', 'post']
    uuid_url_kwarg = 'transferencia_uuid'
    
    def form_valid(self, form):
        try:
            self.object.delete()
            messages.success(self.request, f'{self.object.__class__.__name__} deletada sucesso.')
        except Exception as e:    
            from core.exceptions import get_error_message
            messages.error(self.request, f'{self.object.__class__.__name__} não pôde ser deletado. {get_error_message(e)}')
            return redirect(self.request.META.get('HTTP_REFERER'))
        return redirect(self.get_success_url())    
    
class TransferirView(View):
    def get(self, request, **kwargs):
        transferencia = Transferencia.objects.get(uuid=kwargs.get('transferencia_uuid'))
        try:
            transferencia.transferir()
            messages.success(request, f'{transferencia.adolescente.nome} transferido com sucesso!')
            
        except Exception as e:
            from core.exceptions import get_error_message
            messages.error(request, f'Transferência não pôde ser realizada. {get_error_message(e)}')
            return redirect(request.META.get('HTTP_REFERER'))
    
        return redirect(self.get_success_url())

class TransferenciaDesfazerView(View):
     def get(self, request, **kwargs):
        transferencia = Transferencia.objects.get(uuid=kwargs.get('transferencia_uuid'))
        try:
            transferencia.desfazer()
        except Exception as e:
            from core.exceptions import get_error_message
            messages.error(request, f"Não foi possível desfazer a Transferência. {get_error_message(e)}")
            return redirect(request.META.get('HTTP_REFERER'))
        
        return redirect(self.get_success_url())

class TransferenciaCancelarView(View):
     def get(self, request, **kwargs):
        transferencia = Transferencia.objects.get(uuid=kwargs.get('transferencia_uuid'))
        try:
            transferencia.cancelar()
        except Exception as e:
            from core.exceptions import get_error_message
            messages.error(request, f"Não foi possível cancelar a Transferência. {get_error_message(e)}")
            return redirect(request.META.get('HTTP_REFERER'))
        
        return redirect(self.get_success_url())




### DESVINCULAÇÃO

class DesvinculacaoListView(
    FilteredViewMixin, 
    ListView
):
    model = Desvinculacao
    paginate_by = 20
    filterset_class = DesvinculacaoFilterSet
    template_name = ""

    def get_queryset(self):
        return super().get_queryset().order_by('-modificado_em')
    

class DesvinculacaoCreateView(
    InlineFormsetMixin,
    CreateView
):
    model = Desvinculacao
    form_class = DesvinculacaoForm
    inlineformset_classes = { 'anexos': AnexoDesvinculacaoFormSet }
    template_name = ""


  
class DesvinculacaoUpdateView(
    InlineFormsetMixin,
    UUIDViewMixin,
    UpdateView
):
    model = Desvinculacao
    form_class = DesvinculacaoForm
    inlineformset_classes = { 'anexos': AnexoDesvinculacaoFormSet }
    uuid_url_kwarg = 'desvinculacao_uuid'
    template_name = ""
    


class DesvinculacaoDeleteView(
    UUIDViewMixin,
    DeleteView
):    
    model = Desvinculacao
    http_method_names = ['delete', 'post']
    uuid_url_kwarg = 'desvinculacao_uuid'

    def form_valid(self, form):
        try:
            self.object.delete()
            messages.success(self.request, f'{self.object.__class__.__name__} deletado com sucesso.')
        except Exception as e:    
            from core.exceptions import get_error_message
            messages.error(self.request, f'{self.object.__class__.__name__} não pôde ser deletado. {get_error_message}')
            return redirect(self.request.META.get('HTTP_REFERER'))
        
        return redirect(self.get_success_url())


class DesvincularView(View):
    def get(self, request, **kwargs):
        desvinculacao = Desvinculacao.objects.get(uuid=kwargs.get('desvinculacao_uuid'))
        try:
            desvinculacao.desvincular()
            messages.success(request, f'{desvinculacao.adolescente.nome} Desvinculado com sucesso!')
        except Exception as e:
            from core.exceptions import get_error_message
            messages.error(request, f'Desvinculação não pôde ser realizada. {get_error_message(e)}')
            return redirect(request.META.get('HTTP_REFERER'))
            
        return redirect(self.get_success_url())

class DesvinculacaoDesfazerView(View):
     def get(self, request, **kwargs):
        desvinculacao = Desvinculacao.objects.get(uuid=kwargs.get('desvinculacao_uuid'))
        try:
            desvinculacao.desfazer()
        except Exception as e:
            from core.exceptions import get_error_message
            messages.error(request, f"Não foi possível desfazer a Desvinculação. {get_error_message(e)}")
            return redirect(request.META.get('HTTP_REFERER'))
        
        return redirect(self.get_success_url())

class DesvinculacaoCancelarView(View):
     def get(self, request, **kwargs):
        desvinculacao = Desvinculacao.objects.get(uuid=kwargs.get('desvinculacao_uuid'))
        try:
            desvinculacao.cancelar()
        except Exception as e:
            from core.exceptions import get_error_message
            messages.error(request, f"Não foi possível cancelar a Desvinculação. {get_error_message(e)}")
            return redirect(request.META.get('HTTP_REFERER'))
        
        return redirect(self.get_success_url())

