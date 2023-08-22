from typing import Any, Dict
from django import forms
from django.utils import timezone
from .models import Unidade, Modulo, EntradaAdolescente, Quarto, AnexoEntrada, MedidaAdaptacao, MedidaDisciplinar
from dominios.models import TipoSaidaUnidade
from core.forms.widgets import CustomAttachmentInput, CustomSplitDateTimeWidget
from core.forms.mixins import PreencheProcessoPorAdolescenteMixin, LabelProcessoSemNomeMixin
from adolescentes.models import Adolescente

class UnidadeForm(forms.ModelForm):
    class Meta:
        model = Unidade
        exclude = ("vagas",)


class ModuloLabelMixin:
    @staticmethod
    def modulo_label_from_instance(self):
        return str(self.descricao)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'modulo' in self.fields:
            self.fields['modulo'].label_from_instance = self.modulo_label_from_instance


class QuartoLabelMixin:
    @staticmethod
    def quarto_label_from_instance(self):
        label = str(self.numero)
        if self.nome is not None:
            label += str(self.nome)
        return label

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'quarto' in self.fields:
            self.fields['quarto'].label_from_instance = self.quarto_label_from_instance


class EntradaForm(
    ModuloLabelMixin,
    QuartoLabelMixin,
    forms.ModelForm
):
    def __init__(self, *args, **kwargs):
        if not hasattr(self, 'unidade') or (hasattr(self, 'unidade') and self.unidade is None):
            self.unidade = kwargs.pop('unidade', None)
        super().__init__(*args, **kwargs)
        
        #Infere Unidade se não foi passado no form kwargs
        if self.unidade is None:
            if hasattr(self.instance, 'unidade') and self.instance.unidade is not None:
                self.unidade = self.instance.unidade
        
        if self.unidade is not None:
            if "agente_referencia" in self.fields:
                self.fields["agente_referencia"].queryset = self.unidade.agentes 
            if "especialista_referencia" in self.fields:
                self.fields["especialista_referencia"].queryset = self.unidade.especialistas
            
            if self.unidade.modulos.count() > 1:
                self.fields['modulo'].queryset = self.unidade.modulos.all()
                self.fields['quarto'].queryset = Quarto.objects.none()
            else:
                self.fields['quarto'].queryset = self.unidade.modulos.first().quartos.all()

            if self.unidade.modulos.count() > 1 or self.unidade.modulos.first().quartos.exists():
                    self.fields['quarto'].required = True
        
        # pra no GET ja vir preenchido com o modulo e opções de quarto corretas
        if self.instance.modulo is not None:
            self.fields['quarto'].queryset = self.instance.modulo.quartos.all()
        
        # como no front a pessoa pode mudar o módulo, as opções de quartos podem mudar caso o módulo mude
        # self.data = dados que vieram do preenchimento do formulario via POST
        if 'modulo' in self.data:
            self.fields['quarto'].queryset = Quarto.objects.filter(modulo__id=self.data.get('modulo'))

    class Meta:
        model = EntradaAdolescente
        fields = ('modulo', 'quarto','protetiva', 'agente_referencia', 'especialista_referencia','tipo_entrada', 'tipo_vaga', 'data_entrada')


class EditaModuloQuartoForm(EntradaForm):
    class Meta:
        model = EntradaAdolescente
        fields = ('modulo','quarto')


