from django.contrib import admin
from .models import Ligacao

class LigacaoAdmin(admin.ModelAdmin):
    model = Ligacao


admin.site.register(Ligacao, LigacaoAdmin)