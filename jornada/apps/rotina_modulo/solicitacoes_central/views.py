from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls.base import reverse
from unidades.models import Unidade


from solicitacoes.views import (
    SolicitacaoCreateView,
    SolicitacaoListView,
    SolicitacaoUpdateView
)


class AdministradorSolicitacaoListView(
    LoginRequiredMixin, 
    SolicitacaoListView
):
    template_name = "rotina_modulo/solicitacoes/solicitacao_list.html"

    def get_queryset(self):
        queryset =  super().get_queryset()
        return queryset.filter(unidade__uuid=self.kwargs.get("unidade_uuid"))
        
    

class AdministradorSolicitacaoCreateView(
    LoginRequiredMixin,
    SolicitacaoCreateView
):
    template_name = "rotina_modulo/solicitacoes/solicitacao_form.html"
    
    def form_valid(self, form):
        form.instance.unidade = Unidade.objects.get(uuid=self.kwargs.get('unidade_uuid'))
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        unidade = Unidade.objects.get(uuid=self.kwargs.get('unidade_uuid'))
        kwargs.update({"adolescentes": unidade.adolescentes_lotados})
        return kwargs
    
    def get_success_url(self):
        return reverse('rotina_modulo:solicitacao-list', kwargs={'unidade_uuid': self.kwargs.get('unidade_uuid')})
    
     
class AdministradorSolicitacaoUpdateView(
    LoginRequiredMixin,
    SolicitacaoUpdateView
):
    template_name = "rotina_modulo/solicitacoes/solicitacao_form.html"

    def get_success_url(self):
        return reverse('rotina_modulo:solicitacao-list', kwargs={'unidade_uuid': self.kwargs.get('unidade_uuid')})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        unidade = Unidade.objects.get(uuid=self.kwargs.get('unidade_uuid'))
        kwargs.update({"adolescentes": unidade.adolescentes_lotados})
        return kwargs

    def form_valid(self, form):
        form.instance.unidade = Unidade.objects.get(uuid=self.kwargs.get('unidade_uuid'))
        return super().form_valid(form)

    



