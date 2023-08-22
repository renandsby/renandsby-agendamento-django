from functools import wraps
from django.shortcuts import redirect
from django.utils.decorators import method_decorator

def cbv_decorator(decorator):
    return method_decorator(decorator, name="dispatch")

def disable_for_loaddata(signal_handler):
    """
        Decorator que desliga o signal caso os dados estejam sendo adicionados em um loaddata
    """

    @wraps(signal_handler)
    def wrapper(*args, **kwargs):
        if kwargs.get('raw'):
            return
        signal_handler(*args, **kwargs)
    return wrapper


def grupos_permitidos(*groups):
    def decorator(function):
        @wraps(function)
        def wrapper(request, *args, **kwargs):
            if request.user.groups.filter(name__in=groups).exists():
                return function(request, *args, **kwargs)
            #TODO tela de acesso negado
            return redirect('/')
        return wrapper
    return decorator