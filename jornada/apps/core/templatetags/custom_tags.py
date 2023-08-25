import base64
import os
from core.forms import Bootstrap5FormClassInjecter
from django import forms, template
from django.utils import timezone
from django import template
from django import forms
from django.forms.forms import NON_FIELD_ERRORS
from django.forms.utils import ErrorDict

register = template.Library()


register = template.Library()

@register.filter
def nice_errors(form, non_field_msg='Erro de formulário'):
    nice_errors = ErrorDict()
    if isinstance(form, forms.BaseForm):
        for field, errors in form.errors.items():
            if field == NON_FIELD_ERRORS:
                key = non_field_msg
            else:
                key = form.fields[field].label
            nice_errors[key] = errors
    return nice_errors.items()

@register.filter(name="is_floatable")
def is_floatable(field):
    return (
        isinstance(field.field.widget, forms.widgets.TextInput)
        or isinstance(field.field.widget, forms.widgets.PasswordInput)
        or isinstance(field.field.widget, forms.widgets.DateInput)
        or isinstance(field.field.widget, forms.widgets.Select)
        or isinstance(field.field.widget, forms.widgets.NumberInput)
    )

@register.simple_tag
def define(val=None):
  return val

@register.filter(name='has_group') 
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

@register.filter
def add_class(value, class_name):
    current_classes = value.field.widget.attrs.get("class", "")
    return value.as_widget(attrs={"class": " ".join((current_classes, class_name))})


@register.filter
def add_bootstrap_form_class(obj):
    if hasattr(obj, "field"):
        Bootstrap5FormClassInjecter.handle_field(obj.field)
    return obj

@register.filter
def get_base64_file_name(file_path):
    basename = os.path.basename(str(file_path))
    fileinitial, ext = os.path.splitext(basename)
    
    if len(fileinitial) > 5:
        try:
            new_name = fileinitial[:-5] + '=='
            base64_bytes = new_name.encode("utf-8")
            file_initial_bytes = base64.b64decode(base64_bytes)
            fileinitial = file_initial_bytes.decode("utf-8")
        except:
            ...
                    
    return "".join([fileinitial,ext])

@register.filter
def attrs(value, arg):
    no_spaces = arg.replace(" ", "")
    args_list = no_spaces.split(",")

    for arg_string in args_list:
        splitted = arg_string.split("=")
        value.field.widget.attrs[splitted[0]] = splitted[1]

    return value


@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)


@register.filter
def dump_var(var):
    print(var)
    return var


@register.filter
def parse_bs_alert(var):
    mapping = {"error": "danger", "warning": "warning", "info": "primary", "success":"success", "debug":"secondary"}
    return mapping[var]


@register.filter
def replace(value, arg):
    """
    Replacing filter
    Use `{{ "aaa"|replace:"a|b" }}`
    """
    if len(arg.split("|")) != 2:
        return value

    what, to = arg.split("|")
    return str(value).replace(what, to)


@register.filter
def dictitem(dictionary, key):
    return dictionary.get(key)


@register.filter
def divide(value, arg):
    try:
        return int(value) / int(arg)
    except (ValueError, ZeroDivisionError):
        return None


@register.filter
def get_referer(request):
    return request.META.get("HTTP_REFERER")


@register.simple_tag
def define(val=None):
    return val


@register.simple_tag
def call_method(obj, method_name, *args):
    method = getattr(obj, method_name)
    return method(*args)


