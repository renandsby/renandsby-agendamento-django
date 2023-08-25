from django.contrib import admin
from .models import Agendamento


class AgendamentoAdmin(admin.ModelAdmin):
    ...

admin.site.register(Agendamento, AgendamentoAdmin)
