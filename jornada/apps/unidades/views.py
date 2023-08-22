from django.views.generic import (
    ListView, 
    CreateView, 
    UpdateView, 
    DeleteView,
)

from core.views import UUIDViewMixin, FilteredViewMixin
from core.forms.mixins import InlineFormsetMixin
from django.db.models import F, Func, Value, Q, When, Case
from django.db.models.functions import Cast
from django.db.models import IntegerField, CharField
from .models import Modulo, Quarto, Unidade, EntradaAdolescente


from .forms import (
    EntradaForm,
    UnidadeForm, 
    EditaQuartoForm, 
    EntradaCheckinForm,
    EntradaCheckoutForm,
    AnexoEntradaFormset,
    MedidaAdaptacaoFormset,
    MedidaDisciplinarFormset
)

from core.permission_mixins import CustomPermissionMixin


class UnidadeListView(CustomPermissionMixin, ListView):
    model = Unidade
    template_name = ""
    permission_required = ["unidades.acessar_todas"]
    no_permission_redirect_url = "/"

class UnidadeCreateView(CustomPermissionMixin, CreateView):
    model = Unidade
    form_class = UnidadeForm
    template_name = ""
    permission_required = ["unidades.incluir_unidades"]
    no_permission_redirect_url = "/"


class UnidadeUpdateView(
    UUIDViewMixin,
    CustomPermissionMixin,
    UpdateView
):
    model = Unidade
    form_class = UnidadeForm
    uuid_url_kwarg = "unidade_uuid"
    template_name = ""
    permission_required = ["unidades.editar_unidades"]
    no_permission_redirect_url = "/"


class ExtractInteger(Func):
    """ Returns the first int value from the string. Note that this
    requires the string to have an integer value inside.
    """
    function = 'REGEXP_MATCH'
    template = "CAST( (%(function)s(%(expressions)s, '\d+'))[1] as INTEGER )"
    output_field = IntegerField()


class ModuloListView(ListView):
    model = Modulo
    template_name = ""

    def get_queryset(self):
        return super().get_queryset().filter(
            unidade__uuid = self.kwargs.get("unidade_uuid")
        ).annotate(
            num_modulo=Case(
                    When(
                        descricao__regex='\d+',
                        then=ExtractInteger(F('descricao'))
                    ),
                    default=1
            ),
            
        ).order_by('num_modulo', 'descricao')


    
    
class QuartoListView(ListView):
    model = Quarto
    template_name = ""

    def get_queryset(self):     
        
        return super().get_queryset().filter(
            modulo__uuid = self.kwargs.get("modulo_uuid")
        )
                

class EntradaAdolescenteLotadosListView(
    ListView
):
    model = EntradaAdolescente
    paginate_by = 30
    template_name = ''

    def get_queryset(self):
        return super().get_queryset().filter(lotado=True)



class AcautelamentoListView(
    ListView
):
    model = EntradaAdolescente
    template_name: str = ""

    def get_queryset(self, **kwargs):
        return super().get_queryset().filter(status=1)

class AcautelamentoUpdateView(
    UUIDViewMixin,
    UpdateView
):
    model = EntradaAdolescente
    form_class = EntradaCheckinForm
    uuid_url_kwarg = "entrada_uuid"
    template_name = None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['unidade'] = self.object.unidade
        return kwargs


class SaidaListView(ListView):
    model = EntradaAdolescente
    template_name: str = ""

    def get_queryset(self, **kwargs):
        return super().get_queryset().filter(status=3)
    

class SaidaView(
    UUIDViewMixin,
    UpdateView
):
    model = EntradaAdolescente
    form_class = EntradaCheckoutForm
    uuid_url_kwarg = "entrada_uuid"
    template_name = ''



class EntradaUpdateView(
    InlineFormsetMixin, 
    UUIDViewMixin,
    UpdateView
):
    model = EntradaAdolescente
    form_class = EntradaForm
    uuid_url_kwarg = "entrada_uuid"
    template_name = ''
    inlineformset_classes = {
        "anexos": AnexoEntradaFormset,
        "medidas_adaptacao": MedidaAdaptacaoFormset,
        "medidas_disciplinares": MedidaDisciplinarFormset,

    }
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'unidade': self.object.unidade})
        return kwargs
    



class EditaQuartoView(
    UUIDViewMixin,
    UpdateView
):
    '''
    Essa view permite alterar o quarto de uma entrada.
    ATENÇÃO: ela pressupõe que a unidade não tem módulos, apenas quartos
    '''
    model = EntradaAdolescente
    form_class = EditaQuartoForm
    uuid_url_kwarg = "entrada_uuid"
    template_name = 'rotina_modulo/edita_quarto.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['unidade'] = self.object.unidade
        return kwargs


class IncluirAdolescenteEntradaView(CustomPermissionMixin, CreateView):
    model = EntradaAdolescente
    template_name = ""
    permission_required = ['unidades.incluir_entradas_na_unidade']
    no_permission_redirect_url = "/"

    def get_form_kwargs(self):
        kwargs =  super().get_form_kwargs()
        kwargs['modulo'] = Modulo.objects.get(uuid=self.kwargs.get('modulo_uuid'))
        return kwargs

