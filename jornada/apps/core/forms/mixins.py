from django import forms
from django.contrib import messages
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseRedirect
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