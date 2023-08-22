from django.urls import path

from . import views

app_name = 'livro'

urlpatterns = [
    path("<uuid:livro_uuid>/report/", views.LivroReportView.as_view(),name="livro-report"),
]
