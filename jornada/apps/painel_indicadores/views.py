from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls.base import reverse
from django.views.generic import View, ListView
from unidades.models import Modulo
from django.contrib.auth.mixins import LoginRequiredMixin



class PainelIndicadoresRedirectView(
    LoginRequiredMixin, 
    View
):
    def get(self, request):
        # if (hasattr(request.user, 'servidor') and
        #     request.user.servidor is not None and 
        #     request.user.servidor.unidade is not None
        # ):
        #     return redirect('painel:home', unidade_uuid=request.user.servidor.unidade.uuid)
        
        # fallback pra raiz
        return redirect('painel:home', unidade_uuid=request.user.servidor.unidade.uuid)

class HomePainelIndicadorView(LoginRequiredMixin, View):
    template_name = 'painel_indicadores/unidade_vagas_list.html'
    
    def get(self, request):
       
        quadro_internacao = 10
        
        context = {
            'quadro_internacao' : quadro_internacao,

        }

        return render(request, self.template_name, context)


class HomeModuloView(
    LoginRequiredMixin, 
    View
    
):

    def get(self, request):
        return reverse('painel:home-painel')
    




