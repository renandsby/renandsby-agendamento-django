from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from core.views import serve_protected_document
urlpatterns = [
    path(
        "api/",
        include(
            [   
                path("adolescentes/", include("adolescentes.urls")),
                path("processos/", include("processos.urls")),
                path("unidades/", include("unidades.urls")),
                path("dominios/", include("dominios.urls")),
            ]
        ),
    ),
    path("", include("custom_auth.urls")),
    path("", include("rotina_modulo.urls", namespace="rotina_modulo")),
    
    path("prontuario/", include("prontuario.urls", namespace="prontuario")),
    path("rede_de_apoio/", include("rede_de_apoio.urls", namespace="rede_de_apoio")),
    path("tjdft/", include("tjdft.urls", namespace="tjdft")),
    path("central/", include("central.urls", namespace="central")),
    path("nai/", include("nai.urls", namespace="nai")),
    path("livro/", include("livro.urls", namespace="livro")),
    path("uama/", include("uama.urls", namespace="uama")),
    
    path("tutorial/", include("tutorial.urls", namespace="tutorial")),
    
    path("admin/", admin.site.urls),
    path(settings.MEDIA_URL[1:]+'<path:file>', serve_protected_document, name='media_serve'),

    # path("estatistica/", include("estatistica.urls", namespace="estatistica")),
	# path('django_plotly_dash/', include('django_plotly_dash.urls')),
]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
