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
                path("dominios/", include("dominios.urls")),
            ]
        ),
    ),
    path("", include("custom_auth.urls")),

    path("posicao/", include("posicao.urls", namespace="posicao")),
    # path("vagas/", include("vagas.urls", namespace="vagas")),
    path("dadosEmpresa/", include("dadosEmpresa.urls", namespace="dadosEmpresa")),
    path("usuario_empresa/", include("usuario_empresa.urls", namespace="usuario_empresa")),
    path("agendamento/", include("agendamento.urls", namespace="agendamento")),
    path("admin/", admin.site.urls),
    path(settings.MEDIA_URL[1:]+'<path:file>', serve_protected_document, name='media_serve'),

    # path("estatistica/", include("estatistica.urls", namespace="estatistica")),
	# path('django_plotly_dash/', include('django_plotly_dash.urls')),
]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
