from django.db.models import signals
from functools import partial
import time
from django.conf import settings

from .models import RequestLog


def get_client_ip(request):
    ip_address = request.META.get('HTTP_X_FORWARDED_FOR', None)
    if ip_address:
        ip_address = ip_address.split(', ')[0]
    else:
        ip_address = request.META.get('REMOTE_ADDR', '')
    return ip_address




class RequestLogMiddleware:
    '''
    Middleware que intercepta a criação ou atualização de objetos
    e automaticamente os logs
    '''

    def __init__(self, get_response) -> None:
        self.get_response = get_response


    def __call__(self, request):
        MEDIA_URL = request.path.startswith(settings.MEDIA_URL)
        STATIC_URL = request.path.startswith(settings.STATIC_URL)

        if MEDIA_URL or STATIC_URL:   
            return self.get_response(request)
        
        if hasattr(request, 'user') and request.user.is_authenticated:
            user = request.user
            username = request.user.username
        else:
            user = None
            username = "Anônimo"
        
        log_object = RequestLog(
            user = user,
            username = username,
            ip = get_client_ip(request),
            method = request.method,
            path = request.get_full_path(),
        )
        
        
        if not request.method in ('GET', 'HEAD', 'OPTIONS', 'TRACE'):
            log_changes = partial(self.log_changes, log_object)
            signals.pre_save.connect(
                log_changes,
                dispatch_uid=(
                    self.__class__,
                    request,
                ),
                weak=False,
            )


        start_time = time.time()
    
        response = self.get_response(request)
        
        response_time = time.time() - start_time

        log_object.response_time = response_time
        log_object.save()
        

        signals.pre_save.disconnect(
            dispatch_uid=(
                self.__class__,
                request,
            )
        )
        return response

    def log_changes(self, log_object, sender, instance, **kwargs):
        if hasattr(instance, 'adding') and instance.adding:
            log_object.message = f"CRIOU: {instance._meta.db_table} => {instance.__dict__}"
            
        if hasattr(instance, 'updating') and instance.updating and hasattr(instance, 'changes') and instance.changes:
            log_object.message = f"EDITOU: {instance._meta.db_table}[{instance.pk}] => {instance.changes}" 