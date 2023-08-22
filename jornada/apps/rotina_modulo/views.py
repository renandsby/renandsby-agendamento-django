from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls.base import reverse
from django.views.generic import View, ListView
from unidades.models import Modulo
from django.contrib.auth.mixins import LoginRequiredMixin
from unidades.models import Unidade, EntradaAdolescente, VagaUnidade
from central.painel_vagas import adiciona_vagas, somatorio, somatorio_internacao

from unidades.views import (
    EditaQuartoView,
    ModuloListView,
    QuartoListView,
    EntradaAdolescenteLotadosListView
)

from core.views import FilteredViewMixin

from unidades.filters import ModuloAdolescenteListFilterSet


class ModuloEditaQuartoView(EditaQuartoView):
    template_name = 'rotina_modulo/edita_quarto.html'

    def get_success_url(self):
        return reverse('rotina_modulo:modulo-entradas',kwargs={"modulo_uuid": self.kwargs.get("modulo_uuid")})


class UnidadeRedirectView(
    LoginRequiredMixin, 
    View
):
    def get(self, request):
        if (hasattr(request.user, 'servidor') and
            request.user.servidor is not None and 
            request.user.servidor.unidade is not None
        ):
            return redirect('rotina_modulo:home-modulos', unidade_uuid=request.user.servidor.unidade.uuid)
        
        # fallback pra raiz
        return redirect('/')



class HomeUnidadeView(LoginRequiredMixin, View):
    template_name = 'rotina_modulo/unidade_vagas_list.html'
    
    def get(self, request):
        unidades_internacao = Unidade.objects.filter(tipo_unidade__descricao="Internação")
        quadro_internacao = Unidade.objects.filter(tipo_unidade__descricao="Internação")
        unidades_atendimento_inicial = Unidade.objects.filter(tipo_unidade__descricao="Atendimento Inicial")
        unidades_semiliberdade = Unidade.objects.filter(tipo_unidade__descricao="Semiliberdade") 
        unidades_meio_aberto = Unidade.objects.filter(tipo_unidade__descricao="Meio Aberto") 
        context = {
            'quadro_internacao' : quadro_internacao,
            'unidades_internacao': adiciona_vagas(unidades_internacao),
            'somatorio_internacao': somatorio_internacao(unidades_internacao),
            'unidades_semiliberdade': adiciona_vagas(unidades_semiliberdade),
            'total_semiliberdade': somatorio(unidades_semiliberdade),
            'total_meio_aberto': somatorio(unidades_meio_aberto),
            'unidades_meio_aberto': adiciona_vagas(unidades_meio_aberto),
            'unidades_atendimento_inicial': adiciona_vagas(unidades_atendimento_inicial),
        }

        return render(request, self.template_name, context)


class HomeModuloView(
    LoginRequiredMixin, 
    ModuloListView
):
    template_name = 'rotina_modulo/modulo_list.html'
    
    def dispatch(self, request, *args, **kwargs):
        # Se só tem um módulo, vai direto pra tela daquele módulo
        modulos = self.get_queryset()
        
        # Se a Unidade tem apenas 1 módulo, não faz sentido listar módulos, então faz redirect
        if modulos.count() == 1:
            #Tem quartos
            if modulos.first().quartos.exists():

                # Caso 1 Módulo com quartos exceto NAI (Semis por exemplo)
                return redirect('rotina_modulo:quartos-modulo', modulo_uuid=modulos.first().uuid)

            # Caso UAMA ou Unidade com um módulo sem quartos
            if modulos.first().unidade.tipo_unidade.descricao == "Meio Aberto":
                return redirect('uama:adolescente-list', modulo_uuid=modulos.first().uuid)
            
        return super().dispatch(request, *args, **kwargs)
    


class ModuloQuartoListView(
    LoginRequiredMixin, 
    QuartoListView
):
    template_name = 'rotina_modulo/quarto_list.html'



class ModuloAdolescenteListView(
    LoginRequiredMixin, 
    FilteredViewMixin,
    EntradaAdolescenteLotadosListView
):
    filterset_class = ModuloAdolescenteListFilterSet
    template_name: str = 'rotina_modulo/adolescente_list.html'
    
    def get_queryset(self):
        qs = super().get_queryset().filter(
            modulo__uuid=self.kwargs.get('modulo_uuid'),
            evadido=False
        )
        return qs.order_by('modulo', 'quarto', 'adolescente__nome')
    


