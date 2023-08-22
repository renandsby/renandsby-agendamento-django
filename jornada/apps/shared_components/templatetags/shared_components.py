from django_component import Library, Component
from django.template.exceptions import TemplateSyntaxError

register = Library()

@register.component
class Form(Component):
    template = "shared_components/form.html"
    
    def context(self, *args, **kwargs):
        form = kwargs.get('form', None)
        titulo = kwargs.get('titulo', None)
        
        if form is None:
            raise TemplateSyntaxError(
                f"Componente Form deve ser chamado com uma variável 'form' dentro do contexto \
                ou passar 'form' como parâmetro."
            )
        
        titulo_model = form._meta.model._meta.verbose_name.title()
        if titulo is None:
            if form.instance.pk is None:
                titulo = f"Cadastrar {titulo_model}"
            else:
                titulo = f"Editar {form.instance}"
        
        return {**kwargs, "titulo": titulo}
        
    class Media:
        css = { 'all' : ['shared_components/css/form.css'] }
        

@register.component
class LabeledInput(Component):
    template = "shared_components/labeled_input.html"    

@register.component
class UnlabeledInput(Component):
    template = "shared_components/unlabeled_input.html"  

@register.component
class BreadcrumbItem(Component):
    template = "shared_components/breadcrumb_item.html"


@register.component
class Breadcrumb(Component):
    template = "shared_components/breadcrumb.html"

@register.component
class Fieldset(Component):
    template = "shared_components/fieldset.html"


@register.component
class InlineFormset(Component):
    template = "shared_components/inline_formset.html"
    
    class Media:
        js = ['shared_components/js/inline_formset.js']


@register.component
class Filtros(Component):
    template = "shared_components/filtros.html"
    
    
@register.component
class Paginacao(Component):
    template = "shared_components/paginacao.html"


@register.component
class Modal(Component):
    template = "shared_components/modal.html"

@register.component
class CardAdolescente(Component):
    template = "shared_components/card_adolescente.html"
        
    class Media:
        css = { 'all' : ['shared_components/css/card_adolescente.css'] }
    

@register.component
class BotaoVoltar(Component):
    template = "shared_components/botao_voltar.html"

@register.component
class FormErrors(Component):
    template = "shared_components/form_errors.html"