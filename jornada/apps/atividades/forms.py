from time import time
from typing import Any, Dict
from django import forms
from django.utils import timezone
from adolescentes.models import Adolescente
from django.core.exceptions import NON_FIELD_ERRORS
from core.forms.widgets import CustomAttachmentInput
from core.validators import validate_file_size
from unidades.models import EntradaAdolescente, Unidade, Modulo
from .models import Atividade, AdolescenteAtividade, HistoricoAtividade, AnexoHistoricoAtividade
from servidores.models import Servidor
from core.exceptions import ValidationError
from core.forms.widgets import CustomSplitDateTimeWidget

class AtividadeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        unidade = kwargs.pop('unidade', None)
        super().__init__(*args, **kwargs)
        self.fields["unidade"].widget = forms.HiddenInput()
        
        if unidade is not None:        
            self.fields["unidade"].queryset = Unidade.objects.filter(id=unidade.id)
            self.initial["unidade"] = unidade
    class Meta:
        model = Atividade
        fields = '__all__'
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "Já existe atividade com essa Descrição",
            }
        }



class AdolescenteAtividadeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.unidade = kwargs.pop('unidade', None)
        super().__init__(*args, **kwargs)

        if self.unidade is not None:
            self.fields['atividade'].queryset = self.unidade.atividades.all()


    class Meta:
        model = AdolescenteAtividade
        fields = "__all__" 
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "O adolescente já está inscrito nesta atividade.",
            }
        }

AdolescenteAtividadeFormset = forms.inlineformset_factory(
    EntradaAdolescente, 
    AdolescenteAtividade,
    form=AdolescenteAtividadeForm,
    fk_name="entrada", 
    fields="__all__", 
    extra=1, 
    max_num=1,   
    can_delete=True
)


class HistoricoAtividadeForm(forms.ModelForm):  
    class Meta:
        model = HistoricoAtividade
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields["modulo"].widget = forms.HiddenInput()
        self.initial["modulo"] = self.instance.modulo
        self.fields["modulo"].queryset = Modulo.objects.filter(id=self.instance.modulo.id)
        self.fields["adolescente"].widget = forms.HiddenInput()
        self.initial["adolescente"] = self.instance.adolescente
        self.fields["adolescente"].queryset = Adolescente.objects.filter(id=self.instance.adolescente.id)
        self.fields["atividade"].widget = forms.HiddenInput()
        self.initial["atividade"] = self.instance.atividade
        self.fields["atividade"].queryset = Atividade.objects.filter(id=self.instance.atividade.id)        



class EnvioAdolescentesForm(forms.Form):
    adolescentes = forms.ModelMultipleChoiceField(queryset=Adolescente.objects.none(), widget=forms.MultipleHiddenInput(), to_field_name='uuid')
    atividade = forms.ModelChoiceField(queryset=Atividade.objects.none(), widget=forms.HiddenInput(),to_field_name='uuid')
    data_ida = forms.SplitDateTimeField(initial=timezone.now, label='Data/Hora Ida', widget=CustomSplitDateTimeWidget(time_format="%H:%M", date_format="%Y-%m-%d"))
    observacoes = forms.fields.CharField(label='Observações', widget=forms.widgets.Textarea(), required=False)
    anexo = forms.fields.FileField(max_length=500, required=False, validators=[validate_file_size])

    def __init__(self, *args, **kwargs):
        self.adolescentes = kwargs.pop('adolescentes', None)
        self.atividade = kwargs.pop('atividade', None)    
        self.modulo = kwargs.pop('modulo', None)
        
        super().__init__(*args, **kwargs)
        
        if self.modulo is not None:
            self.fields['adolescentes'].queryset = self.modulo.adolescentes
            self.fields['atividade'].queryset = self.modulo.unidade.atividades.all()

        if self.adolescentes is not None:
            self.fields['adolescentes'].initial = self.adolescentes
        
        if self.atividade is not None:  
            self.fields['atividade'].initial = self.atividade
        
    



