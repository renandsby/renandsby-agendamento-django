from django.views import View
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .decorators import unauthenticated_user
from django.contrib.auth.views import (LoginView as AuthLoginView, 
                                       PasswordChangeView as AuthPasswordChangeView,
                                       LogoutView as AuthLogoutView)

@method_decorator(unauthenticated_user, name='dispatch')
class LoginView(AuthLoginView):
    template_name = "custom_auth/login.html"
    success_url = '/'

    def form_valid(self, form):
        http_respose = super().form_valid(form)    
        if form.get_user().change_password:
           return redirect('alterar_senha')
        return http_respose 
    

    
@method_decorator(login_required(login_url='login'), name='dispatch')
class LogoutView(AuthLogoutView):
    success_url = '/'
    
@method_decorator(login_required(login_url='login'), name='dispatch')
class PasswordChangeView(AuthPasswordChangeView):
    template_name = "custom_auth/alterar_senha.html"
    success_url = '/'

@method_decorator(login_required(login_url='login'), name='dispatch')
class PasswordChangeView(AuthPasswordChangeView):
    template_name = "custom_auth/alterar_senha.html"
    success_url = '/'

    def form_valid(self, form):
        http_respose = super().form_valid(form)    

        form.user.change_password = False
        form.user.save()

        return http_respose

class RedirectView(LoginRequiredMixin, View):
    def _handle_user(self, request):
                      
        if request.user.has_perm('unidades.acessar_todas') or \
           request.user.has_perm('unidades.acessar_todas_internacoes') or \
           request.user.has_perm('unidades.acessar_todas_semiliberdades') or \
           request.user.has_perm('unidades.acessar_todas_geamas'):
            return redirect('rotina_modulo:home-unidades')
        
        if (hasattr(request.user, 'servidor') and
            request.user.servidor is not None and 
            request.user.servidor.unidade is not None
        ):
            return redirect('rotina_modulo:home-modulos', unidade_uuid=request.user.servidor.unidade.uuid)

        # Se não caiu em nenhum caso, Fallback é base.html (tela em branco)
        return render(request, "base.html")
    
    def get(self, request):
        return self._handle_user(request)
