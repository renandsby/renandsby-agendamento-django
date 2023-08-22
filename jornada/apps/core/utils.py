from rest_framework.request import Request
from django.http import QueryDict

import calendar
import datetime
from django.utils.html import avoid_wrapping
from django.utils.timezone import is_aware
from django.utils.translation import gettext, ngettext_lazy

# Tipos de vaga que, se o adolescente está na unidade ocupando essa vaga, ele não é considerado vinculado a ela
TIPOS_VAGA_NAO_VINCULANTES = ["Atendimento Inicial", "Internação Provisória"]


def date_to_plantao(date):
    return 1


def clona_request(request, new_data):
    """
    copiado do clone_request do rest_framework, mas altera os dados, não o metodo
    """
    ret = Request(
        request=request._request,
        parsers=request.parsers,
        authenticators=request.authenticators,
        negotiator=request.negotiator,
        parser_context=request.parser_context
    )
    
    ret._data = request._data
    ret._files = request._files
    ret._full_data = new_data
    ret._content_type = request._content_type
    ret._stream = request._stream
    ret.method = request.method
    
    if hasattr(request, '_user'):
        ret._user = request._user
    
    if hasattr(request, '_auth'):
        ret._auth = request._auth
    
    if hasattr(request, '_authenticator'):
        ret._authenticator = request._authenticator
    
    if hasattr(request, 'accepted_renderer'):
        ret.accepted_renderer = request.accepted_renderer
    
    if hasattr(request, 'accepted_media_type'):
        ret.accepted_media_type = request.accepted_media_type
    
    if hasattr(request, 'version'):
        ret.version = request.version
    
    if hasattr(request, 'versioning_scheme'):
        ret.versioning_scheme = request.versioning_scheme
    
    return ret


def update_multiple_data(data, **kwargs):
    '''
    atualiza dados de um request.data, como é imutavel cria-se um novo QueryDict
    '''
    new_data = []
    for d in data:
        if d is not None:
            q = QueryDict('', mutable=True)
            q.update(d)
            q.update(kwargs) 
            new_data.append(q.copy())
    return new_data


def save_with_parent_serializer(data, serializer, related_name, action='', *args, **kwargs):
    raise_exception = kwargs.pop('raise_exeption', True)
    if related_name in serializer.fields.keys():         
        __serializer_class = serializer.fields[related_name]
        if hasattr(__serializer_class, 'child'):
            __serializer_class = __serializer_class.child.__class__
        else:
            __serializer_class = __serializer_class.__class__

        data = [data] if type(data) is not list else data

        for d in data:       
            related_serializer = __serializer_class(data=d, many=False)
            try:
                related_serializer.is_valid(raise_exception=raise_exception)
            except Exception as e:
                if action == 'create':
                    serializer.instance.delete()
                raise e

            related_serializer.save()


def formata_idade_de_nascimento(d, now=None, reversed=False, time_strings=None, depth=3):

    TIME_STRINGS = {
        "year": ngettext_lazy("%(num)da", "%(num)da", "num"),
        "month": ngettext_lazy("%(num)dm", "%(num)dm", "num"),
        "day": ngettext_lazy("%(num)dd", "%(num)dd", "num"),
    }

    TIMESINCE_CHUNKS = (
        (60 * 60 * 24 * 365, "year"),
        (60 * 60 * 24 * 30, "month"),
        (60 * 60 * 24, "day"),
    )
    if time_strings is None:
        time_strings = TIME_STRINGS
    if depth <= 0:
        raise ValueError("depth must be greater than 0.")
    # Convert datetime.date to datetime.datetime for comparison.
    if not isinstance(d, datetime.datetime):
        d = datetime.datetime(d.year, d.month, d.day)
    if now and not isinstance(now, datetime.datetime):
        now = datetime.datetime(now.year, now.month, now.day)

    now = now or datetime.datetime.now(datetime.timezone.utc if is_aware(d) else None)

    if reversed:
        d, now = now, d
    delta = now - d

    # Deal with leapyears by subtracing the number of leapdays
    leapdays = calendar.leapdays(d.year, now.year)
    if leapdays != 0:
        if calendar.isleap(d.year):
            leapdays -= 1
        elif calendar.isleap(now.year):
            leapdays += 1
    delta -= datetime.timedelta(leapdays)

    # ignore microseconds
    since = delta.days * 24 * 60 * 60 + delta.seconds
   
    for i, (seconds, name) in enumerate(TIMESINCE_CHUNKS):
        count = since // seconds
        if count != 0:
            break
   
    result = []
    current_depth = 0
    while i < len(TIMESINCE_CHUNKS) and current_depth < depth:
        seconds, name = TIMESINCE_CHUNKS[i]
        count = since // seconds
        if count == 0:
            break
        result.append(avoid_wrapping(time_strings[name] % {"num": count}))
        since -= seconds * count
        current_depth += 1
        i += 1
    return gettext(" ").join(result)