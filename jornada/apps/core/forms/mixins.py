from django import forms
from django.contrib import messages
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseRedirect
from adolescentes.models import Adolescente
from processos.models import Processo
from unidades.models import EntradaAdolescente
from dominios.models import Cidade, Bairro


class UUIDParseFieldsMixin:
    ''' 
    TODO aprimorar essa mixin e aplicar em todos forms do sistema
    Garante que todos os campos de um form que sejam de escolha de entes de outro model
    irão sempre espor na tag <select> apenas o uuid
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field, forms.ModelChoiceField):
                model_class = field.choices.queryset.model
                if hasattr(model_class, 'uuid'):
                    field.to_field_name = 'uuid'


class LabelProcessoSemNomeMixin:
    @staticmethod
    def processo_label_from_instance(self):
        return self.str_sem_nome()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['processo'].label_from_instance = self.processo_label_from_instance


class PreencheProcessoPorAdolescenteMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['processo'].queryset = Processo.objects.none()
    
        if hasattr(self.instance, 'adolescente'):
            if self.instance.adolescente is not None:
                self.fields['processo'].queryset = self.instance.adolescente.processos.all()

        if 'adolescente' in self.data and self.data.get('adolescente') != "":
            self.fields['processo'].queryset = Processo.objects.filter(adolescente__id=self.data.get('adolescente'))

            
class UfCidadeBairroMixin:
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cidade'].queryset = Cidade.objects.none()
        self.fields['bairro'].queryset = Bairro.objects.none()

        # GET
        # Se objeto já tem uf selecionado
        if self.instance.uf is not None:
            self.fields['cidade'].queryset = self.instance.uf.cidades.all()
        
        # se objeto já tem cidade selecionada
        if self.instance.cidade is not None:
            self.fields['bairro'].queryset = self.instance.cidade.bairros.all()
        
        
        # POST
        # Se objeto já tem uf selecionado
        if 'uf' in self.data:
            self.fields['cidade'].queryset = Cidade.objects.filter(uf__sigla=self.data.get('uf'))
        
        if 'cidade' in self.data:
            self.fields['bairro'].queryset = Bairro.objects.filter(cidade__codigo=self.data.get('cidade'))
        
        if self.prefix is not None:
            if self.prefix+'-uf' in self.data:
                self.fields['cidade'].queryset = Cidade.objects.filter(uf__sigla=self.data.get('uf'))
            
            if self.prefix+'-cidade' in self.data:
                self.fields['bairro'].queryset = Bairro.objects.filter(cidade__codigo=self.data.get('cidade'))
            
            
            

class PreencheAdolescentesLotadosEmUnidadesMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        adol_lotados_ids = EntradaAdolescente.objects.filter(
                lotado=True
            ).all().values_list('adolescente__id', flat=True)
            
        adol_lotados_ids = list(adol_lotados_ids)
        if self.instance.pk and self.instance.adolescente is not None and self.instance.adolescente.id not in adol_lotados_ids:
            adol_lotados_ids.append(self.instance.adolescente.id)
        self.fields['adolescente'].queryset =  Adolescente.objects.filter(id__in=adol_lotados_ids)


class PreencheAdolescentesNaoLotadosEmUnidadesMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        adol_lotados_ids = EntradaAdolescente.objects.filter(
            lotado=True
        ).all().values_list('adolescente__id', flat=True)

        adol_lotados_ids = list(adol_lotados_ids)
        if self.instance.pk and self.instance.adolescente is not None and self.instance.adolescente.id in adol_lotados_ids:
            adol_lotados_ids.remove(self.instance.adolescente.id)

        self.fields['adolescente'].queryset =  Adolescente.objects.all().exclude(id__in=adol_lotados_ids)


class InlineFormsetMixin:
    inlineformset_classes = None
    
    def get_formset_kwargs(self):
        return None

    def get_inlineformset_classes(self):
        if self.inlineformset_classes is None:
            raise ImproperlyConfigured("InlineFormsetMixin is missing the inlineformset_classes attribute.")
        return self.inlineformset_classes
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        if self.request.POST:
            for context_name, inlineformset_class in self.get_inlineformset_classes().items():
                context[context_name] = inlineformset_class(self.request.POST, self.request.FILES, instance=self.object)
        else:
            class_args = {}
            for context_name, inlineformset_class in self.get_inlineformset_classes().items():
                if self.object is not None:
                    class_args = { 'instance' : self.object }
                
                if self.get_formset_kwargs() is not None:
                    if context_name in self.get_formset_kwargs():
                        class_args.update(self.get_formset_kwargs()[context_name])
                
                context[context_name] = inlineformset_class(**class_args)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formsets = {}
        for context_name in self.get_inlineformset_classes().keys():
            formsets[context_name] = context[context_name]
        
        if all([formset.is_valid() for formset in formsets.values()]):
            
            try:
                self.object = form.save()
                for formset in formsets.values():
                    formset.instance = self.object
                    formset.save()
                return HttpResponseRedirect(self.get_success_url())
            except Exception as e:
                from core.exceptions import get_error_message
                messages.error(self.request, f' Erro de formulário: {get_error_message(e)}')
                return self.render_to_response(self.get_context_data(form=form))        
        else:
            return self.render_to_response(self.get_context_data(form=form))