class RetornoAdolescentesForm(forms.Form):
    historicos = forms.ModelMultipleChoiceField(queryset=HistoricoAtividade.objects.none(), widget=forms.MultipleHiddenInput(), to_field_name='uuid')
    atividade = forms.ModelChoiceField(queryset=Atividade.objects.none(), widget=forms.HiddenInput(), to_field_name='uuid')
    data_retorno = forms.SplitDateTimeField(initial=timezone.now, label='Data/Hora Retorno', widget=CustomSplitDateTimeWidget(time_format="%H:%M", date_format="%Y-%m-%d"))
    observacoes = forms.fields.CharField(label='Observações', widget=forms.widgets.Textarea(), required=False)
    anexo = forms.fields.FileField(max_length=500, required=False, validators=[validate_file_size])
    
    def __init__(self, *args, **kwargs):
        self.historicos = kwargs.pop('historicos', None)
        self.atividade = kwargs.pop('atividade', None)
        self.modulo = kwargs.pop('modulo', None)
        
        super().__init__(*args, **kwargs)
        
        if self.modulo is not None:
            self.fields['atividade'].queryset = self.modulo.unidade.atividades.all()
        
        if self.historicos is not None:
            self.fields['historicos'].initial = self.historicos
        
        if self.atividade is not None:  
            self.fields['atividade'].initial = self.atividade
            self.fields['historicos'].queryset = HistoricoAtividade.objects.filter(atividade=self.atividade)
        
            



class AgendamentoEnviarForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['data_ida'] = timezone.now

    class Meta:
        model = HistoricoAtividade
        fields = ('data_ida', 'observacoes') 

class AgendamentoRetornarForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['data_retorno'] = timezone.now
        
    class Meta:
        model = HistoricoAtividade
        fields = ('data_retorno', 'observacoes') 

class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = HistoricoAtividade
        fields = ('adolescente', 'atividade', 'data_prevista_ida', 'observacoes_agendamento', 'servidores_relacionados')

    def __init__(self, *args, **kwargs):
        self.modulo = kwargs.pop('modulo', None)
        super().__init__(*args, **kwargs)
        
        if self.modulo is not None:
            self.fields['adolescente'].queryset = self.modulo.adolescentes.all()
            self.fields['atividade'].queryset = self.modulo.unidade.atividades.all()
            self.fields['servidores_relacionados'].queryset = self.modulo.unidade.servidores.all()
            
        if self.instance.pk:
            self.fields['servidores_relacionados'].queryset = self.instance.atividade.unidade.servidores.all()
            self.fields['atividade'].queryset = self.instance.atividade.unidade.atividades.all()
            self.fields['adolescente'].queryset = self.instance.atividade.unidade.adolescentes_lotados.all()
        


        self.fields['atividade'].label_from_instance = lambda obj: obj.descricao


        
class AgendamentoAtividadeForm(forms.Form):
    adolescentes = forms.ModelMultipleChoiceField(queryset=Adolescente.objects.none())
    servidores = forms.ModelMultipleChoiceField(queryset=Servidor.objects.none(), required=False)
    atividade = forms.ModelChoiceField(queryset=Atividade.objects.none())
    data_prevista_ida = forms.DateTimeField(label='Data', widget=forms.widgets.DateTimeInput, required=False)
    observacoes_agendamento = forms.fields.CharField(label='Observações', widget=forms.widgets.Textarea(), required=False)
    
    def __init__(self, *args, **kwargs):
        self.modulo = kwargs.pop('modulo', None)    
        super().__init__(*args, **kwargs)
        
        if self.modulo is not None:
            self.fields['adolescentes'].queryset = self.modulo.adolescentes.all()
            self.fields['atividade'].queryset = self.modulo.unidade.atividades.all()
            self.fields['servidores'].queryset = self.modulo.unidade.servidores.all()

        self.fields['atividade'].label_from_instance = lambda obj: obj.descricao


AnexoAgendamentoAtividadeFormset = forms.inlineformset_factory( 
        HistoricoAtividade,
        AnexoHistoricoAtividade,
        fk_name="historico",
        fields="__all__",
        extra=1,
        widgets={
                'anexo' : CustomAttachmentInput()
            }
        )