class EditaQuartoForm(EntradaForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["modulo"].widget = forms.HiddenInput()
        
    class Meta:
        model = EntradaAdolescente
        fields = ('modulo','quarto')

class EntradaCheckinForm(EntradaForm):
    data_entrada = forms.SplitDateTimeField(required=True, initial=timezone.now, widget=CustomSplitDateTimeWidget(time_format="%H:%M", date_format="%Y-%m-%d"))
    
    class Meta:
        model = EntradaAdolescente
        fields = ('modulo', 'quarto','protetiva', 'data_entrada', 'agente_referencia', 'especialista_referencia','tipo_entrada', 'tipo_vaga')
    
    def clean(self) -> Dict[str, Any]:
        return_value =  super().clean()
        cleaned_data = self.cleaned_data
        if 'adolescente' in cleaned_data:
            adolescente = cleaned_data['adolescente']
            from unidades.logic import nao_tem_outra_entrada_lotado
            nao_tem_outra_entrada_lotado(adolescente)
        return return_value
    
    def save(self, commit=True):
        self.instance.realizar_entrada()
        return super().save(commit)



class EntradaCheckoutForm(forms.ModelForm):
    data_saida = forms.SplitDateTimeField(required=True, initial=timezone.now, widget=CustomSplitDateTimeWidget(time_format="%H:%M", date_format="%Y-%m-%d"))
    tipo_saida = forms.ModelChoiceField(
        queryset=TipoSaidaUnidade.objects.all(), 
        required=True
    )

    class Meta:
        model = EntradaAdolescente
        fields = ('tipo_saida','data_saida')
    
    def save(self, commit=True):
        self.instance.realizar_saida()
        return super().save(commit)

class EntradaCheckoutNAIForm(forms.ModelForm):
    data_prevista_saida = forms.DateField(required=False, initial=timezone.now)
    tipo_saida = forms.ModelChoiceField(
        queryset=TipoSaidaUnidade.objects.all(), 
        required=True
    )

    class Meta:
        model = EntradaAdolescente
        fields = ('tipo_saida','data_prevista_saida','observacoes_saida')
    
    def save(self, commit=True):
        self.instance.status = EntradaAdolescente.Status.SAIDA_PENDENTE
        self.instance.save()
        return super().save(commit)
    

class EditaEntradaAdmUnidadeForm(
    PreencheProcessoPorAdolescenteMixin,
    LabelProcessoSemNomeMixin,
    EntradaForm
):
    
    class Meta:
        model = EntradaAdolescente
        fields = ('modulo', 'quarto','protetiva', 'evadido', 'agente_referencia', 'especialista_referencia','tipo_entrada', 'tipo_vaga', 'data_entrada', 'processo')

def adolescente_label_from_instance(adol):
    label = str(adol.nome)
    if adol.possui_entrada_ativa:
        label += f" ({adol.entrada_em_unidade_atual.get_status_display()} em {str(adol.unidade_atual.sigla)})"
        if adol.entrada_em_unidade_atual.processo is not None:
            label += f" [{str(adol.entrada_em_unidade_atual.processo.str_sem_nome())}]"
    return label

class EntradaCheckinNAIForm(
    PreencheProcessoPorAdolescenteMixin,
    LabelProcessoSemNomeMixin,
    EntradaCheckinForm
):  
    data_entrada = forms.DateTimeField(required=True, initial=timezone.now)
    def __init__(self, *args, **kwargs):
        self.modulo = kwargs.pop('modulo', None)
        super().__init__(*args, **kwargs)
        
        # self.fields['adolescente'].label_from_instance = adolescente_label_from_instance    
        self.fields['adolescente'].queryset = Adolescente.nao_vinculados_em_unidade()
        
        self.fields["unidade"].widget = forms.HiddenInput()
        self.initial["unidade"] = self.modulo.unidade
        self.fields["unidade"].queryset = Unidade.objects.filter(id=self.modulo.unidade.id)
        
        self.fields["modulo"].widget = forms.HiddenInput()
        self.initial["modulo"] = self.modulo
        self.fields["modulo"].queryset = Modulo.objects.filter(id=self.modulo.id)
        
        self.fields['quarto'].required = True
        self.fields['quarto'].queryset = self.modulo.quartos.all()

    class Meta:
        model = EntradaAdolescente
        fields = ('adolescente', 'processo', 'unidade', 'modulo', 'quarto','protetiva', 'agente_referencia', 'especialista_referencia','tipo_entrada', 'tipo_vaga')



AnexoEntradaFormset = forms.inlineformset_factory(
    EntradaAdolescente,
    AnexoEntrada, 
    fk_name="entrada", 
    fields="__all__", 
    extra=1, 
    max_num=1,
    can_delete=True, 
    widgets = {
        'anexo': CustomAttachmentInput(),
    } 
)

MedidaAdaptacaoFormset = forms.inlineformset_factory(
    EntradaAdolescente,
    MedidaAdaptacao, 
    fk_name="entrada", 
    fields="__all__", 
    extra=1, 
    max_num=1,
    can_delete=True, 
)

MedidaDisciplinarFormset = forms.inlineformset_factory(
    EntradaAdolescente,
    MedidaDisciplinar, 
    fk_name="entrada", 
    fields="__all__", 
    extra=1, 
    max_num=1,
    can_delete=True, 
)